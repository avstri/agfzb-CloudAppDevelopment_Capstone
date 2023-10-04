from django.db import models
from django.utils.timezone import now

# Create your models here.
class CarMake(models.Model):
    name = models.CharField(max_length=20)
    origin_country = models.CharField(max_length=50)
    description = models.TextField(max_length=100)

    def __str__(self):
        return f"{self.name}"

class CarModel(models.Model):
    SEDAN = 'Sedan'
    WAGON = 'Wagon'
    SUV = 'SUV'
    COUPE = 'Coupe'
    MINIVAN = 'MiniVan'
    TRUCK = 'Truck'

    CAR_TYPE_CHOICES = [
        (SEDAN, 'Sedan'),
        (WAGON, 'Wagon'),
        (SUV, 'SUV'),
        (COUPE, 'Coupe'),
        (MINIVAN, 'MiniVan'),
        (TRUCK, 'Truck')
    ]

    name = models.CharField(max_length=20)
    make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    car_type = models.CharField(
        null = False,
        max_length=20,
        choices = CAR_TYPE_CHOICES,
        default = SEDAN)
    year = models.DateField(null = False)
    dealerId = models.IntegerField(null = True)

    def __str__(self):
        return f"{self.make} {self.name} {self.year}"

class CarDealer:

    def __init__(self, address, city, full_name, id, lat, long, short_name, st, zip):
        # Dealer address
        self.address = address
        # Dealer city
        self.city = city
        # Dealer Full Name
        self.full_name = full_name
        # Dealer id
        self.id = id
        # Location lat
        self.lat = lat
        # Location long
        self.long = long
        # Dealer short name
        self.short_name = short_name
        # Dealer state
        self.st = st
        # Dealer zip
        self.zip = zip

    def __str__(self):
        return "Dealer name: " + self.full_name

class DealerReview(models.Model):
    def __init__(self, dealership, name, purchase, review, purchase_date, 
        car_make, car_model, car_year, id):
        self.dealership=dealership
        self.name=name
        self.purchase=purchase
        self.review=review
        self.purchase_date=purchase_date
        self.car_make = car_make
        self.car_model = car_model
        self.car_year = car_year
        self.id = id

    def __str__(self):
        return f"Dealer rewview: {self.name}"
