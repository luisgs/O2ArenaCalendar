from icalendar import vCalAddress, vText, Calendar, Event
from datetime import datetime
import pytz

# iCalendar


def toiCalendar(List_Event):
    # Entry value has the following structure: it is a LIST!!!
    # [      event = {'name': '',
    #               'dstart': ''
    #               'dtend': ''
    #               'category': "All day event",
    #               'infoLink': "",
    #               'ticketsLink': "",
    #               'image': ""}
    # ]
    cal = Calendar()
    cal.add('prodid', '-//O2 Arena calendar')
    cal.add('version', '2.0')
    organizer = vCalAddress('MAILTO:email@noreply.com')

    location = vText('O2Arena at Ceskomoravska')

    dtstamp = datetime(2017, 10, 24, 0, 0, 0, tzinfo=pytz.utc)

    for i in (range(len(List_Event))):
        event = Event()
#        print("Elem %i and name %s" %(i, List_Event[i]['name']))
#        print(List_Event[i]['dtstart'])
        event.add('dtstart', List_Event[i]['dtstart'])
        event.add('dtend', List_Event[i]['dtend'])
        event.add('summary', (List_Event[i]['name']))
        event.add('description', "Information regarding this event via: " +
                  (List_Event[i]['infoLink']) + ". You can buy tickets via: " +
                  List_Event[i]['ticketsLink'])
        event.add('location', location)
        event.add('organizer', organizer)
        event.add('dtstamp', dtstamp)
        event['uid'] = ("%s/%i@luisgs.github" % (dtstamp.strftime("%Y%m%d"), i))
        #  print(event)
        cal.add_component(event)
        cal_content = cal.to_ical()

    with open("O2ArenaCalendar.ics", 'wb') as f:
        f.write(cal_content)


if __name__ == "__main__":
    toiCalendar("asd")
