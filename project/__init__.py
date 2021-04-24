import sys


from logging import (
    getLogger as GetLogger,
    FileHandler as LoggerFileHandler,
    Formatter as LoggerFormatter,
    StreamHandler as LoggerStreamHandler,

    INFO as LOGGER_LEVEL_INFO,
)


from os import (
    environ as environment,
    getlogin,
    makedirs as make_directory,
)

from os.path import (
    abspath as absolute_path,
    dirname as directory_name,
    isdir as is_directory,
    join as join_paths,
)


from platform import (
    architecture,
    machine,
    platform,
    processor,
)


from time import gmtime, strftime


from .version import __version__


APP_NAME = ''  # application's name (e.g.: PDF to HTML Converter)
APP_SLUG = ''  # application's slug, html safe string (e.g.: pdf_to_html_converter)
APP_ASCII_ART = r""""""  # custom ASCII art (e.g.: ¯\_(ツ)_/¯ )

APP_DEVELOPMENT_REPOSITORY = ''  # usually GitHub development repository
APP_RELEASE_PAGE = ''  # releases page
APP_LATEST_RELEASE_PAGE = ''  # latest release URL

AUTHORS = (
    'ScorpionIPX',
)

__authors_formatted__ = ''
for author in AUTHORS:
    __authors_formatted__ += '\t- {}\n'.format(author)

STATION = environment['COMPUTERNAME']
USER = getlogin()


if getattr(sys, 'frozen', False):
    CURRENT_DIR = directory_name(sys.executable)
elif __file__:
    CURRENT_DIR = directory_name(__file__)
else:
    CURRENT_DIR = absolute_path(directory_name(sys.argv[0]))

LOGS_DIR = join_paths(CURRENT_DIR, '{}_logs'.format(APP_SLUG))


if not is_directory(LOGS_DIR):
    try:
        make_directory(LOGS_DIR)
    except Exception as err:
        print("Failed to generate logging directory! {}\nUsing default log directory!".format(err))
        LOGS_DIR = join_paths(directory_name(__file__), '{}_logs'.format(APP_SLUG))
        make_directory(LOGS_DIR)


LOGGER = GetLogger(APP_SLUG)


log_formatter = LoggerFormatter('%(asctime)s: %(message)s', "%d-%b-%Y %H:%M:%S")
log_file_name = '{}_{}.log'.format(APP_SLUG, strftime("%Y_%m_%d_%H_%M_%S", gmtime()))
log_file = join_paths(LOGS_DIR, log_file_name)


file_output = LoggerFileHandler(log_file)
file_output.setFormatter(log_formatter)
file_output.setLevel(LOGGER_LEVEL_INFO)
LOGGER.addHandler(file_output)

console = LoggerStreamHandler()
console.setLevel(LOGGER_LEVEL_INFO)
console.setFormatter(log_formatter)
LOGGER.addHandler(console)

LOGGER.setLevel(LOGGER_LEVEL_INFO)

LOGGER.info('{} version {}'.format(APP_NAME, __version__))
LOGGER.info('Release page: {}'.format(APP_RELEASE_PAGE))
LOGGER.info('Author(s):\n{}'.format(__authors_formatted__))
LOGGER.info('Log file: {}'.format(log_file))
LOGGER.info('USER: {}'.format(USER))
LOGGER.info('STATION: {}'.format(STATION))
LOGGER.info('PLATFORM: {} {} {} {}\n'
            .format(platform(),
                    architecture(),
                    machine(),
                    processor(),
                    )
            )

if APP_ASCII_ART:
    LOGGER.info(APP_ASCII_ART)
