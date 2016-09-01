import logging

from MFRC522 import MFRC522

logger = logging.getLogger('reader')


class Card(object):
    def __init__(self, cid=None, content=None):
        self.cid = cid
        self.content = content

    def __str__(self):
        return '(%r, %r)' % (self.cid, self.content)

    def __repr__(self):
        return 'Card(%r, %r)' % (self.cid, self.content)


def read_card(block=56, sector=None, key=None):
    if key is None:
        key = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
    # If sector is set, ignore block
    if sector is not None:
        block = sector * 4  # 4 blocks per sector
        sector = None

    with MFRC522.MFRC522Reader() as reader:
        card = Card()

        # Scan for cards
        (status, TagType) = reader.MFRC522_Request(reader.PICC_REQIDL)

        # If a card is found
        if status == reader.MI_OK:
            logger.debug("Card detacted")
        else:
            return None

        # Get the cid of the card
        status, cid = reader.MFRC522_Anticoll()

        if status != reader.MI_OK:
            logger.error('fail to read card id')
            raise Exception('Card error')

        # If we have the cid, prepare to read the content
        card.cid = '%02x%02x%02x%02x' % (cid[0], cid[1], cid[2], cid[3])
        logger.debug("card found (%s)", card.cid)
        reader.MFRC522_SelectTag(cid)
        status = reader.MFRC522_Auth(reader.PICC_AUTHENT1A, block, key, cid)

        # read the content
        if status != reader.MI_OK:
            logger.error('fail to read card content')
            raise Exception('Card error')

        data = reader.MFRC522_Read(block)
        card.content = "".join([chr(i) for i in data if i != 0])
        logger.debug('get card content (%s)', card.content)
        # stop raeding
        reader.MFRC522_StopCrypto1()

    return card

if __name__ == '__main__':
    while True:
        card = read_card(block=0, key=[0xff, 0xff, 0xff, 0xff, 0xff, 0xff])
        print(card)
