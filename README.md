## How to run the project

1. clone the project locally

2. create a new virtual environment and activate it

3. run `pip install -r requirements.txt`

4. run `python manage.py migrate`

5. run `python manage.py runserver` and the server will be live

6. to populate the products and orders table, please make `GET` requests to `products/populate` and `orders/populate` viewpoints in that order


## Endpoints

`/orders/populate` -> populate the DB with `n` random orders, `n` in range of (1, 10)
`/orders/add` -> make a new order 

`/products/populate` -> populate the DB with pre-defined products
`/products/add` -> add a product to the DB
`/products` -> get all products 
`/products/<int:product_id>` -> get a particular product

`products/recommend/<int:product_id>` -> get product recommendations by entering a product id 


## Recommendation System

The product recommendation system looks at all the products that have been bought together with the target product and orders them by most frequently purchased together to least frequently purchased together items. The response contains a list and the first item in the list is the one most frequenty purchased with the product and the last item the least frequently purchased item. 
