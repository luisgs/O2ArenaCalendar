

# iCalendar has the format below:
#
#
header= ('BEGIN:VCALENDARiVERSION:2.0\n'+
        'PRODID:-//ZContent.net//Zap Calendar 1.0//EN\n'+
        'CALSCALE:GREGORIAN\n'+
        'METHOD:PUBLISH\n'+
         'BEGIN:VTIMEZONE\n'+
         'TZID:Europe/Berlin\n'+
         'TZURL:http://tzurl.org/zoneinfo-outlook/Europe/Berlin\n'+
         'X-LIC-LOCATION:Europe/Berlin\n')
accion= ('BEGIN:VEVENT\n'+
        'SUMMARY:%s\n'+       # Event;s title
        'URL:%s\n'+           # URL with additional info
        'UID:2008-04-28-04-15-56-62-@americanhistorycalendar.com\n'+
        'SEQUENCE:0\n'+
        'STATUS:CONFIRMED\n'+
        'TRANSP:TRANSPARENT\n'+
        'RRULE:FREQ=YEARLY;INTERVAL=1;BYMONTH=2;BYMONTHDAY=12\n'+
        'DTSTART:%s\n'+     # Event start
        'DTEND:%s\n'+       # Event end
        'DTSTAMP:20150421T141403\n'+
        'CATEGORIES:%s\n'+  # Category!
        'LOCATION:%s\n'+    # Location
        'DESCRIPTION:%s\n'+    # Description
        'END:VEVENT\n')
footer= 'END:VCALENDAR'


def generateiCalEvent(event):
    return accion % (event['name'], event['infoLink'], event['date'],
                     "CATEGORIA", event['hour'], "LOCATION",
                     event['ticketsLink'])

def toiCalendar(List_Event):
    # Entry value has the following structure: it is a LIST!!!
    # [      event = {'name': '',
    #               'date': ''
    #               'hour': "All day event",
    #               'infoLink': "",
    #               'ticketsLink': "",
    #               'image': ""}
    # ]
    print(accion%("Title!!!", "URL!!", "comienzo", "final", "categoria", "location", "description"))



if __name__ == "__main__":
    toiCalendar("asd")
