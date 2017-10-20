import sys
import logging
import urllib2
from bs4 import BeautifulSoup
import datetime

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


def sparta_dates(text):
    logging.info('SPARTA DATES: Creating a list of dates')
    # we receive something like this:
    # 24. 10., 5. 11., 17. 11. ... 2017
    # we return:
    # [24102017, 05112017, 17112017]
    list_sparta_dates = []
    dates = text.replace(" ", "").encode('utf8').split('....')
    year = dates[-1]
    dayMonths = dates[0].split(',') # contains a list with dayMOnths dates.
    dates1 = dayMonths + [year]     # contains [11.5, 12.6, 13.5, 2017]
    for i in range(len(dayMonths)):
        fecha = datetime.datetime(int(dates1[-1]),
                                int(dates1[i].split('.')[1]),
                                int(dates1[i].split('.')[0])).strftime('%d%m%Y')
        # print(fecha)
        list_sparta_dates = list_sparta_dates + [fecha]
    # print(list_sparta_dates)
    logging.info('exiting SPARTA DATES')
    return list_sparta_dates


def insertInListEvents(Events):
    # PRE: We received part of the HTML text, only the raw section we want
    # SOL: we extract values we want AND insert them into our data structure
    logging.info('InsertInListEvents: Inserting events in our list')
    for i in range(len(Events)):
        name = Events[i].find('h3').find('a').text
        infoLink = Events[i].find('h3').find('a').attrs['href']
        ticketsLink = Events[i].find('a').attrs['href']
        image = Events[i].find('div').attrs['style']

        date_hour = Events[i].find('p').text
        # print(name)
        if name.encode('utf8') == 'Sparta':
            hour = "Sparta hour!"
            list_sparta_dates = sparta_dates(date_hour)
            # print("La fecha es %s"% ( sparta_dates(date_hour)))
            date = "Sparta"

            for i in range(len(list_sparta_dates)):
                # We fullfil our event entity with our data
                # data is stored in unicode. printing will show it correctly
                event = {'name': name.encode('utf8'),
                         'date': list_sparta_dates[i],
                         'hour': hour,
                         'infoLink': infoLink,
                         'category': "SPORT",
                         'ticketsLink': ticketsLink,
                         'image': image}
                # Insert event element in our list
                List_events.append(event.copy())
        else:
            if date_hour.find(',') != -1:   # found!
                date = Events[i].find('p').text.split(',')[0].replace(" ", "")
                hour = Events[i].find('p').text.split(',')[1][1:-4]
            else:
                date = date_hour
                hour = "00:00"
            # We fullfil our event entity with our data
            # data is stored in unicode. printing will show it correctly
            event = {'name': name.encode('utf8'),
                     'date': date,
                     'hour': hour,
                     'infoLink': infoLink,
                     'ticketsLink': ticketsLink,
                     'image': image}
            # Insert event element in our list
            List_events.append(event.copy())
        print(Events[0])
        break
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
