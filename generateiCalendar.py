from icalendar import vCalAddress, vText, Calendar, Event, Alarm
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

    location = vText('O2 Arena at Ceskomoravska')
    description = ""
    dtstamp = datetime(2017, 10, 24, 0, 0, 0, tzinfo=pytz.utc)

    for i in (range(len(List_Event))):
        event = Event()
        print("Elem %i and name %s" % (i, List_Event[i]['name']))
#        print(List_Event[i])
        event.add('dtstart', List_Event[i]['dtstart'])
        event.add('dtend', List_Event[i]['dtend'])
        event.add('summary', (List_Event[i]['name']))
        event.add('location', location)
        event.add('organizer', organizer)
        event.add('url', List_Event[i]['infoLink'])
        event.add('geo', '50.104788;14.493774')
        event.add('dtstamp', dtstamp)
        event['uid'] = ("%s/%i@luisgs.github" % (dtstamp.strftime("%Y%m%d"), i))
        # if there are NOT tickets left.
        if (List_Event[i]['TicketsLeft'] == 0):
            alarm = Alarm()
            alarm.add("action", "DISPLAY")
            alarm.add("description", "Reminder")
            alarm.add("TRIGGER;RELATED=START", "-PT{0}H".format(1))
            description = "This event is FULL! "
            event.add_component(alarm)
        #  print(event)
        event.add('description', description + List_Event[i]['description'])
        cal.add_component(event)
        #  print(event)
        cal_content = cal.to_ical()

    with open("O2ArenaCalendar.ics", 'wb') as f:
        f.write(cal_content)


if __name__ == "__main__":
    toiCalendar("asd")
