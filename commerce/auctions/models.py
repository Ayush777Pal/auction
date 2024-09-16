from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):   #creates a user 
    pass

class house(models.Model):  # helss in select the house
    type=models.CharField(max_length=50)

    def __str__(self):
        return self.type

class Bid(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE, blank=True, related_name="userbid")
    bid=models.FloatField(default=0)

    def __str__(self):
        return f"{self.bid}"



class listing(models.Model):    # description of material to be putted in auction
    title=models.CharField(max_length=40)
    discription=models.CharField(max_length=40)
    imageurl=models.CharField(max_length=1000)
    price=models.ForeignKey(Bid, on_delete=models.CASCADE, blank=True, null=True, related_name="price")
    owner=models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    isactive=models.BooleanField(default=True)
    house=models.ForeignKey(house, on_delete=models.CASCADE, blank=True, null=True)
    watchlist=models.ManyToManyField(User, null=True, blank=True, related_name="listingwatch")

    def __str__(self):
        return self.title


class Comment(models.Model):
    author=models.ForeignKey(User, on_delete=models.CASCADE, blank=True, related_name="user")
    list=models.ForeignKey(listing, on_delete=models.CASCADE, related_name="listingsc")
    comment=models.CharField(max_length=300)

    def __str__(self):
        return f"{self.author} has commented on {self.list}"

    


