import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nettunes.settings")

import django
django.setup()

from catalog.models import Record
from django.contrib.auth.models import User

record_data = [('Abbey Road',3,3),('Nevermind',2,2),('Purple Rain',2,2), ('Thriller',2,2), ('The Dark Side of the Moon',1,1), \
           ('The Wall',2,2),('The Slim Shady LP',1,1),('Lemonade',1,1),('21',1,1),('Scorpion',1,1), \
           ('My Beautiful Dark Twisted Fantasy',2,2), ('Fantasia',1,1)]

for entry in record_data:
    title = entry[0]
    owned = entry[1]
    available = entry[2]
    record = Record(name=title, num_owned=owned, num_available=available)
    record.save()

