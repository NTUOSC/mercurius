import sys
import os
import json
import logging
# load config file

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SETTINGS_FILE = 'settings/settings.json'
SETTINGS_PATH = os.path.join(BASE_DIR, SETTINGS_FILE)

try:
    settings_file = open(SETTINGS_PATH)
    config =  json.load(settings_file)
except FileNotFoundError:
    print('configuration file not found')
    logging.critical('lost configuration file')
    sys.exit(1)
except json.JSONDecodeError:
    print('configuration file error')
    logging.critical('configuration file parse error')
    sys.exit(1)

KEYS = {}
try:
    for kp in config['keys']:
        KEYS[kp['block']] = kp['key']
except KeyError:
    pass

DEBUG = False

FUNCTION_BLOCK = config['function_block']

STUDENT_BLOCK = config['student_block']

LATENCY = 1 / config.get('fequency', 2)

VOTE_TOKEN_NAME = config.get('token_name', 'token')

VOTE_TOKEN = config.get('token', '')

VOTE_PATH = config.get('VOTE_PATH', 'http://httpbin.org/post')

def RUN(content):
    for cmd in config['commands']:
        if cmd['name'] == content:
            logging.info('execute %s' % cmd['command'])
            os.system(cmd['command'])


if DEBUG:
    LOGGING_PATH = os.path.join(BASE_DIR, 'mercurius.log')
    logging.basicConfig(filename=LOGGING_PATH, level=logging.DEBUG,
            format='%(asctime)s:%(name)s:%(levelname)s:%(message)s')
else:
    LOGGING_PATH = config.get('logging_path', '/var/log/mercurius.log')
    logging.basicConfig(filename=LOGGING_PATH, level=logging.INFO,
            format='%(asctime)s:%(name)s:%(levelname)s:%(message)s')

if FUNCTION_BLOCK not in KEYS:
    print('lack of function key')
    logging.critical('lack of function key')
    sys.exit(1)
if STUDENT_BLOCK not in KEYS:
    print('lack of student key')
    logging.critical('lack of student key')
    sys.exit(1)
