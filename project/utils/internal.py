from json import (
    loads as string_to_dict,
)

from packaging import (
    version as version_parser,
)

from requests import (
    get as http_request_get,
    post as http_request_post,
)


from project import (
    APP_NAME,
    LOGGER,
    STATION,

    __version__,
)


def submit_statistics():
    """submit_statistics

        Track this tool usage for statistics overview.
    :return: publish result
    :rtype: bool
    """
    raise NotImplemented('submit_statistics not implemented')


def get_this_tool_latest_release_tag(suppress_warning=False):
    """get_this_tool_latest_release_tag

        Get tag name of the latest release published on GitHub.
    :param suppress_warning: specify if warning should be suppressed (muted).
    :type suppress_warning: bool
    :return: tag name
    :rtype: str
    """
    api_link = ''  # to be filled by developer
    try:
        response = http_request_get(api_link)
        response_as_dict = string_to_dict(response.content)
        tag = response_as_dict.get('tag_name')
    except Exception as exception:
        assert exception
        warning = 'Warning! Failed to check {app} latest release version! To enable this feature, make sure you are ' \
                  'connected to Continental\'s intranet (VPN).\nThis is just a warning and will not affect tool\'s ' \
                  'functionality!'.format(app=APP_NAME)
        if suppress_warning:
            pass
        else:
            LOGGER.warning(warning)
        tag = None
    if not tag:  # no releases yet or no connection to release page
        tag = '0.0.0'
    return tag


LATEST_VERSION = get_this_tool_latest_release_tag()


def this_tool_is_up_to_date():
    """this_tool_is_up_to_date

        Check if this tool is up to date, comparing with the latest release available on GitHub page.
    :return: up to date status
    :rtype: bool
    """
    current_version = version_parser.parse(__version__)
    latest_version = version_parser.parse(LATEST_VERSION)
    result = current_version >= latest_version
    return result
