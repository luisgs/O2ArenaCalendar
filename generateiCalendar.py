from icalendar import vCalAddress, vText, Calendar, Event
from datetime import datetime

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

    organizer = vCalAddress('MAILTO:email@noreply.com')
    location = vText('O2Arena at Ceskomoravska')

    for i in (range(len(List_Event))):
        event = Event()
        print("Elem %i and name %s" %(i, List_Event[i]['name']))
        print(List_Event[i]['dtstart'])
        event.add('dtstart', List_Event[i]['dtstart'])
        event.add('dtend', List_Event[i]['dtend'])
        event.add('summary', (List_Event[i]['name']))
        event.add('location', location)
        event.add('organizer', organizer)
        event['uid'] = '20050115T101010/27346262376@mxm.dk'
        cal.add_component(event)
        cal_content = cal.to_ical()

    with open("meeting.ics", 'wb') as f:
        f.write(cal_content)


if __name__ == "__main__":
    toiCalendar("asd")
