from json import loads

from os.path import (
    dirname as directory_name,
    join as join_paths,
)


ERROR_CODE_INVALID_VERSION_NUMBER = 69
ERROR_CODE_INVALID_RELEASE_DESCRIPTION = 70
ERROR_CODE_FAILED_TO_PREPARE_RELEASE_PACKAGE = 13
ERROR_CODE_FAILED_TO_PUBLISH_ARTIFACTS = 96
ERROR_CODE_FAILED_TO_BUILD_PROJECT = 66

ROOT_DIRECTORY = directory_name(directory_name(directory_name(__file__)))


def get_config(config_file):
    """get_config

    :param config_file: absolute path to JSON config file
    :type config_file: str
    :return: configuration
    :rtype: dict
    """
    try:
        file_handler = open(config_file, 'r')
        file_content = file_handler.read()
        file_handler.close()
    except Exception as exception:
        error = 'Failed to open config file! {}'.format(exception)
        print(error)
        raise InterruptedError(error)

    configuration = loads(file_content)
    del file_content

    return configuration


# content of tc_config.json as dictionary
BUILD_CONFIGURATION_PATH = join_paths(ROOT_DIRECTORY, 'tc', 'tc_config.json')
BUILD_CONFIGURATION = get_config(BUILD_CONFIGURATION_PATH)


def get_pvrt_credentials(credentials_path):
    """get_pvrt_credentials

    :param credentials_path:
    :return:
    """
    try:
        file_handler = open(credentials_path, 'r')
        file_content = file_handler.read()
        file_handler.close()
    except Exception as exception:
        error = 'Failed to open credentials file! {}'.format(exception)
        print(error)
        return False

    encoded_user = file_content.split('\n')[0]
    encoded_password = file_content.split('\n')[1]

    return encoded_user, encoded_password


if __name__ == '__main__':
    # testing
    c = get_config(BUILD_CONFIGURATION_PATH)
    print(c)
