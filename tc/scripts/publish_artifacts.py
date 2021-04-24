from os.path import (
    dirname as directory_name,
    join as join_paths,
)


# prepare Python environment on TeamCity build agent
# ======================================================================================================================
import sys

sys.path.append(directory_name(directory_name(__file__)))
# ======================================================================================================================


try:
    # for local builds
    from tc.scripts import utils
    from tc.scripts import version_number_check
except ImportError:
    # for TeamCity builds
    from scripts import utils
    from scripts import version_number_check


from base64 import b64decode

from re import (
    search as regex_search,
    findall as regex_find_all,
)

from subprocess import check_output

ROOT_DIRECTORY = utils.ROOT_DIRECTORY
BUILD_CONFIGURATION = utils.BUILD_CONFIGURATION


def get_release_description():
    """get_release_description

        Extract release description from app version file.
    :return: description
    :rtype: str
    """
    app_version_file_path = join_paths(ROOT_DIRECTORY, BUILD_CONFIGURATION['app_version_file'])
    try:
        file_handler = open(app_version_file_path, 'r')
        file_content = file_handler.read()
        file_handler.close()
    except Exception as exception:
        error = 'Failed to open app version file! {}'.format(exception)
        print(error)
        return False

    all_versions_regex = r'(\d*\.\d*\.\d*)'
    number_of_versions = len(regex_find_all(all_versions_regex, file_content))

    if number_of_versions < 2:
        error = 'No description specified for first release! Please make changes in version.txt!\nDEBUG: NOV={}'\
            .format(number_of_versions)
        print(error)
        return False

    if number_of_versions == 2:
        # first release
        description = file_content
        return description

    current_build_version = version_number_check.get_current_version(version_file_path=app_version_file_path)

    major, minor, patch = current_build_version.split('.')
    regex = r'{}\.{}\.{}\n([\s\S]+?)\d*\.\d*.\d*\s'.format(major, minor, patch)

    # for version = 0.0.18, the regex will be: "0\.0\.18\s([\s\S]+?)\d*\.\d*.\d"

    # 0\.0\.18\s([\s\S]+?)\d*\.\d*.\d - EXPLANATION
    # 0 matches the character 0 literally (case sensitive)
    # \. matches the character . literally (case sensitive)
    # 0 matches the character 0 literally (case sensitive)
    # \. matches the character . literally (case sensitive)
    # 18 matches the characters 18 literally (case sensitive)
    # \s matches any whitespace character (equal to [\r\n\t\f\v ])
    # 1st Capturing Group ([\s\S]+?)
    # Match a single character present in the list below [\s\S]+?
    # +? Quantifier — Matches between one and unlimited times, as few times as possible, expanding as needed (lazy)
    # \s matches any whitespace character (equal to [\r\n\t\f\v ])
    # \S matches any non-whitespace character (equal to [^\r\n\t\f\v ])
    # \d* matches a digit (equal to [0-9])
    # * Quantifier — Matches between zero and unlimited times, as many times as possible, giving back as needed (greedy)
    # \. matches the character . literally (case sensitive)
    # \d* matches a digit (equal to [0-9])
    # . matches any character (except for line terminators)
    # \d matches a digit (equal to [0-9])

    try:
        description = regex_search(regex, file_content).group(1)
    except Exception as exception:
        error = 'Failed to parse regex! {}!\nPlease make sure you specified correct version number in version.txt for ' \
                'current build release description!'\
            .format(exception)
        print(error)
        return False

    return description


# main function
def publish_artifacts():
    """publish_artifacts

        Create release and upload artifacts.
    :return: process result
    :rtype: bool
    """

    app_version_file_path = join_paths(ROOT_DIRECTORY, BUILD_CONFIGURATION['app_version_file'])
    current_build_version = version_number_check.get_current_version(version_file_path=app_version_file_path)
    description = get_release_description()
    if not description:
        print('Could not retrieve release description!')
        return False

    pvrt_ipx = r'D:\Tools\TeamCity\buildAgent\auth\github\pvrt.ipx'
    b64encoded_user, b64encoded_password = utils.get_pvrt_credentials(pvrt_ipx)

    release_package_artifact_file_name = '{}.zip'.format(BUILD_CONFIGURATION['repository_name'])
    release_package_artifact = join_paths(ROOT_DIRECTORY, 'artifacts', release_package_artifact_file_name)

    github_published = r'D:\Tools\TeamCity\buildAgent\tools\github-release\github_release_handler_cmd.exe'
    os_cmd = '{} '.format(github_published)
    os_cmd += '--repository_name={} '.format(BUILD_CONFIGURATION['repository_name'])
    os_cmd += '--repository_owner={} '.format(BUILD_CONFIGURATION['repository_owner'])
    os_cmd += '--tag=v{} '.format(current_build_version)
    os_cmd += '--user={} '.format(b64decode(b64encoded_user).decode('ascii'))
    os_cmd += '--password={} '.format(b64decode(b64encoded_password).decode('ascii'))
    os_cmd += '--artifact={} '.format(release_package_artifact)
    # multiple lines string cannot be passed to exe sa argument, so $br is used to mark line feed
    os_cmd += '--description="{}" '.format(description.replace('\n', '$br'))

    upload_timeout = BUILD_CONFIGURATION.get('upload_artifacts_timeout', 1200)  # default 1200 sec

    try:
        os_process_output = check_output(
            os_cmd,
            universal_newlines=True,
            shell=True,
            bufsize=255,
            timeout=upload_timeout,  # seconds
        )
    except Exception as exception:
        error = 'Failed to run command! {}'.format(exception)
        print(error)
        exit(utils.ERROR_CODE_FAILED_TO_PUBLISH_ARTIFACTS)
        return False

    if os_process_output:
        print(os_process_output)
    return True


if __name__ == '__main__':
    if not publish_artifacts():
        exit(utils.ERROR_CODE_FAILED_TO_PUBLISH_ARTIFACTS)
    exit(0)
