# Bibliometrics
*17/05/2023*

## 1. Connect to production db via `Adminer`

Run
```console
$ ssh -L 9081:localhost:9080 -N -f -l bibliometric bibliometric-dev.ethz.ch
```
and then visit [localhost:9081](http://localhost:9081/).

To access use values from the file `.env`

| | |
|-------|---------|
| **System**   | PostgreSQL          |
| **Server**   | `POSTGRES_SERVER`   |
| **Username** | `POSTGRES_USER`     |
| **Password** | `POSTGRES_PASSWORD` |
| **Database** | `POSTGRES_DB`       |



## 2. Drop and recreate the schema `bibliometrics_s1`

From the `Adminer`, run these SQL commands

```sql
DROP SCHEMA IF EXISTS bibliometrics_s1 CASCADE;

CREATE SCHEMA bibliometrics_s1;
```

## 3. Install everything we need

```console
$ python3 -m venv venv

$ source venv/bin/activate

$ pip install poetry

$ poetry install --with dev
```

## 4. Create and run the Scopus migration

Check that `libbiblio/db/migrations/versions` is empty, then

```console
$ poetry run alembic revision --autogenerate -m "scopus"
```

Now open the `.py` file inside that folder and remove every line of code that
refers to `Web of Science` (we will make another migration when starting the
WoS ingestion).

After that run
```console
$ poetry run alembic upgrade head
```

## Checks during ingestion

Inspect
```
while [[ 1 == 1 ]]; do date >> scopus_inspect; poetry run biblio scopus inspect >> scopus_inspect; sleep 300; done
```

Memory
```
while [[ 1 == 1 ]]; do date >> scopus_memory; ps -elf | grep 'scopus' | grep 'ingested' >> scopus_memory; sleep 150; done
```
