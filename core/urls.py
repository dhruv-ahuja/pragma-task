from django.urls import path

from . import views

urlpatterns = [
    path("orders/add", views.place_order, name="place_order"),
    path("products", views.get_products, name="get_products"),
    path("products/<int:product_id>", views.get_product, name="get_product"),
    path("products/add", views.add_product, name="add_product"),
    # product recommender view
    path(
        "products/recommend/<int:product_id>",
        views.recommend_products,
        name="recommend_products",
    ),
    # helper to populate products
    path("products/populate", views.populate_products, name="populate_products"),
    # helper to populate orders
    path("orders/populate", views.populate_orders, name="populate_orders"),
]
