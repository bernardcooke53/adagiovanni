# Adagiovanni

<p align="center">
<img alt="GitHub release (latest by date including pre-releases)" src="https://img.shields.io/github/v/release/bernardcooke53/adagiovanni?display_name=tag&include_prereleases">
<a href="https://github.com/psf/black/actions"><img alt="Actions Status" src="https://github.com/psf/black/workflows/Test/badge.svg"></a>
<a href="https://black.readthedocs.io/en/stable/?badge=stable"><img alt="Documentation Status" src="https://readthedocs.org/projects/black/badge/?version=stable"></a>
<a href="https://github.com/bernardcooke53/adagiovanni/blob/main/LICENSE"><img alt="License: MIT" src="https://black.readthedocs.io/en/stable/_static/license.svg"></a>
<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
<a href="https://mypy.readthedocs.io/en/stable/index.html"><img src="http://www.mypy-lang.org/static/mypy_badge.svg" alt="Checked with mypy"></a>
<a href="https://flake8.pycqa.org/en/latest/?badge=latest"><img alt="Documentation Status" src="https://readthedocs.org/projects/flake8/badge/?version=latest"></a>
</p>

---
A RESTful backend application for Giovanni to collect sandwich orders
from his customers, and to see his schedule. The API runs atop a Mongo
database, which the included docker compose file will create in a
container.

## Why "adagiovanni"?
An app for Giovanni, written on top of [FastAPI](https://fastapi.tiangolo.com/) -
it rolls off of the tongue easier than "allegriovanni"!

## Application Requirements
Giovanni has sent us some notes in an email:
> “Each handmade sandwich takes me 2½ minutes to make.
> It then takes me 1 minute to serve the sandwich and take payment.
> I take a break when there aren’t any orders to make or serve.”  

The schedule must contain the sequence number, time, task, and recipient.
For example, if Giovanni has three sandwich orders to prepare,
the schedule should include information along these lines: 

1. 00:00 Make sandwich for Stavros
2. 02:30 Serve sandwich for Stavros
3. 03:30 Make sandwich for Anisa
4. 06:00 Serve sandwich for Anisa
5. 07:00 Make sandwich for Adeel
6. 09:30 Serve sandwich for Adeel
7. 10:30 Take a break. 

### Assumptions
There is no UI currently required though this would help bring the product to life. The MVP is purely a
backend REST API, and Giovanni has picked up enough knowledge from the software developers that he serves
coffee and lunch to to be an adept enough user of `cURL` and Python's `requests` library; this will allow
him to work with this early demo.

The MVP for the product needs to accept sandwich orders and list outstanding tasks for Giovanni.
Another assumption is that Giovanni stocks certain ingredients for a fixed choice of sandwiches on the menu,
and that customers can choose from any of the available sandwiches. A sample of common sandwich choices is
included, but that may need to be customised by Giovanni at a later date.

The MVP doesn't include any scope for customization of sandwich orders.
The MVP doesn't allow customers to edit or cancel their order after submission!
The MVP makes Giovanni's schedule public - if Giovanni wants to put his schedule into an admin portal,
this can be added in later.

Based on Giovanni's input, customers will place their order for pickup ASAP and the schedule will reflect
the earliest time it can be served on a first-come, first-served basis. This means if Stavros places his order
now, and Anisa 10 seconds later, Stavros' order will be added to the schedule immediately for pickup in 2.5 minutes.
Anisa's order will be added to the schedule for pickup 3.5 minutes after Stavros' is scheduled for service, to allow
Giovanni time to serve and take payment for Stavros' order, and prepare Anisa's.

Customers will pay in-person upon service of their sandwich, and through separate software (this app doesn't have any payment
integration!).

## Running the application
If you are just interested in seeing the application working,
you will need to install [Docker](https://docs.docker.com/) and [`docker-compose`](https://github.com/docker/compose).
This app has been developed and tested with:

* Python 3.8.10
* Docker version 20.10.12, build e91ed57
* docker-compose v2.2.3
* Ubuntu 20.04 (LTS)

On Debian/Ubuntu, you can run
```bash
sudo apt install docker
```
to install Docker, and then go to https://github.com/docker/compose
for installation instructions for `docker-compose`.

You can then run the application by opening a terminal and running
```bash
docker compose up -d --build
```

Navigate to `http://localhost:8000/` to confirm the application is running.

## Usage/API
As the application is built on top of FastAPI, the Swagger UI is an excellent
location to view the API documentation and get an indication of its usage.
Since there may be a frontend added at a later date, the usual `/docs` route
has been moved to `/api/v1/docs` - if running locally following the above
instructions, go to `http://localhost:8000/api/v1/docs`.

You can visit `/orders` to get a list of the orders currently submitted,
and `/schedule` to see Giovanni's schedule.

Using a client of your choice, you can send a POST request to `/orders`
to submit a new order - the request body should identify you in the
`customer_name` field, and the sandwich you'd like to order in the
`/sandwich` field.

The orders you submit are persistent in the Mongo database, so even if
you shut down the application with
```bash
docker compose down
```
you can still restart at a later date, and the orders will be loaded back
into the application. Since this application is just a demonstration,
there is no delete functionality and the database is shared with the
integration tests; however the data is stored in a docker volume called
`adagiovanni_db`, so if you want to reset the demo application, you can
find the volume in your list of Docker volumes with
```bash
docker volume ls
```
and remove the database volume with
```bash
docker volume rm adagiovanni_db
```

## Running tests
Testing is run via [pytest](https://docs.pytest.org/en/7.0.x/),
which you can install via pip. It's recommended if you do this
outside of a virtual environment to install using the provided
`dev-requirements.txt` file as a constraint; this way your version
of pytest will match the one used to develop the tests:
```bash
pip install pytest -c dev-requirements.txt
```

Once you have installed pytest, navigate to the project root. Here,
you can run unit tests by via:
```bash
pytest -k unit
```
or integration tests via
```bash
pytest -k integration
```
**Note:** in order to run the integration tests, you will need to start
the database with
```bash
docker compose up -d mongo
```

You can run all of the tests at once with
```bash
pytest
```

Alternatively, if you are using [poetry](https://python-poetry.org/), then you can simply run
```bash
poetry run pytest
```
for all tests, or specify the same additional options to run either
unit or integration tests. See the appendix for installing poetry.

## Installing the API from source
This package isn't currently yet available on PyPI, so if you would
like to install the API as a Python package, you can build one from the
source code.

This is easiest done with `poetry` - running
```bash
poetry build
```
will produce a source distribution (`sdist`) and a `wheel`. If you aren't
using poetry and prefer the traditional build route, then you can use
another excellent module called `build` from the project root as follows:
```bash
python3 -m pip install --upgrade build~=0.7.0
python3 -m pip build . --wheel
python3 -m pip install dist/adagiovanni-*.whl
```
It should also be possible to

## Developing
In order to develop the application, you will need to install Python3.8+.
It's recommended to use a virtual environment and install the dependencies
with
```bash
python3 -m pip install -r requirements.txt
python3 -m pip install -r dev-requirements.txt
```
**Note:** `uvicorn` is installed as one of these dependencies.
You can then run a development server via
```bash
uvicorn adagiovanni.main:app --host 0.0.0.0 --port 8000 --workers 1
```
or, for convenience you can also run
```bash
python3 start_server.py
```

If you are using poetry, you can run
```bash
poetry install --no-root
```
to install all development dependencies, and
```bash
poetry run adagiovanni
```
to start the application on a development server.

## Appendix: Installing poetry
On Debian/Ubuntu, this also requires `python3-venv` e.g.
```
sudo apt install python3.8-venv
```

Run the following command to install poetry:
```bash
curl -sSL https://install.python-poetry.org | python3 -
```
You will then need to tell poetry that this is a project
which it should manage by running the following command
from the root of the repository:
```bash
poetry init
```
