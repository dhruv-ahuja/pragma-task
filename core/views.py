import collections
import json
from django.core import serializers

from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import Order, Product, OrderInfo
from . import helpers

# Create your views here.
@api_view(["POST"])
def place_order(request):
    """
    Places an order given the desired products and their quantities.
    """

    # steps to place an order: confirm all required products in db,
    # fetch the products and their quantities to order,
    # add each item in the order cart to the order
    # place order by saving it to db

    # fetching the products to be put into the order, by looking at the
    # request body's json data
    products_to_order = request.data["products"]

    # each product item is in the form of a tuple here, the first element is
    # the Product instance itself and the second is the required quantity
    order_cart: list(Product, int) = helpers.fetch_products_from_db(products_to_order)

    if not order_cart:
        # we return a 404 or resource not found if any of the desired items
        # is not found in the database
        Response.status_code = 404
        message = {"message": "product(s) not found"}
        return Response(message)

    # now we have all the products to be ordered ready
    # we create a new order and use the 3rd table, our joining table, to
    # associate all the products with a single order item
    order = Order.objects.create()

    for item in order_cart:
        order_info = OrderInfo.objects.create(
            order=order, product=item[0], product_quantity=item[1]
        )
        order_info.save()

    order.save()

    # we send the 201 status code indicating that the resource has been created
    Response.status_code = 201
    # returning an empty response because I think an empty response is better
    # than no response, will also help know that everything went correctly
    return Response({})


@api_view(["POST"])
def add_product(request):
    """
    Add a product to the database.
    """
    product_name = request.data["name"]
    product_category = request.data["category"]

    # ensure product doesn't already exist
    if Product.objects.filter(name=product_name).exists():
        # from what I could find, a resource conflict should be addressed
        # with a 409 or "conflict"
        Response.status_code = 409
        message = {"message": "product already exists"}
        return Response(message)

    Product.objects.create(name=product_name, category=product_category)

    Response.status_code = 201
    return Response({})


@api_view(["GET"])
def get_product(request, product_id):
    """
    Get a product from the database given its ID.
    """

    fetch_product = Product.objects.filter(pk=product_id)

    if not fetch_product.exists():
        Response.status_code = 404
        message = {"message": "product not found"}
        return Response(message)

    product_json = serializers.serialize("json", fetch_product)
    message = {"data": product_json}
    return Response(message)


@api_view(["GET"])
def get_products(request):
    """
    Get all products from the database.
    """

    products = Product.objects.all()
    products_json = serializers.serialize("json", products)
    message = {"data": products_json}
    return Response(message)


@api_view(["GET"])
def recommend_products(request, product_id):
    """
    Get similar product recommendations for a product given its ID.
    """

    fetch_product = Product.objects.filter(pk=product_id)

    if not fetch_product.exists():
        Response.status_code = 404
        message = {"message": "product not found"}
        return Response(message)

    product = fetch_product[0]

    # fetch all orders that contain the product
    orders_with_product = Order.objects.filter(product__name=product.name)

    product_frequency = collections.defaultdict(int)

    # we need to make a frequency dict calculating products frequently paired
    # with the given product
    # for each order containing the target product, we fetch a list of all the
    # products in that order and add them to the frequency dictionary
    # this will tell us what is bought frequently with that product
    for order in orders_with_product:
        products = order.product_set.all()

        for item in products:
            # we dont want to add the target product itself to the
            # frequency dict
            if item != product:
                product_frequency[item.pk] += 1

    # making a list of the product ids
    # the most frequently matched items will be recommended first
    # sorting the frequency dict such that the most frequently grouped together
    # items appear first
    most_frequent_groupings = dict(
        sorted(product_frequency.items(), key=lambda item: item[1], reverse=True)
    )

    product_ids = [product_id for product_id in most_frequent_groupings.keys()]

    message = {"data": product_ids}
    print(product_ids)
    recommended_products = json.dumps(message)

    return Response(recommended_products)


# now, the views to populate products and orders for testing,
# these act as the scripts required by the task
@api_view(["GET"])
def populate_products(request):
    """
    Populate the database with pre-defined products.
    """

    helpers.populate_products()
    return Response({})


@api_view(["GET"])
def populate_orders(request):
    """
    Populate the database with random orders.
    """

    helpers.populate_orders()
    return Response({})
