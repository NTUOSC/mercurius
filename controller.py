import sys
import json
import logging
from time import sleep

import requests

import settings

from reader import read_card

logger = logging.getLogger('controller')

while True:
    # checking content
    # function card
    try:
        fb = settings.FUNCTION_BLOCK
        card = read_card(block=fb, key=settings.KEYS[fb])
    except KeyError:
        pass
    except Exception as e:
        logging.error(e)
    else:
        logging.info('get command "%s"' % card.content)
        settings.RUN(card.content)

    # student card
    try:
        sb = settings.STUDENT_BLOCK
        card = read_card(block=sb, key=settings.KEYS[sb])
    except KeyError:
        pass
    except Exception as e:
        logging.error(e)
    else:
        logging.info("get student card (%s)" % card.content)
        res = requests.post(settings.VOTE_PATH, data={
            'student_id': card.content,
            'card_id': card.cid,
            settings.VOTE_TOKEN_NAME: settings.VOTE_TOKEN
        })
        if res.status_code != 200:
            logging.warn(res.text)

    # fequency of scanning
    sleep(settings.LATENCY)
