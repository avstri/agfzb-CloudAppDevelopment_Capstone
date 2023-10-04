from django.db import models
from django.utils.timezone import now

# Create your models here.
class CarMake(models.Model):
    name = models.CharField(max_length=20)
    origin_country = models.CharField(max_length=50)
    description = models.TextField(max_length=100)

    def __str__(self):
        return self.name

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


# <HINT> Create a plain Python class `CarDealer` to hold dealer data
# class CarDealer(models.Model):
#     def __str__(self):
#         return "car Dealer"

# # <HINT> Create a plain Python class `DealerReview` to hold review data
# class DealerReview(models.Model):
#     def __str__(self):
#         return "car Dealer Review"