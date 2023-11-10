import logging

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s: %(name)s: %(message)s')
LOGGER = logging.getLogger('botmysterieux')
LOGGER.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='botmafieux.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
LOGGER.addHandler(handler)