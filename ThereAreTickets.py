from urllib.request import urlopen
from bs4 import BeautifulSoup
import logging
import sys
from urllib.error import HTTPError


URL = 'https://www.ticketportal.cz/Event/METALLICA'
URL2 = 'https://www.o2arena.cz/en/events/Ritchie-Blackmore´s-RAINBOW_438.html'

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)


def ThereAreTickets(URL):
    """ ThereAreTickets?
    We received an URL where to buy tickets and scrap it
    if there are tickets left = 1
    if not = 0
    eoc = -1
    """
    logging.info('AreAllTicketsSold: reading URL and parsing it!')
    # We read ticket website
    try:
        soup = BeautifulSoup(urlopen(URL))
    except HTTPError as error:
        logging.info('ThereAreTickets: Error while openning a url')
        logging.info('URL: Error code is %s'% error)
#        logging.info('URL: %s'% (URL))
        return -1

    try:
        text = soup.findAll("div", attrs={"class": "status"})
    except:
        logging.info('ThereAreTickets: Error parsing an URL')
        logging.info('URL: %s'% (URL))
        return -1

    # We have parsed a html file and we know that in a div class called 'status'
    # 'status' class contains a string that says: no more tickets
    if text is not None and len(text) > 0:
        text = text[0].find('p').text
        if text.find('V síti Ticketportal nyní vyprodáno.') != -1:  # no tickets
#            logging.info("There are NOT tickets left!!")
            return 0    # All is sold!
        else:
            # for any reason this text changes...
#            logging.info("There ARE tickets left")
            return 1    # Not all is sold
    else:
        # if this div class is not found, it means taht there ARE tickets
#        logging.info("There ARE tickets left")
        return 1    # Not all is sold


if __name__ == "__main__":
    ThereAreTickets(URL2)
