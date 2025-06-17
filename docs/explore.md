In this section we show how to use Bibliometrics to interact with the content of the database.

We will use Python scripting, launched through Poetry to have all the necessary dependencies
```console
$ poetry run python

Python 3.10.5 (v3.10.5:f377153967, Jun  6 2022, 12:36:10) [Clang 13.0.0 (clang-1300.0.29.30)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>>
```

> We could also use `ipython` or `jupyter notebook`, the important thing is to use them through Poetry to have the dependencies available.

The following three lines are essential to begin any data exploration

```console
>>> from libbiblio.db.models import *

>>> from libbiblio.db.session import get_db

>>> db = next(get_db())
```

`db` is a Session object and it will allow us to connect to the database and make queries on it.

If, for example, we want to see all the publications of a ScopusAuthor whose name begins with `Y` we could ask
```console
>>> db.query(
        ScopusAuthor
    ).where(
        ScopusAuthor.wos_standard.startswith("Y")
    ).first().publications
```

Queries must be made according to the syntax of SQLAlchemy.
A very comprehensive guide to this can be found at [this link](https://docs.sqlalchemy.org/en/20/orm/queryguide/index.html).


> You may need to import other functions from sqlalchemy as needed, such as `in_`, `not_`, `func` or others, depending on the queries you want to make.
