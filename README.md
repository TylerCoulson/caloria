# Caloria

Caloria is a food and weight tracking application that helps users keep track of their daily caloric intake and monitor their weight.

## Features

- **Food Tracking**: Users can log their meals and track their daily caloric intake.
- **Weight Tracking**: Users can record and monitor their weight over time.
- **Goal Setting**: Users can set weight loss goals and track their progress.
- **Custom Food Creation**: Users can create and track custom foods with their own nutritional information.
- **Weight Prediction**: Users can predict their future weight based on their current weight and assumed calorie intake.

# Technologies Used

Caloria is built using the following technologies:

- Python: A powerful programming language used for the backend development of the application.
- FastAPI: A modern, fast (high-performance) web framework for building APIs with Python.
- HTMX: A JavaScript library that allows you to access and manipulate HTML content with ease, making your web application more interactive.
- SQLAlchemy: A Python library for working with databases.

## Web Version

A web version of Caloria is available at [food-track.fly.dev](https://food-track.fly.dev). 


## Installation

1. Clone the repository: `git clone https://github.com/TylerCoulson/caloria.git`\
2. Create a virtual environment: `python -m venv venv`
3. Install the required packages: `pip install -r requirements.txt`
4. Create a file named `.env` in the root directory of the project with the following content:

   ```plaintext
   DATABASE_URL=your_database_url_here
   SUPPRESS_EMAIL_SENDING=True if you don't want to send emails False otherwise
   ```
5. Create a file named `secrets.py` in the `auth` directory with the following content:

   ```python
   from app.config import settings
   secrets = {
       "SECRET_KEY": "your_secret_key_here"
        "EMAIL":{
            "MAIL_USERNAME": "your email name",
            "MAIL_PASSWORD": "your email password",
            "MAIL_FROM": "your email address",
            "MAIL_PORT": "your mail port",
            "MAIL_SERVER": "mail server",
            "MAIL_STARTTLS": True,
            "MAIL_SSL_TLS": False,
            "TEMPLATE_FOLDER": "app/templates",
            "SUPPRESS_SEND": settings.SURPRESS_EMAIL_SEND
        }
   }

6. Start the application: `python app/main.py`

## Usage

1. Sign up for a Caloria account or log in to your existing account.
2. Log your meals and track your daily caloric intake.
3. Record your weight and monitor your progress over time.
4. Set goals and track your progress towards achieving them.

## Contributing

Contributions are welcome! If you'd like to contribute to Caloria, please follow these steps:

1. Fork the repository.
2. Create a new branch: `git checkout -b feature/your-feature-name`
3. Make your changes and commit them: `git commit -m "Add your commit message"`
4. Push to the branch: `git push origin feature/your-feature-name`
5. Open a pull request.

## Contact

If you have any questions or suggestions, feel free to reach out to us at tecoulson92@gmail.com.