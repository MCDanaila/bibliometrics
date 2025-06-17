We will describe here the preliminary steps to be taken in order to use Bibliometrics.

Prerequisites:

- `git`;
- `Python >= 3.8`;
- `Poetry >= 1.3` (see [here](https://python-poetry.org/docs/#installation)).

The first thing to do is to clone the GitLab repository:
```console
$ git clone git@sissource.ethz.ch:sis/bibliometrics.git
```

Then install the software with all its dependencies
```console
$ cd bibliometrics
$ poetry install
```
> If you want to install also the _development dependencies_, you need to run
> `poetry install --with dev`

We must now give Bibliometrics the address and credentials of the database.

To do so, simply create a copy of file `env_template` and call it `.env`
```console
$ cp env_template .env
```
This file defines the following environment variables
```console
DB_ENGINE
POSTGRES_USER
POSTGRES_PASSWORD
POSTGRES_SERVER
POSTGRES_PORT
POSTGRES_DB
```
If you want to use Bibliometrics on a local database (we will now see how to do this), you do not need to further edit the `.env` file.
Instead, to interact with other databases, you will need to manually edit it.
To get your credentials please contact:

- Teresa Kubacka (teresa.kubacka@library.ethz.ch)
- Matthew Baker (matthew.baker@id.ethz.ch)

---

## Local DB

Bibliometrics comes with the possibility to instantiate a local database to connect to, especially useful for development and testing purposes.
The database will be built inside a container, so it is necessary to install Docker (see [here](https://docs.docker.com/get-docker/)).

Now make sure you are in the root directory of the project
(where the `docker-compose.yaml` file is) and run

```console
$ docker compose up -d
```
> For some older versions of Docker you may need to type `docker-compose` and not `docker compose`

This will build two containers: a `Postgres` database and an `Adminer` database GUI. You can see them by running
```console
$ docker ps

CONTAINER ID   IMAGE             COMMAND                  CREATED          STATUS          PORTS                    NAMES
5f352fe27197   postgres:alpine   "docker-entrypoint.s…"   10 seconds ago   Up 10 seconds   0.0.0.0:5433->5432/tcp   bibliometrics_bibliodb_1
5290fa284f3f   adminer           "entrypoint.sh php -…"   10 seconds ago   Up 10 seconds   0.0.0.0:9080->8080/tcp   bibliometrics_adminer_1
```

At this point, the database knows nothing about our tables. To build them, we use the `Alembic` migration software (already installed with the `poetry install`)
```console
$ poetry run alembic upgrade head
```

Each time the code inside `libbiblio/db` is changed, it is necessary to review and upgrade the database before continuing
```console
$ poetry run alembic revision --autogenerate -m "<revision name>"
$ poetry run alembic upgrade head
```

To destroy the containers
```console
$ docker compose down
```
and also remove the volume associated with the DB container
```console
$ docker volume ls

DRIVER    VOLUME NAME
local     bibliometrics_bibliodb_volume

$ docker volume rm bibliometrics_bibliodb_volume
```

> **TIP:** if you mess things up and the database seems to stop working, do the following:
> <ol> <li>`docker compose down`</li><li>`docker volume rm bibliometrics_bibliodb_volume`</li><li>`rm libbiblio/db/migrations/versions/*py`</li><li>`docker compose up -d`</li><li>`poetry run alembic revision --autogenerate -m "choose a name"`</li><li>`poetry run alembic upgrade head`</li></ol>


## Local GUI

To access the Adminer GUI go to  [http://localhost:9080](http://localhost:9080).
You need to provide the following credentials

|  Login | |
| ---------  | -----------------------|
| System:    | `PostgreSQL`           |
| Server:    | `<BIBLIODB_NAME>:5432` |
| Username:  | `<POSTGRES_USER>`      |
| Password:  | `<POSTGRES_PASSWORD>`  |
| Database:  | `<POSTGRES_DB>`        |

where `<POSTGRES_USER>`, `<POSTGRES_PASSWORD>` and `<POSTGRES_DB>` are taken
from the `.env` file, and `<BIBLIODB_NAME>` is the last column of the `postgres`
row from the `docker ps` command

```console
$ docker ps

CONTAINER ID   IMAGE             COMMAND                  CREATED       STATUS       PORTS                    NAMES
5f352fe27197   postgres:alpine   "docker-entrypoint.s…"   2 hours ago   Up 2 hours   0.0.0.0:5433->5432/tcp   bibliometrics_bibliodb_1
5290fa284f3f   adminer           "entrypoint.sh php -…"   2 hours ago   Up 2 hours   0.0.0.0:9080->8080/tcp   bibliometrics_adminer_1
```
> In this example `<BIBLIODB_NAME>` is `bibliometrics_bibliodb_1`.
