# Movie & Series Helper Telegram Bot

## Project Description
This is a Telegram bot designed to help users quickly find information about movies and TV series. It uses the TMDb API to fetch accurate data and allows users to save their favorite media

## Features
* **Search:** Find movies and TV shows by title using the TMDb database
* **Random Recommendation:** Get a random highly-rated movie or series
* **Favorites List:** Save media to a personal favorites list and remove them when needed
* **Interactive UI:** Uses Inline Keyboards to add items to favorites

## Technologies Used
* **Language:** Python 
* **Framework:** aiogram 3.x Async Telegram Bot API
* **API:** TMDb REST API (requests library)
* **Data Persistence:** JSON for local data storage
* **Concepts:** Object-Oriented Programming (Inheritance, Polymorphism), Decorators, Unit Testing

## Installation Instructions
1. Clone this repository to your local machine:
2. Install the required libraries by running:
   `pip install -r requirements.txt`
3. Open `main.py` and put your Telegram bot token in the `BOT_TOKEN` variable
4. Open `utils/tmdb_client.py` and replace the `API_KEY` string with your TMDb API key

## How to Run the Project
Open your terminal or command prompt, navigate to the project folder, and run:
`python main.py`
The bot will start polling and will be ready to receive commands in Telegram

## Screenshots

* Search Feature <img width="1272" height="977" alt="image" src="https://github.com/user-attachments/assets/374ae836-6070-4402-aa7d-52da540cbef2" />

* Random and Favorites <img width="817" height="930" alt="image" src="https://github.com/user-attachments/assets/6d21736b-25b9-4704-a516-2ee30aa1393c" />


## Developer
* **Amir:** Solo developer. Responsible for core logic, OOP structure, TMDb API integration, Telegram bot routing, state management, data persistence
