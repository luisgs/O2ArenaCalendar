import sys
import logging
from urllib.request import urlopen
from bs4 import BeautifulSoup
import datetime
import generateiCalendar
import pytz
import ThereAreTickets

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
    #  logging.info('cleanHTML: extracting only HTML sectionwith events')
    soup = BeautifulSoup(O2RawPage, 'html.parser')
    soup2 = soup.find_all("div", attrs={"class": "event_preview toLeft"})
    #  logging.info('exiting SPARTA DATES')
    return soup2


def sparta_dates(text):
    logging.info('SPARTA DATES: Creating a list of dates')
    # we receive something like this: string in utf
    # "24. 10., 5. 11., 17. 11. ... 2017"
    # we return:
    # [24102017, 05112017, 17112017] in a datetimeformat!!!
    list_sparta_dates = []
    #  print(text)
    dates = text.replace(" ", "").split('....')
    year = dates[-1]
    dayMonths = dates[0].split(',')     # contains a list with dayMOnths dates.
    dates1 = dayMonths + [year]         # contains [11.5, 12.6, 13.5, 2017]
    #
    #  event.add('dtstart', datetime(2010, 10, 10, 10, 0, 0,
    #       tzinfo=pytz.timezone("Europe/Vienna")))
    for i in range(len(dayMonths)):
        dtstart = datetime.datetime(int(dates1[-1]),
                                    int(dates1[i].split('.')[1]),
                                    int(dates1[i].split('.')[0]), 18, 20,
                                    tzinfo=pytz.timezone("Europe/Prague"))
        dtend = datetime.datetime(int(dates1[-1]),
                                  int(dates1[i].split('.')[1]),
                                  int(dates1[i].split('.')[0]), 20, 00,
                                  tzinfo=pytz.timezone("Europe/Prague"))
#        print(dtstart)
        list_sparta_dates = list_sparta_dates + [[dtstart, dtend]]
#    print(list_sparta_dates)
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
        description = ''
        date_hour = Events[i].find('p').text
        if name == 'Sparta':
            list_sparta_dates = sparta_dates(date_hour)
            # print("La fecha es %s"% ( sparta_dates(date_hour)))
            for i in range(len(list_sparta_dates)):
                # We fullfil our event entity with our data
                # data is stored in unicode. printing will show it correctly
                event = {'name': name,
                         'dtstart': list_sparta_dates[i][0],
                         'dtend': list_sparta_dates[i][1],
                         'infoLink': infoLink,
                         'category': "SPORT",
                         'description': description,
                         'ticketsLink': ticketsLink,
                         'image': image}
                # Insert event element in our list
                List_events.append(event.copy())
        else:
            if date_hour.find(',') != -1:   # found!
                if date_hour.find('hod') != -1:     # found it!
                    # date_hour has this form: 27.4.2017, 20.00 hod
                    date = Events[i].find('p').text.split(',')[0].replace(" ", "")
                    hour = Events[i].find('p').text.split(',')[1][1:-4]
                else:
                    # we have this case: 6. 1., 7. 1. 2018
                    date = Events[i].find('p').text.split(',')[0].replace(" ", "")+".2018"
                    hour = "17:00"
            else:
                date = date_hour
                hour = "17:00"
            #  print(date)
            #  print(name)
            dtstart = datetime.datetime(int(date.split('.')[-1]),
                                        int(date.split('.')[1]),
                                        int(date.split('.')[0]),
                                        int(hour.split(":")[0]),
                                        int(hour.split(":")[1]),
                                        tzinfo=pytz.timezone("Europe/Prague"))
            dtend = datetime.datetime(int(date.split('.')[-1]),
                                      int(date.split('.')[1]),
                                      int(date.split('.')[0]),
                                      int(hour.split(":")[0])+2,  # hours
                                      int(hour.split(":")[1]),
                                      tzinfo=pytz.timezone("Europe/Prague"))
            # We fullfil our event entity with our data
            # data is stored in unicode. printing will show it correctly
            #  print(date)
            #  print(dtstart)
            #  print(hour)
            description = 'Informational link via: ' + infoLink + \
                          '. You can buy tickets via: ' + ticketsLink
#            print(Events[0])
#            print(ticketsLink)
            TicketsSold = ThereAreTickets.ThereAreTickets(ticketsLink.replace("´",""))
            event = {'name': name,
                     'dtstart': dtstart,
                     'dtend': dtend,
                     'infoLink': infoLink,
                     'category': "OTHERS",
                     'ticketsLink': ticketsLink,
                     'description': description,
                     'image': image,
                     'TicketsSold': TicketsSold}
            # Insert event element in our list
            List_events.append(event.copy())
#        break
#    print(List_events[0]['name'])
#    print(List_events[0])
    logging.info('exiting inserting in LIst')


def curlURL(URL):
    # logging.info('curl: URL function. Scraping website')
    # we request to read an URL
    page = urlopen(URL)
    # we read it and send it
    return page.read()


def main():
    #  logging.info('MAIN: Main function')
    rawEvents = cleanHTML(curlURL(O2EventsURL))
    insertInListEvents(rawEvents)
    logging.info('generate iCalendar')
    generateiCalendar.toiCalendar(List_events)
    logging.info('exiting iCalendar')

if __name__ == "__main__":
    sys.exit(main())
