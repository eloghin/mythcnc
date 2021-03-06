from decimal import Decimal
from django.conf import settings
from shop.models import Product, ProductImage

class Cart(object):
    def __init__(self, request):
        """
        Initialize the cart.
        """
        self.session = request.session  # store the current session to make it available to other methods of the Cart class
        cart = self.session.get(settings.CART_SESSION_ID) # initialize the cart with a request object
        if not cart:
            # save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart


    def add(self, product, quantity=1, override_quantity=False):
        """
        Add a product to the cart or update its quantity.
        """
        product_id = str(product.id)
        # picture = ProductImage.objects.filter(product=product.id).first()

        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0,
                                        'price': str(product.price),
                                        #'picture': picture
                                        }

        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity

        self.save()


    def save(self):
        # mark the session as "modified" to make sure it gets saved
        self.session.modified = True


    def remove(self, product):
        """
        Remove a product from the cart.
        """
        product_id = str(product.id)

        if product_id in self.cart:
            del self.cart[product_id]

        self.save()


    def __iter__(self):
        """
        Iterate over the items in the cart and get the products
        from the database (for views and templates)
        """
        product_ids = self.cart.keys()
        # get the product objects and add them to the cart
        products = Product.objects.filter(id__in=product_ids)

        cart = self.cart.copy()
        for product in products:
            picture = ProductImage.objects.filter(product=product.id).first()
            cart[str(product.id)]['product'] = product
            cart[str(product.id)]['picture'] = picture

        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item


    def __len__(self):
        """
        Count all items in the cart.
        """
        return sum(item['quantity'] for item in self.cart.values())


    def get_total_price(self):
        """
        calculate the total cost of the items in the cart.
        """
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())


    def clear(self):
        # remove cart from session
        del self.session[settings.CART_SESSION_ID]
        self.save()
