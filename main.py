from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from declarations import Event, Base
from fhku_event_scraper import get_latest_events
from stadt_ku_scraper import get_latest_events_2


engine = create_engine('sqlite:///events_db.sqlite')
Base.metadata.bind=engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

events = get_latest_events()
events2 = get_latest_events_2()



def levenshtein(s1, s2):
    if len(s1) < len(s2):
        return levenshtein(s2, s1)

    # len(s1) >= len(s2)
    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[
                             j + 1] + 1  # j+1 instead of j since previous_row and current_row are one character longer
            deletions = current_row[j] + 1  # than s2
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]

unique_events=[]
for ev in events:
    for i in range(0,len(events2)):
        if(levenshtein(ev,events2[i]) < 3):
            unique_events.append(ev)
    for j in range(0,len(events)):
        if((levenshtein(ev,events[i]) < 3)):
            unique_events.append(ev)


for event in unique_events:
    ev = session.query(Event).filter_by(identifier=event['identifier']).first()

    if not ev:
        session.add(Event(
            name=event['name'],
            location=event['location'],
            link=event['link'],
            short=event['short'],
            date=event['date'],
            source=event['source'],
            identifier=event['identifier']
        ))

    session.commit()
    session.close()
