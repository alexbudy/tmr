# Track-My-Run webapp

A Flask based, [HTMX](https://htmx.org/) powered web application used for tracking and managing personal aerobic runs. 

The live version of this site can be found on [www.track-my-run.com](https://www.track-my-run.com)

## Table of Contents

- [Purpose](#purpose)
- [Local Installation](#local-installation)
- [Migrations, Tests, and Scripts](#migrations-tests-and-scripts)
- [Future Improvements](#future-improvements)
- [Contributing](#contributing)

## Purpose

The primary purpose of this project is to get hands on experience with development and production-level deployment of a full-fledged modern-day web application, using a common web framework (Flask) and an interesting non-SPA front end JS libary (HTMX).

As such, all feedback is helpful and appreciated.

This application has all the common components of a web-application including:
- dockerized containers
- Postgres, Redis, session management with cookies, and authorization with salted passwords
- `.env` file for dev and prod setup
- SQLAlchemy ORM for database access
- Github Actions automated unit test runs on push, and one-click deployment to live site
- No JavaScript - Jinja templates generate HTMX which allow for custom tags to call the API with the full REST model, and replace target HTML elements 'under-the-hood'
- Some non-JS UI functionality, such as sortable columns

## Local Installation
Installation of the application for local experimentation and development requires some prerequisites:
- Python installed (I am using `3.12.3` as of this writing)
- Docker service up and running
- `docker-compose` command working

First, clone and `cd` the repository
```
git clone https://github.com/alexbudy/track-my-run.git
cd track-my-run
```
Take a look at the `.env.template` file - check/modify those values to your liking (the defaults should be ok for development) and then rename that file to `.env`. This is to prevent `.env` files to be committed as they can contain sensitive information.

Then, build and run the docker containers

```
docker-compose build
docker-compose up
```
Server should come up and you can access the server on `localhost:5000` (or `SERVER_PORT` value).
As long as your `FLASK_APP` environment variable is not `prod`, server/template code changes will be hot-reloaded on change and save.

## Migrations, Tests, and Scripts
Migration files are auto-generated by `Alembic` (more on that below).
To generate new migrations and run the unit test suite, you will need to create a virtual environment and install dependencies:
```
python -m venv venv
source venv/Scripts/activate (or source venv/bin/activate on unix machines)
pip install -r requirements.txt
```

#### Unit Tests

After activating your virtual environment, you can run
```
python -m pytest
```
from the root directory, which will discover and run all tests in the repo.

#### Migrations
You can make changes to the schema by modifying or creating new models in `app/models/models.py`

Then, create a new migration file with alembic:
```
alembic revision --autogenerate -m "Briefly describe changes here"
```
The file will be  be placed in `migrations/version`, prepended by a unique hash value.
Now the migrations need to be applied to the DB(s) - run
```
alembic --name dev upgrade head   # this applies to the dev DB
alembic --name test upgrade head  # this is for the test DB
```
There is also `--name prod` for the prod DB (and in fact configurations for the DBs can be made in `alembic.ini`).
Here are some other useful commands (picked from [this blog post](https://medium.com/@johnidouglasmarangon/using-migrations-in-python-sqlalchemy-with-alembic-docker-solution-bd79b219d6a#useful-commands:~:text=database%20were%20printed.-,Useful%20commands,-In%20this%20section)).
```
alembic upgrade head                            # apply all migrations
alembic downgrade base                          # revert all migrations
alembic downgrade -1                            # revert migration one by one
alembic upgrade +1                              # apply migration one by one
alembic downgrade base && alembic upgrade head  # reset the db
```

#### Scripts
The `scripts` directory holds automated scripts that can be used to perform various tasks, such as populate a database with dummy runs. Run the script from the root directory with 
```
PYTHONPATH=$(pwd) python scripts/generate_runs.py 3 --env dev # generate 100 runs for user with id 3 on the dev environment
```

## Future Improvements
Now that the framework for the application is in place, there can be many potential directions to take the application to work with new technologies and implement interesting features.
- A friend-based system where you can track/compare your runs with friends, send friend requests, and messages
- Implementation of [Cooper Aerobics](https://www.cooperaerobics.com/Downloads/About/Aerobics-Points-System.aspx) point based system for tracking aerobic points, with targets, goals, and automated notifications.
- A global weekly, monthly, and distance based leaderboard
- Profile/admin pages
- Addition of a JSON API to allow for SPA JS frameworks
- Extend unit testing
- Experiment with UI and various color schemes
- Add other activity types - swimming, biking, walking
- ...

The possibilities become endless 🚀

## Contributions
The primary purpose of this project as it stands is for self-educational purposes. As such, all contributions, suggestions, etc are welcome!

Feel free to contact the owner (me) at alexbudy@gmail.com.

Thanks for reading!
