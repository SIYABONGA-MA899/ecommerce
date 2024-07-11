from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Customer(models.Model):

    user = models.OneToOneField(User, null = True, blank =  True, on_delete= models.CASCADE)
    name = models.CharField(max_length= 30, null = False, blank=False)
    email = models.CharField(max_length = 200,  null=False, blank = False)

    def __str__(self):

        return(self.name)

class Product(models.Model):

    name = models.CharField(max_length=30, blank  = False, null = False)
    price = models.FloatField(null = False, blank = False)
    sex = models.CharField(max_length=5, null = False, blank = False)
    kind = models.CharField(max_length=30, null = False, blank = False)
    image = models.ImageField(null = True, blank = True)

    def __str__(self):

        return(self.name)

    @property
    def imageURL(self):

        try:

            url = self.image.url

        except:

            url = ''

        return(url)

class Order(models.Model):

    customer = models.ForeignKey(Customer, null = True, blank = True, on_delete=models.SET_NULL)
    complete = models.BooleanField(default = False)
    order_date = models.DateTimeField(auto_now_add=True)
    transaction_id = models.CharField(max_length=100, null=True)

    @property
    def number_of_items(self):

        tot_items = 0
        items = self.orderitem_set.all()

        for item in items:

            tot_items += item.quantity

        return(tot_items)
    
    @property
    def cartTotal(self):
    
        total = 0
        items = self.orderitem_set.all()
    
        for item in items:

            total += item.itemTotal

        return(total)

class OrderItem(models.Model):

    order = models.ForeignKey(Order, on_delete=models.CASCADE, null  = True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null = True)
    quantity = models.IntegerField(default = 0, null = False, blank = False)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def itemTotal(self):

        total = self.product.price * self.quantity
        return(total)

class ShippingAddress(models.Model):

    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length  = 30, null = False, blank = False)
    country = models.CharField(max_length  = 30, null = False, blank = False)
    city = models.CharField(max_length  = 30, null = False, blank = False)
    zipcode = models.CharField(max_length=20, null = False, blank = False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):

        return(self.address) 




