import sys, logging
import urllib2
from bs4 import BeautifulSoup

O2EventsURL = "https://www.o2arena.cz/en/events/"
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)


def cleanHTML(O2RawPage):
    soup = BeautifulSoup(O2RawPage, 'html.parser')
#    print soup.find_all("div", attrs={"id": "events_index"})
    soup2 = soup.find_all("div", attrs={"class": "event_preview toLeft"})
    print(soup2[0])



def curlURL(hola):
    logging.info('curlURL function')
    # we request to read an URL
    page = urllib2.urlopen(O2EventsURL)
    # we read it and save it
    page_content = page.read()
    cleanHTML(page_content)


def main():
    curlURL(O2EventsURL)

if __name__ == "__main__":
    sys.exit(main())
