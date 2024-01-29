# 💕 ECG Analyzer Service


ECG Analyzer is distributed, scalable, secure and containerized web application built on top of FastAPI and Celery.
For the sake of this challenge, it can be deployed locally with Docker Compose and provides a friendly API Documentation.



## Getting Started
The service has been designed with scalability in mind, that's why Celery is the core here.
FastAPI (with uvicorn workers) and Celery (with native worker approach) can be horizontally scaled whenever is needed.
At the same time the API level just enqueue the tasks in the Celery broker (RabbitMQ) and perform some basic DB transactions.
The business logic is decoupled from the API and attached to the Celery Workers (or RabbitMQ consumers), which are the responsible
for analyzing an ECG and performing the operations needed.

### Prerequisites

- [**Docker / Docker Compose**](https://www.docker.com/products/docker-desktop/)
- **.env file** (For good practices it has not been included in the repo but can be found [here](https://password.link/NpugQkj/#TU9II1kzaG4+QF8zdWwxJnFu))

### Services

| **Service Name**       | **Description**                                 |
|------------------------|-------------------------------------------------|
| **api**                | FastAPI service                                 |
| **analyzer**           | Celery service                                  |
| **rabbitmq**           | RabbitMQ service used as a broker within Celery |
| **redis**              | Redis service used as a backend within Celery   |
| **db**                 | PostgreSQL database service                     |
| **pgadmin (Optional)** | PGAdmin service (UI for PostgreSQL database)    |


### Proposed Architecture/Workflow for Production approach
![Workflow/Architecture](https://i.imgur.com/FlzXevl.png)


### SQL Tables and relationships
![SQL Tables](https://i.imgur.com/r7ODFPF.png)


### Running the application

Once all prerequisites are satisfied, navigate to the root directory of the project and run the following commands in order to deploy the services locally:

Building containers:
```bash
docker compose build
```
Running containers:
```bash
docker compose up
```

## API
ECG API has been designed with versioning pattern, so can easily be extended in the future with more functionalities.
Explore the API and its endpoints using OpenAPI and Redoc documentation:

- [http://localhost:8000/docs](http://localhost:8000/docs)
- [http://localhost:8000/redoc](http://localhost:8000/redoc)

The authentication type is Basic Authentication (username and password)

## Admin: Creating users

1. Authenticate as Admin with Basic Auth (credentials can be found on the `.env` file)
2. Perform a POST request to `/v1/admin/register_user` with the username and password to create.
3. This user can now perform ECG submissions and result retrievals.


## Analyzer core
Providing an Analyzer interface (Abstract Class) is key for supporting new analyzers in the future.
The interface and its implementation can be found on: `./src/analyzer.py`.

There are 2 implementations that could analyze signals and return the count of zero-crossings.



## Running the tests

```bash
pip install -r requirements-dev.txt
pytest ./tests
```
