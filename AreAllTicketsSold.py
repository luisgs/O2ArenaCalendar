from urllib.request import urlopen
from bs4 import BeautifulSoup
import logging
import sys

URL = 'https://www.ticketportal.cz/Event/METALLICA'
URL2 = 'http://retro.ticketportal.cz/activeRoot/VIPzone_seatingPlan.asp?eventID=972'

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)


def ThereAreTickets(URL):
    logging.info('AreAllTicketsSold: reading URL and parsing it!')
    # We read ticket website
    soup = BeautifulSoup(urlopen(URL))
    text = soup.findAll("div", attrs={"class": "status"})

    # We have parsed a html file and we know that in a div class called 'status'
    # 'status' class contains a string that says: no more tickets
    if text is not None and len(text) > 0:
        text = text[0].find('p').text
        if text.find('V síti Ticketportal nyní vyprodáno.') != -1:  # no tickets
            logging.info("THere are NO tickets left!!")
            return 0    # All is sold!
        else:
            # for any reason this text changes...
            logging.info("there ARE tickets left")
            return 1    # Not all is sold
    else:
        # if this div class is not found, it means taht there ARE tickets
        logging.info("there ARE tickets left")
        return 1    # Not all is sold


if __name__ == "__main__":
    ThereAreTickets(URL2)
