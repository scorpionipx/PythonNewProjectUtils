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


from shutil import (
    rmtree as delete_directory,
)

from os import (
    W_OK,
    access,
    chmod,
    remove as delete_file,
)

from stat import S_IWUSR


ROOT_DIRECTORY = utils.ROOT_DIRECTORY
BUILD_CONFIGURATION = utils.BUILD_CONFIGURATION


def cleanup_package():
    """cleanup_package

        Delete unnecessary content.
    :return: process result
    :rtype: bool
    """
    print('Deleting unnecessary content...')

    # specify relative path to the root (e.g.: CarMaker/src, CarMaker/include)
    to_be_deleted_directories = [
        'lab2daq_info/lab2daq_info_logs',
    ]
    to_be_deleted_directories.sort()  # sort the list (alphabetically) for an easier overview in the log

    # do not specify files in this tuple if they are within to_be_deleted_directories
    # specify relative path to the root (e.g.: CarMaker/doc/Docs_link.url)
    to_be_deleted_files = [

    ]
    to_be_deleted_files.sort()  # sort the list (alphabetically) for an easier overview in the log

    if to_be_deleted_directories:
        print('Deleting directories:')
        # enumerating directories
        for to_be_deleted_directory in to_be_deleted_directories:
            print('- {}'.format(to_be_deleted_directory))

        total = len(to_be_deleted_directories)
        for index, to_be_deleted_directory in enumerate(to_be_deleted_directories):
            print('[{}/{}] Deleting directory: {}...'.format(index + 1, total, to_be_deleted_directory))
            try:
                delete_directory(to_be_deleted_directory)
            except Exception as exception:
                error = 'Failed to delete directory: {}! {}'.format(to_be_deleted_directory, exception)
                print(error)
                return False
        print('Directories deleted!')
    else:
        print('No directory specified to be deleted! Step skipped!')

    if to_be_deleted_files:
        print('Deleting files:')
        for to_be_deleted_file in to_be_deleted_files:
            print('- {}'.format(to_be_deleted_file))

        total = len(to_be_deleted_files)
        for index, to_be_deleted_file in enumerate(to_be_deleted_files):
            print('[{}/{}] Deleting file: {}...'.format(index + 1, total, to_be_deleted_file))
            try:
                delete_file(to_be_deleted_file)
            except Exception as exception:
                error = 'Failed to delete file: {}! {}'.format(to_be_deleted_file, exception)
                print(error)
                return False
        print('Files deleted!')
    else:
        print('No file specified to be deleted! Step skipped!')

    return True


def handle_delete_errors(func, path, _):
    """handle_delete_errors

        Used for hidden or read-only files to by-pass access limitations.
    :param func: caller
    :param path: path that caused the error
    :param _: to be displayed
    :return: function call
    """
    if not access(path, W_OK):
        chmod(path, S_IWUSR)
        func(path)


# main function
def prepare_release_package():
    """prepare_release_package

        Prepare the artifacts to be published.
    :return: process result
    :rtype: bool
    """
    if not cleanup_package():
        return False

    return True


if __name__ == '__main__':
    if not prepare_release_package():
        exit(utils.ERROR_CODE_FAILED_TO_PREPARE_RELEASE_PACKAGE)
    exit(0)
