from libbiblio.db.models import *
from libbiblio.db.session import get_db

db = next(get_db())

print("from libbiblio.db.models import *")
print("from libbiblio.db.session import get_db")
print("db = next(get_db())")
