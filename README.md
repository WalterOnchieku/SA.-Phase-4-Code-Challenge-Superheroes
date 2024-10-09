PHASE 4 CODE CHALLENGE
# Hero API

This project is a RESTful API built with Flask and SQLAlchemy to manage a collection of superheroes and their powers. It supports various operations such as creating, reading, updating, and deleting heroes and powers.

## Table of Contents

- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)

## Features

- Create, read, update, and delete heroes and their powers.
- Manage relationships between heroes and their powers using a many-to-many association.
- Simple JSON responses for easy integration with front-end applications.

## Technologies Used

- **Flask**: A lightweight web framework for Python.
- **Flask-SQLAlchemy**: SQLAlchemy support for Flask.
- **SQLite**: A lightweight disk-based database.
- **SQLAlchemy-Serializer**: A library for serializing SQLAlchemy models.
- **cURL**: A command-line tool for making API requests.

## Installation

To run this project locally, follow these steps:

1. Clone the repository:
    ```bash
    git clone git@github.com:WalterOnchieku/SA.-Phase-4-Code-Challenge-Superheroes.git
    cd hero-api
    ```

2. Create a virtual environment and activate it:
    ```bash
    python -m venv venv
    # On Windows
    venv\Scripts\activate
    # On macOS/Linux
    source venv/bin/activate
    ```

3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Run the application:
    ```bash
    python run.py
    ```

## Usage

Once the application is running, you can interact with the API using tools like Postman or cURL. The API runs on `http://localhost:5555`.

### Example cURL Requests

- **Get all heroes**:
    ```bash
    curl http://localhost:5555/heroes
    ```

- **Get a hero by ID**:
    ```bash
    curl http://localhost:5555/heroes/1
    ```

- **Get all powers**:
    ```bash
    curl http://localhost:5555/powers
    ```

- **Create a new HeroPower**:
    ```bash
    curl -X POST http://localhost:5555/hero_powers -H "Content-Type: application/json" -d '{"strength": "Average", "power_id": 1, "hero_id": 3}'
    ```

## API Endpoints

| Method | Endpoint             | Description                                    |
|--------|----------------------|------------------------------------------------|
| GET    | `/heroes`            | Get a list of all heroes                      |
| GET    | `/heroes/:id`        | Get a hero by ID                              |
| GET    | `/powers`            | Get a list of all powers                      |
| GET    | `/powers/:id`        | Get a power by ID                             |
| PATCH  | `/powers/:id`        | Update a power by ID                          |
| POST   | `/hero_powers`       | Create a new HeroPower                        |




