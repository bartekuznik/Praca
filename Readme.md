# Design and implementation of a web application supporting the rental of medical equipment

## Table of Contents

1. [Project Overview](#project-overview)
2. [Technologies](#technologies)
3. [Architecture](#architecture)
4. [Installation](#installation)


## Project Overview

This project is a web application designed to make renting medical equipment easier. Users can rent and offer medical devices for rent. The app includes features for user account management, adding and managing equipment, renting equipment, and more.

## Technologies 

- **Python 3.8.1**
- **Django 3.2.8**
- **Bootstrap 4.3.1**
- **Django Crispy Forms 1.13.0**
- **Pillow  8.4.0**

## Architecture

The app follows the MVT (Model-View-Template) pattern:

- **Model: Defines the data structure and stores it in the SQLite database.**
- **View: Defines the logic of the app, handling user interactions and updating the database.**
- **Template: The front-end of the app, which shows the HTML and CSS content to the user.**

## Installation

To run the project locally, follow these steps:

1. Clone the repository:

```
git clone https://github.com/bartekuznik/Praca.git
```

2. Install the required dependencies:

```
pip install -r requirements.txt
```

3. Go to the project directory:

```
cd mysite
```

4. Run the server:

```
python manage.py runserver
```