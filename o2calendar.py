import sys, logging
import urllib2
from bs4 import BeautifulSoup


O2EventsURL = "https://www.o2arena.cz/en/events/"


logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)


List_events = []


def cleanHTML(O2RawPage):
    logging.info('cleanHTML function')
    soup = BeautifulSoup(O2RawPage, 'html.parser')
    soup2 = soup.find_all("div", attrs={"class": "event_preview toLeft"})

    return soup2


def insertInListEvents(Events):
    logging.info('Inserting events in our list')
    for i in range(len(Events)):
        name = Events[i].find('h3').find('a').text
        date_hour = Events[i].find('p').text
        if date_hour.find(',') != -1:   # found!
            date = Events[i].find('p').text.split(',')[0].replace(" ","")
            hour = Events[i].find('p').text.split(',')[1][1:-4]
        else:
            date = date_hour
            hour = "00:00"
        infoLink = Events[i].find('h3').find('a').attrs['href']
        ticketsLink = Events[i].find('a').attrs['href']
        image = Events[i].find('div').attrs['style']
       
        event = {'name' : name,
            'date' : date,
            'hour' : hour,
            'infoLink' : infoLink,
            'ticketsLink' : ticketsLink,
            'image': image}
        # Insert event element in our list
        List_events.append(event.copy())


def curlURL(hola):
    logging.info('curl: URL function')
    # we request to read an URL
    page = urllib2.urlopen(O2EventsURL)
    # we read it and send it
    return page.read()


def main():
    rawEvents = cleanHTML(curlURL(O2EventsURL))
    insertInListEvents(rawEvents)


if __name__ == "__main__":
    sys.exit(main())
