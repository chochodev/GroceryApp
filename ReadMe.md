# GroceryApp

GroceryApp is a Flask-based application for managing and selling grocery.

## Installation

1. Create a virtual environment using the following command:
  ```
  python3 -m venv env
  ```
  or 
  ```
  python -m venv env
  ```

2. Activate the virtual environment:

- For Windows:
  In Powershell terminal of the root directory
  ```
  cd env
  Scripts\activate
  ```
  In Command Prompt terminal of the root directory
  ```
  env\Scripts\activate
  ```

- For macOS/Linux:

  ```
  source env/bin/activate
  ```

3. Install the required libraries by running the following command:

    ```
    pip install -r requirements.txt
    ```
    This will install Flask, Flask-Login, Flask-SQLAlchemy and Flask-Migrate.

## Running the Application

To run the server, execute the following command:

    ```
    & "C:\Users\MY PC\Documents\Projects\Flask\GroceryApp\env\Scripts\python.exe" "C:\Users\MY PC\Documents\Projects\Flask\GroceryApp\main.py"
    ```

This will start the Flask application and make it accessible at `http://localhost:5000`.

TROUBLESHOOTING

If you face any issues after editing the models.py file, you can use Flask-Migrate to update the database schema.

If you're using PowerShell, set the environment variable FLASK_APP using the following command:

bash
```
$env:FLASK_APP = "main"
```
Then, initialize the migration:

bash
```
flask db init
```
Next, generate an initial migration:

bash
```
flask db migrate -m "Initial migration"
```
Finally, apply the migration to update the database schema:

bash
```
flask db upgrade
```
This will update the database schema according to the changes made in the models.

License

This project is licensed under the [MIT License](LICENSE).
