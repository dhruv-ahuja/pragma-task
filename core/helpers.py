# file to store helper funcs

import random

from .models import Order, Product, OrderInfo


def fetch_products_from_db(products_to_order: list) -> list:
    """
    Fetches the required products from the database.
    """

    # order_cart will store all the product instances as fetched from the db
    order_cart = []
    # django has lazy querying, meaning that items are only fetched if requested
    # for, thus saving resources
    all_products = Product.objects.all()

    # each product item is in the form of a list, the first element is the name
    # and the second is the required quantity
    for item in products_to_order:
        product = all_products.filter(name__contains=item[0])
        quantity = item[1]

        # we follow the all or nothing concept, either all items from the order
        # exist in the db and we process the order, or we do not
        if not product.exists():
            return []

        # we have to get the object inside the queryset
        product = product[0]
        order_cart.append((product, quantity))

    return order_cart


def fetch_products_in_order(order_id: int) -> list:
    """
    Fetches Products in an order given order ID.
    """

    products = []

    # we dont have to worry about verifying whether
    order = Order.objects.get(pk=order_id)


def get_products():
    """
    Returns a list of pre-defined products.
    """

    products = [
        ("computer", "electronics"),
        ("laptop", "electronics"),
        ("monitor", "electronics"),
        ("speakers", "audio"),
        ("headphones", "audio"),
        ("eggs", "food"),
        ("rice", "food"),
        ("bread", "food"),
        ("milk", "food"),
        ("wheat", "food"),
        ("oats", "food"),
        ("notebook", "stationery"),
        ("pen", "stationery"),
        ("pencil", "stationery"),
        ("shampoo", "bathing"),
        ("soap", "bathing"),
        ("conditioner", "bathing"),
        ("curtains", "decor"),
        ("chair", "decor"),
    ]

    return products


def populate_products() -> None:
    """
    Populates the database with products.
    """

    products = get_products()

    for product in products:
        Product.objects.create(name=product[0], category=product[1])


def populate_orders() -> None:
    """
    Populates the database with orders.
    """

    products = get_products()

    # we generate a random no. of products to add to the order
    product_count = random.randint(1, 10)

    # now, we are generating the products to pick from the products list
    # so, we pick out n random items from the list, whom we will add
    # to the order, where n is the random generated int
    # so if n = 2, we will pick any 2 random products from the list
    # sample products_to_pick = [2,12,8,6]
    products_to_pick = random.sample(range(0, len(products)), product_count)

    for _ in range(20):
        # creating an order, now we loop over the products to
        # pick and add them all to this one order
        order = Order.objects.create()
        for index in products_to_pick:
            # first we get the name of the product from the pre-defined list
            item = products[index]
            # now we fetch the actual Product models' instance from the db
            # so that we can add it to the order
            # item is a tuple with product name and its category
            product = Product.objects.get(name=item[0])

            # generating a random quantity for the product
            quantity = random.randint(1, 10)

            order_info = OrderInfo.objects.create(
                order=order, product=product, product_quantity=quantity
            )
            order_info.save()
