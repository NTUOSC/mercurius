import sys
import json
import logging
from time import sleep
from threading import Thread

import requests

import settings
from MFRC522.MFRC522 import AuthError

from reader import read_card

def heart_beat():
    if not hasattr(settings, 'HEART_BEAT_PATH'):
        return
    if settings.HEART_BEAT_PATH is None:
        while True:
            sleep(10)

    while True:
        try:
            res = requests.head(settings.HEART_BEAT_PATH, timeout=1)
            logging.debug(res)
        except Exception as e:
            logging.error('[Network Error] %s' % e)
        finally:
            sleep(10)

def reader():
    logging.info('start to waiting for cards')
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

        # staff card
        try:
            sb = settings.STAFF_BLOCK
            card = read_card(block=sb, key=settings.KEYS[sb])
        except AuthError:
            pass
        except Exception as e:
            logging.error(e)
        else:
            if card is not None:
                logging.info("get staff card (%s)" % card.cid)
                try:
                    logging.info("get staff card (%s)" % card.content)
                    username = card.content.split(':')[0]
                    password = card.content.split(':')[1]
                except:
                    logging.error('Wrong format of staff card')
                    continue

                try:
                    res = requests.post(settings.STAFF_PATH, data={
                        'username': username,
                        'password': password,
                        })
                    logging.debug(res)
                except Exception as e:
                    logging.error('[Network Error] %s' % e)
                else:
                    if res.status_code != 200:
                        logging.warn(res.text)

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
                        'student_id': card.content[0:10],
                        'card_id': card.cid,
                        settings.VOTE_TOKEN_NAME: settings.VOTE_TOKEN
                        })
                    logging.debug(res)
                except Exception as e:
                    logging.error('[Network Error] %s' % e)
                else:
                    if res.status_code != 200:
                        logging.warn(res.text)

        # fequency of scanning
        sleep(settings.LATENCY)

if __name__ == '__main__':
    heart_beat_thread = Thread(target=heart_beat, daemon=True)
    heart_beat_thread.start()

    reader_thread = Thread(target=reader, daemon=True)
    reader_thread.start()
    try:
        heart_beat_thread.join()
    except (KeyboardInterrupt, SystemExit):
        sys.exit()
