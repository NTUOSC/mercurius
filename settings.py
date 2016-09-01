import os
import json
import logging
# load config file

try:
    settings_file = open('settings/settings.json')
    config =  json.load(settings_file)
except FileNotFoundError:
    print('configuration file not found')
    sys.exit(1)
except json.JSONDecodeError:
    print('configuration file error')
    sys.exit(1)

KEYS = {}
try:
    for kp in config['keys']:
        KEYS[kp['block']] = kp['key']
except KeyError:
    pass

FUNCTION_BLOCK = config['function_block']

STUDENT_BLOCK = config['student_block']

LATENCY = 1 / config.get('fequency', 2)

VOTE_TOKEN_NAME = config.get('token_name', 'token')

VOTE_TOKEN = config.get('token', '')

VOTE_PATH = config.get('VOTE_PATH', 'http://httpbin.org/post')

def RUN(content):
    for cmd in config['commands']:
        if cmd['name'] == content:
            os.system(cmd['command'])

LOGGING_PATH = config.get('logging_path', '/var/log/mercurius.log')

logging.basicConfig(filename=LOGGING_PATH, level=logging.DEBUG,
        format='%(asctime)s:%(name)s:%(levelname)s:%(message)s')

DEBUG = False
