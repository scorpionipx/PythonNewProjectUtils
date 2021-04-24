from os.path import (
    dirname as directory_name,
    join as join_paths,
)


# prepare Python environment on TeamCity build agent
# ======================================================================================================================
import sys

sys.path.append(directory_name(directory_name(__file__)))
# ======================================================================================================================


from requests import session as http_session

from base64 import b64decode

from lxml import html

from packaging import version as version_parser

# local imports
# ======================================================================================================================
try:
    # for local builds
    from tc.scripts import utils
    from tc.scripts.publish_artifacts import get_release_description
except ImportError:
    # for TeamCity builds
    from scripts import utils
    from scripts import publish_artifacts
# ======================================================================================================================


ROOT_DIRECTORY = utils.ROOT_DIRECTORY
BUILD_CONFIGURATION = utils.BUILD_CONFIGURATION


def get_latest_version(repository_url):
    """get_latest_version

    :param repository_url: repository's url
    :type repository_url: str
    :return: latest release version
    :rtype: str
    """
    print('Logging into session for private project...')
    session = http_session()
    login_response = session.get('https://github.conti.de/login')
    tree = html.fromstring(login_response.content)
    data = {i.get('name'): i.get('value') for i in tree.cssselect('input')}
    pvrt_ipx = r'D:\Tools\TeamCity\buildAgent\auth\github\pvrt.ipx'
    b64encoded_user, b64encoded_password = utils.get_pvrt_credentials(pvrt_ipx)
    data['login'] = b64decode(b64encoded_user).decode('ascii')
    data['password'] = b64decode(b64encoded_password).decode('ascii')
    login_response = session.post('https://github.conti.de/session', data=data)
    if login_response.status_code == 200:
        print('Successfully logged into session!')
    else:
        error = 'Failed to establish session! {}'.format(login_response)
        print(error)
        return False

    latest_release_link = '{}/releases/latest'.format(repository_url)
    response = session.get(latest_release_link)
    latest_release_formatted_link = str(response.url)
    if latest_release_formatted_link.endswith('releases'):
        # no releases available
        return '0.0.0'

    latest_version = latest_release_formatted_link.split('/')[-1].strip().replace('v', '')
    return latest_version


def get_current_version(version_file_path):
    """get_current_version

        Extract current build version number from app version file.
    :param version_file_path: Absolute path to version file (version.txt / cm_template_version.txt).
    :type version_file_path: str
    :return: current version
    :rtype: str
    """
    try:
        file_handler = open(version_file_path, 'r')
        file_content = file_handler.read()
        file_handler.close()
    except Exception as exception:
        error = 'Failed to open version file! {}'.format(exception)
        print(error)
        return False

    try:
        version_line = file_content.split('\n')[0]
        del file_content

        current_version = version_line[version_line.find('\''):].strip().replace('\'', '')
    except Exception as exception:
        error = 'Failed to parse version file! {}'.format(exception)
        print(error)
        return False
    return current_version


# main function
def check_version(old_version, current_version):
    """check_version

        Current build version should be greater than the last release version.
    :param old_version: latest release version
    :type old_version: str
    :param current_version: current build version
    :type current_version: str
    :return:
    """
    print('Checking current version number: {} vs latest release version number: {}...'
          .format(old_version, current_version))
    if version_parser.parse(old_version) >= version_parser.parse(current_version):
        print('Invalid number version! Latest release version available: {}! Current build version: {}'
              .format(old_version, current_version))
        print('Build version must be higher than the latest release version!')
        return False
    print('Version number ok!')
    return True


if __name__ == '__main__':
    app_version_file_path = join_paths(ROOT_DIRECTORY, BUILD_CONFIGURATION['app_version_file'])
    current_build_version = get_current_version(version_file_path=app_version_file_path)
    latest_release_version = get_latest_version(repository_url=BUILD_CONFIGURATION['repository_url'])
    if not check_version(
            old_version=latest_release_version,
            current_version=current_build_version,
    ):
        exit(utils.ERROR_CODE_INVALID_VERSION_NUMBER)

    description = publish_artifacts.get_release_description()
    if not description:
        error = 'Failed to retrieve release description!'
        print(error)
        exit(utils.ERROR_CODE_INVALID_RELEASE_DESCRIPTION)

    exit(0)  # no error
