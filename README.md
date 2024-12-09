### Commands Overview

The Makefile includes the following targets:

#### General Help

```shell
make help
```

Prints a list of all available Makefile commands along with a brief description of each.


#### Initialization

```shell
make init
```

Performs initial configurations to prepare the project for running. Specifically:

* Creates required directories: ./dags, ./logs, ./plugins, and ./config.
* Generates a .env file with the current user’s UID for Airflow configuration.
* Runs docker compose up airflow-init to initialize Airflow.

#### Project Management

```shell
make deep-clean
```

Removes all Docker containers, images, networks, and volumes associated with the project. Useful for resetting the environment.

```shell
make up
```

Launches the project by running docker compose up.

#### Code Quality

```shell
make lint
```

lint: Lints the project by:

* Running Black for code formatting.
* Running isort to sort imports.

#### How to Spin Up the Project

Ensure Prerequisites Are Installed:

* Docker and Docker Compose must be installed on your system.
* Optionally, ensure Python and required development tools (e.g., Black and isort) are installed if you plan to modify the code.

This will prepare the environment and initialize necessary configurations.

Start the Project:

```shell
make up
```

This will start the application using Docker Compose.

Once started, services will be available: 

* Airflow: localhost:8080
* Postgres: localhost:5432 

Use the Airflow UI to monitor and manually trigger DAGs. Example DAGs include:

setup_database: For creating the database schema.
setup_staging_area: For loading the json iot data.
load_dimensions: For data warehousing dimensions.
load_facts: For data warehousing facts. (WIP)
