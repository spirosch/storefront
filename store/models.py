from datetime import datetime
import email
from enum import _auto_null
from http.client import PAYMENT_REQUIRED
from itertools import product
from math import prod
from pickle import TRUE
from pyexpat import model
from tkinter import CASCADE
from turtle import title
from django.db import models
from django.forms import DateTimeField

# Create your models here.

class Promotion(models.Model):
    description = models.CharField(max_length=255)
    discount = models.FloatField()


class Collection(models.Model):
    title = models.CharField(max_length=255)
    # we define this class before Product class so we can reference it next.
    # if we can define this class above the reference class then we can reference this class with strings 
    #  collection = models.ForeignKey('Collection', on_delete=models.PROTECT)
    featured_product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True, related_name='+')
    # εδώ βάλαμε το Product σε εισαγωγικά γιατί δεν έχουμε δηλώσει ακόμα την κλάση Product (δεν είναι από πάνω)
    # επειδή όμως στην κλάση Product από κάτω έχουμε δηλώσει την κλάση Collection πρέπει να βάλουμε τα εισαγωγικά εδώ
    # γιατί δεν γίνεται και οι δύο κλάσεις να είναι από κάτω.
    # επίσης με το related_name='+' λέμε στην Django να μην δημιουργήσει την αυτόματη συσχέτιση που δημιουργεί

class Product(models.Model):
  # sku = models.CharField(max_length=10, primary_key=True) 
  # --> if we don't use the automatic ID generate that Django provides
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    description = models.TextField()
    # Textfield doesn't have any required arguments (max_lenth etc.)
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    # use DecimalField (δεκαδικός) για τις τιμές. Don't use float because they have round issues.
    # DecimalField has 2 required arguments. For example if we want to have 9999.99
    # that's 6 digits and 2 digits after decimal point
    invetory = models.IntegerField()
    last_update = models.DateTimeField(auto_now=True)
    # auto_now=True --> every time we update a product object,
    #  Django automatically stores the current date time in this field
    #  also we have auto_now_add=True --> with this only the first time we create
    # a product object (Class Products), Django stores the current date time here.
    collection = models.ForeignKey(Collection, on_delete=models.PROTECT)
    # on_delete=models.PROTECT --> if you accidentaly delete a Collection, we don't end up deleting all the products
    # in that collection
    promotions = models.ManyToManyField(Promotion)

class Customer(models.Model):
    MEMBERSHIP_BRONZE = 'B'
    MEMBERSHIP_SILVER = 'S'
    MEMBERSHIP_GOLD = 'G'
    

    MEMBERSHIP_CHOICES = [
        (MEMBERSHIP_BRONZE,'Bronze'),
        (MEMBERSHIP_SILVER,'Silver'),
        (MEMBERSHIP_GOLD,'Gold')
    ]
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    # unique=True so don't end up with duplicate emails.
    phone = models.CharField(max_length=255)
    birth_date = models.DateField(null=True)
    # models.DateField(null=True) --> so this field is nullable
    membership = models.CharField(max_length=1, choices=MEMBERSHIP_CHOICES, default=MEMBERSHIP_BRONZE) 
    # B for Bronze, S for Silver and G for Gold
    
    class Meta:
        db_table = 'store_customers'
        indexes = [
            models.Index(fields=['last_name', 'first_name'])
            # we use indexes to speed up our queries.
        ]


class Order(models.Model):
    PAYMENT_STATUS_PENDING = 'P'
    PAYMENT_STATUS_COMPLETE = 'C'
    PAYMENT_STATUS_FAILED = 'F'
    
    PAYMENT_STATUS_CHOICES = [
        (PAYMENT_STATUS_PENDING, 'Pending'),
        (PAYMENT_STATUS_COMPLETE, 'Complete'),
        (PAYMENT_STATUS_FAILED, 'Failed')
    ]    
    placed_at = models.DateTimeField(auto_now_add=True)
    # with auto_now_add=True, Django automatically populates this field / when create a new order
    payment_status = models.CharField(max_length=1, choices=PAYMENT_STATUS_CHOICES, default=PAYMENT_STATUS_PENDING)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    # If accidentaly delete customer, we don't end up deleting orders.


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    product = models.ForeignKey(Product,on_delete=models.PROTECT)
    quantity = models.PositiveSmallIntegerField()
    # prevent negative values from getting stored in this field
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    # we define unit_price here also because we should always store the price of the product at the time it was ordered
    

# class Address(models.Model):
#     street = models.CharField(max_length=255)
#     city = models.CharField(max_length=255)
#     customer = models.OneToOneField(Customer,on_delete=models.CASCADE, primary_key=True)

    # on_delete the customers τότε Cascade (αλληλουχία) δηλαδή θα σβηστεί εκτός του customer και η διεύθυνση του και όλα
    # υπάρχει επίσης και το on_delete=models.SETT_NULL όπου σβήνει τον customer αλλά όχι τις διευθύνσεις και κάνει τον customer null
    # αλλά επειδή ο customer είναι CharField και δεν δέχεται null values δεν βγάζει νόημα. 
    # on_delete=models.SET_DEFAULT --> this field will be set with the default value
    # on_delete=models.SET_PROTECT --> with this we can prevent the deletion / if there is a child, we cannot delete the Parent
    # first we must delete the child.
    # primary_key=True --> if we don't set this, Django will create another field here called ID, so every address is going to have
    # an ID. And that means we're going to end up with a one to many relationship between customers and addresses, because we can have
    # many addresses with the same customer. But if we make this field the primary key, we can only have one addresses for each customer
    # because primary keys don't allow duplicate values.

class Address(models.Model):
    street = models.CharField(max_length=255)     
    city = models.CharField(max_length=255)
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    # for one to many relationship, we change the oneToOneField to ForeignKey, so we are telling 
    # Django that Customer is a foregin key in this table
    # next we need to remove primary_key=True because we need multiple address for this customer
    # / allow duplicate values in this column
    zip_code = models.CharField(max_length=255)

class Cart(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    # this field gets auto populated when we create a new Cart


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    # on delete a cart, delete it, we don't need it anymore, delete all the items automatically
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    # if we can delete a product, meaning if that product has never ordered before, then that product should be removed
    # for all the existing shopping carts as well.
    quantity = models.PositiveSmallIntegerField()
    # # prevent negative values from getting stored in this field
