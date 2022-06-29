from django.db import models

# Create your models here.

# one order can have many products
# one product can be in many orders
# eg, order 1 can have headphones and bread but order 2 can also have
# headphones and/or bread
# this means that there's a many to many relationship between the two models
# we'll need what's called a 'joining table' that handles these relations
# that stores records of combinations of the 2 tables
# https://dzone.com/articles/how-to-handle-a-many-to-many-relationship-in-datab


class Order(models.Model):
    date = models.DateTimeField(auto_now_add=True)

    def get_products_list(self):
        # retrieving all products added to the current order
        products = self.product_set.all()

        # get their names
        product_names = [item.name for item in products]
        return product_names

    def __str__(self):
        product_names = self.get_products_list()
        return f"order date: {self.date}, products: {product_names}"


class Product(models.Model):
    name = models.CharField(max_length=100, unique=True)
    category = models.CharField(max_length=100)
    cost = models.IntegerField(default=1)
    order = models.ManyToManyField(Order, through="OrderInfo")

    def __str__(self):
        return f"product name: {self.name}, category: {self.category}, \
cost: {self.cost}"


class OrderInfo(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    # I believe product quantity should be defined here, since Product
    # represents a Product in the inventory, like bread. Bread is bread,
    # whether its 1 loaf or many. We can't define quantity directly in its
    # Product model.
    # also, quantity further proves our point that one order can have many
    # of one particular product.
    product_quantity = models.IntegerField(default=1)

    class Meta:
        # disallows adding one product multiple times to an order
        unique_together = ("order", "product")

    def __str__(self):
        return f"{self.order}, {self.product}, quantity: \
{self.product_quantity}"
