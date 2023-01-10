# Flask Notes service
---------------------
This is a simple notes api using Python Flask and Postgresql.

N.B. Requires Docker to be installed and Python3

---

### Env variables
--------------------
```bash
export FLASK_APP=api
export FLASK_DEBUG=1
export APP_SETTINGS=Local
export SECRET_KEY=this-really-needs-to-be-changed
export DATABASE_URL=postgresql+psycopg2://loki:d0nt4get@localhost:5432/notes
export DATABASE_TEST_URL=postgresql+psycopg2://loki:d0nt4get@localhost:5432/notes-test

```

---

### Run the API
---------------
## In Docker containers
Start both the services (DB & API) with following commands
```bash
chmod +x create-test-db.sh
docker-compose build
docker-compose up -d
```
API will be available at ```localhost:8080/swagger```

## Locally
Start the DB in  container
```bash
docker-compose up -d postgres
```

and the API (DB is in the container)
```bash
docker-compose up -d postgres
python -m venv venv && . venv/bin/activate
pip install -r requirements/dev.txt
flask run -p 8080
```
then the API will be available at ```localhost:8080```
N.B. change the hostname ```postgres``` with ```localhost``` in both ENVs DATABASE_URL and DATABASE_URL_TEST
---

### Documentation
-----------------
The Swagger documentation is available @```localhost:<port>/swagger```

enter the db at 
```
psql postgresql://todos:d0nt4get@localhost:5432/todos
```
---

### Optimizations
-----------------
A more optimized setup with [uWSGI-NGINX](https://flask.palletsprojects.com/en/1.1.x/deploying/uwsgi/).

Standalone [WSGI Containers](https://flask.palletsprojects.com/en/1.1.x/deploying/wsgi-standalone/).
