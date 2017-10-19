import sys
import logging
import urllib2
from bs4 import BeautifulSoup


O2EventsURL = "https://www.o2arena.cz/en/events/"


logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)


List_events = []

event = {'name': '',
         'date': '',
         'hour': "All day event",
         'infoLink': "",
         'ticketsLink': "",
         'image': ""}


def cleanHTML(O2RawPage):
    logging.info('cleanHTML: extracting only HTML sectionwith events')
    soup = BeautifulSoup(O2RawPage, 'html.parser')
    soup2 = soup.find_all("div", attrs={"class": "event_preview toLeft"})

    return soup2


def insertInListEvents(Events):
    # PRE: We received part of the HTML text, only the raw section we want
    # SOL: we extract values we want AND insert them into our data structure
    logging.info('InsertInListEvents: Inserting events in our list')
    for i in range(len(Events)):
        name = Events[i].find('h3').find('a').text
        date_hour = Events[i].find('p').text
        if date_hour.find(',') != -1:   # found!
            date = Events[i].find('p').text.split(',')[0].replace(" ", "")
            hour = Events[i].find('p').text.split(',')[1][1:-4]
        else:
            date = date_hour
            hour = "00:00"
        infoLink = Events[i].find('h3').find('a').attrs['href']
        ticketsLink = Events[i].find('a').attrs['href']
        image = Events[i].find('div').attrs['style']

        # We complete our event entity with our data
        # data is stored in unicode. while printing will be fine
        event = {'name': name.encode('utf8'),
                 'date': date,
                 'hour': hour,
                 'infoLink': infoLink,
                 'ticketsLink': ticketsLink,
                 'image': image}
        # Insert event element in our list
        List_events.append(event.copy())
    print(List_events[0]['name'])
    print(List_events[0])


def curlURL(URL):
    logging.info('curl: URL function. Scraping website')
    # we request to read an URL
    page = urllib2.urlopen(URL)
    # we read it and send it
    return page.read()


def main():
    logging.info('MAIN: Main function')
    rawEvents = cleanHTML(curlURL(O2EventsURL))
    insertInListEvents(rawEvents)


if __name__ == "__main__":
    sys.exit(main())
