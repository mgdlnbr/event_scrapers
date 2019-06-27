import requests
from bs4 import BeautifulSoup
import re
import datetime
import hashlib


def parse_location(location_string):
    matches = re.search(r'Ort: (.*)$', location_string.strip())

    if matches:
        return matches[1]
    else:
        return ""


def parse_date(date_string):
    matches = re.search(r'([0-9]{2})\.([0-9]{2})\.(2[0-9]{3})', date_string)
    year = int(matches[3])
    month = int(matches[2])
    day = int(matches[1])
    return datetime.datetime(year, month, day)


def get_latest_events():
    response = requests.get("https://www.fh-kufstein.ac.at/ger/Veranstaltungen")
    soup = BeautifulSoup(response.content, 'html.parser')

    events = []
    items = soup.select('.news-item')
    for item in items:
        title_tag = item.select_one('.title')
        date_tag = item.select_one('.date')
        link_tag = item.select_one('a')
        short_tag = item.select_one('.eztext-field')

        name = title_tag.contents[0].strip()
        date = parse_date(date_tag.contents[0])
        location = parse_location(date_tag.contents[2])

        hash = hashlib.sha256()
        hash.update(bytes(name,'utf-8'))
        hash.update(bytes(location, 'utf-8'))
        hash.update(bytes(str(date.time()), 'utf-8'))

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

