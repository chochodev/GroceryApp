# What is Edenfresh

Edenfresh is a Flask-based e-commerce application for managing and selling grocery.
It has the functionalities of basic e-commerce website such as browsing products in the menu, searching for products, negotiating prices, adding products to cart, ordering for products...

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


## Usage

### Home Page

Starting with the home page, unauthenticated users (users that are not signed in) will see a bar with text and two call-to-action buttons to login or sign up. Unauthenticated users are limited to only accessing the home, menu, about us, terms of use pages, as well as the login and signup pages.

### Authentication (Login & Signup)

#### Log In

To log in, enter your account credentials (email and password) and click the login button. Upon successful login, you will be redirected to the home page with a flash message displaying the user's name. Logged-in users have access to additional pages depending on their user type (admin or customer).

#### Sign Up

If you don't have an account, you can create one by clicking the signup button. Fill out the signup form with the required information, and upon successful registration, you will be logged in and redirected to the home page with a flash message displaying the user's name. Signed-in users have access to more pages depending on their user type (admin or customer).

### Logged-in Users

#### Admin

An admin user has access to pages available to unauthenticated users, as well as admin-specific pages accessible through the admin link. The admin pages include:

- Dashboard
- Orders
- Customers
- Products

#### Dashboard

The dashboard provides basic information about the current database, including:

- Orders:
  - Pending Orders: Orders made by customers that are awaiting the admin's response.
  - Total Orders: The total number of orders made by all customers.

- Customers:
  - Active Customers: Customers who have placed at least one order.
  - Total Customers: The total number of signed-up users, including the admin.

- Products:
  - Selling Products: The total number of products included in at least one customer's order.
  - Total Products: The total number of products created by the admin.

#### Orders

The orders page has three nav buttons to toggle between:

- All orders:
  - This contains all the orders from the customer including the one still in cart.

- Unapproved orders:
  - This contains pending orders which the admin has to act on by clicking on the button underneath to either approve or reject the order.

- Approved orders:
  - This contains the order approved and to be delivered to the customers. This also contains their address.

#### Customers

The customer provides basic information about all the signed up customers including the admin.

## Products

The Products section displays a comprehensive list of available products, including basic information for each product. To edit a product, simply click on it, and you will be redirected to the edit-product page. From there, you can make the desired modifications to the product details and save the changes using the button located below the form.

### Creating New Products

To create a new product, click on the "New Product" button, which can be found on the product page. This action will redirect you to the product creation page, where you can enter all the necessary information for the new product. Once you have entered the details, save the product by following the prompts on the page.

#### Home

The last nav link "Home" is for redirecting the admin back to the home page.

#### Customer

A customer user has access to pages available to unauthenticated users, as well as customer-specific pages accessible through the customer link. The customer pages include:

- Cart
- Allergy
- Account

#### Cart

The cart page contains all the product selected from the menu page.

#### Allergy

The link to allergy page can be located in the footer section. It contains all the products added to the allergy list.

To add product in your allergy list, simply click on the delete icon on the product from the menu page.

You can remove products from the allergy list by clicking on the delete button below the product description.

#### Account

This is the account settings page where users can edited there account information.
Click on the save button below to update account information.

## Logging out

To logout, the user should click on the logout icon on the nav link or the logout link in the footer section, a message should flash indicating the logged out user's name and should be redirected to the login page.

## License

This project is licensed under the [MIT License](LICENSE).
