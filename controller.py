import sys
import json
import logging
from time import sleep

import requests

import settings
from MFRC522.MFRC522 import AuthError

from reader import read_card

logger = logging.getLogger('controller')

logger.info('start to waiting for cards')
while True:
    # checking content
    # function card
    try:
        fb = settings.FUNCTION_BLOCK
        card = read_card(block=fb, key=settings.KEYS[fb])
    except AuthError:
        pass
    except Exception as e:
        logging.error(e)
    else:
        if card is not None:
            logging.info('get command "%s"' % card.content)
            settings.RUN(card.content)

    # student card
    try:
        sb = settings.STUDENT_BLOCK
        card = read_card(block=sb, key=settings.KEYS[sb])
    except AuthError:
        pass
    except Exception as e:
        logging.error(e)
    else:
        if card is not None:
            logging.info("get student card (%s)" % card.content[0:9])
            try:
                res = requests.post(settings.VOTE_PATH, data={
                    'student_id': card.content,
                    'card_id': card.cid,
                    settings.VOTE_TOKEN_NAME: settings.VOTE_TOKEN
                })
            except Exception as e:
                logger.error('[Network Error] %s' % e)
            else:
                if res.status_code != 200:
                    logging.warn(res.text)

    # fequency of scanning
    sleep(settings.LATENCY)
