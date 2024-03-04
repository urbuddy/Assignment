# Assignment: Marketplace REST Framework Web Application with Simple JWT Authentication

# To Run this Project follow below:

        mkvirtualenv authenv
        pip install -r requirements.txt
        python manage.py makemigrations
        python manage.py migrate
        python manage.py runserver

# Endpoints of Rest API Requests:

        ● POST /user/register/: Create a new user and get a new token.

        ● POST /user/login/: Log in with the existing user and get a new token.
    
        ● GET /products/: List of all Products.
    
        ● POST /products/add_for_sell/: Add new product for sell.

        ● POST /products/purchase/{product_id}/: Purchase product with its product id.
