import requests
from bs4 import BeautifulSoup
import re
import datetime
import hashlib


def parse_date(date_string):
    matches = re.search(r'([0-9]{2})\.([0-9]{2})\.(2[0-9]{3})', date_string)
    year = int(matches[3])
    month = int(matches[2])
    day = int(matches[1])
    return datetime.datetime(year, month, day)


def get_latest_events_2():
    response = requests.get("http://www.kufstein.at/de/events.html")
    soup = BeautifulSoup(response.content, 'html.parser')

    events = []
    items = soup.select('.tmEventsGroup')
    for item in items:
        title_tag = item.select_one('.title')
        date = item.select_one('.date')
        link_tag = item.select_one('a', href=True)
        short_tag = item.select_one('.text')
        location = item.select_one('.addition')

        name = item.select_one('.title')

        hash = hashlib.sha256()
        hash.update(bytes(str(name),'utf-8'))
        hash.update(bytes(str(location), 'utf-8'))
        hash.update(bytes(str(date), 'utf-8'))

        events.append({
            "name": title_tag.contents[0].strip(),
            "date": date,
            "location": location,
            "link": "https://www.fh-kufstein.ac.at" + link_tag['href'].strip(),
            "short": short_tag.contents[0].strip(),
            "source": "FH Kufstein Homepage",
            "identifier": hash.hexdigest()
        })

    return events
