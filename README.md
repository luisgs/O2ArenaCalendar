# O2 Arena Calendar

This script is capable of scrapping O2 Arena website (event;s page) and create an ics file or icalendar file.

O2 Arena website: o2arena.cz/en/events/

## Getting Started

If you are willing to have and run this script locally, please follow the steps below. iCalendar file will be generated with as many events as O2 Arena website has. This script has not historical db so events that do not appear in this URL will not appear.

This script also double checks if there are tickets left to buy; if there are NOT, it will add an ALARM and it will also write into the 'description' : this event is full.

### Prerequesites

This script requires:
```
* Python3
* bs4 lib
* [icalendar lib](http://icalendar.readthedocs.io/en/latest/install.html)
```

### Executing

```
git clone https://github.com/luisgs/O2ArenaCalendar.git
python3 o2calendar.py
```

This script will generate a file called: "o2arencacalendar.ics" in the same folder where this script is executed.

### Output
There is a icalendar.ics output posted in this repo and it is named: O2ArenaCalendar.ics
