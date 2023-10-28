# Classroom

DRF API for classroom management

## Table of Contents

- [About](#about)
- [Features](#features)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [Warnings](#warnings)
- [Contributing](#contributing)
- [License](#license)

### About

This is a simple API for classroom management.
It provides endpoints for creating, updating, deleting and retrieving students, teachers and classrooms.

### Features

- CRUD operations for students, teachers and classrooms
- Searching and Ordering filters
- JWT Authentication
- Permissions for various operations
- Swagger and ReDoc documentation

### Getting Started

You will need Python 3.11+ and pip installed on your system.
By default, the project uses PostgreSQL as the database, so you will need to install and run a PostgreSQL server.
You can use any other database by changing the settings in `core/settings.py`.
However, note that the project uses full text search which is only available in PostgreSQL.
You can change other settings for JWT authentication, media files, etc. in `core/settings.py`.

Once you have the database running, follow the steps below to get started.


1. Clone the repo

```sh
git clone https://github.com/aabidk20/classroom
```

2. Create and activate a virtual environment

```sh
cd classroom
python3 -m venv venv
source venv/bin/activate
```

3. Install the dependencies

```sh
pip install -r requirements.txt
```

4. Run the migrations

```sh
python manage.py migrate
```

5. Create a superuser

```sh
python manage.py createsuperuser
```

6. Run the server

```sh
python manage.py runserver
```

The server will be running at `http://localhost:8000/`.


### Usage
The API documentation is available at `/api/schema/swagger-ui` and `/api/schema/redoc` endpoints.


### Warnings
- The default keys and secrets in `core/settings.py` are hardcoded for development purposes only.
- The default CORS settings in `core/settings.py` are not secure.


### Contributing

Contributions are always welcome!

### License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
