import logging

log = logging.getLogger(__name__)

# Log to file settings
logging.basicConfig(
    filename='net.log',
    filemode='a',
    format='[%(asctime)s %(filename)18s] %(levelname)-7s - %(message)7s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.DEBUG)

# Log to console setings
# set up log to console
console = logging.StreamHandler()
console.setLevel(logging.INFO)
# set a format which is simpler for console use
formatter = logging.Formatter('[%(asctime)s %(filename)18s] %(levelname)-7s - %(message)7s')
console.setFormatter(formatter)
# add the handler to the root logger
logging.getLogger(__name__).addHandler(console)

# logger = logging.getLogger(__name__) # use '' to get the log from other modules


