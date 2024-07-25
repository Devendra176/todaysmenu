# TodayMenu Application

TodayMenu is a FastAPI-based application that allows restaurants to register, add their menus, and set today's menu. Customers can see a list of restaurants nearby up to 5 km with today's menu.

## Features

- Restaurant registration
- Add and manage menus
- Set today's menu
- Find restaurants nearby up to 5 km
- View today's menu for nearby restaurants

## Technologies Used

- FastAPI
- SQLAlchemy
- PostgreSQL (or any other supported database)
- CI/CD for automated deployments

## Requirements

- Python 3.10+
- PostgreSQL (or another database)
- FastAPI
- SQLAlchemy
- Uvicorn (for running the application)

## Setup

### Clone the repository

```bash
https://github.com/Devendra176/todaysmenu.git
cd todaymenu
```

### Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```
### Set up the database
- Create a PostgreSQL database.
- Update the database URL in your environment variables or 'settings.py'.

### Run database migrations
```bash
alembic upgrade head
```
### Start the application
```bash
uvicorn app.main:app --reload
```
