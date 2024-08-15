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
    This will install Flask, Flask-Login, Flask-SQLAlchemy, Flask-Migrate and all other libraries and packages.

## Running the Application

To run the server, execute the following command:

    ```
    & "C:\Users\MY PC\Documents\Projects\Flask\GroceryApp\env\Scripts\python.exe" "C:\Users\MY PC\Documents\Projects\Flask\GroceryApp\main.py"
    ```
    or
    ```
    python main.py
    ```
    after activating the virtual environment (env)

This will start the Flask application and make it accessible at `http://localhost:5000`.

## Troubleshooting

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
This will update the database schema based on the changes in the models.

Note: Ignore any warning messages during the migration process and proceed.

4. If you encounter any migration issues while using the development server after updating the `models.py` file, it is recommended to delete specific folders in your project's root directory to resolve the issues. 

Note: This will delete all the data in the database

Delete the following folders:

- `__pycache__`
- `instance`
- `migrations`

Please exercise caution when deleting these folders, as they contain important files related to migrations and database configurations.

After deleting the folders, you may need to recreate the database and perform the migration again.

It's essential to have a backup of your data before proceeding with any database-related actions.
