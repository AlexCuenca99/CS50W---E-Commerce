from django.contrib.auth.models import AbstractUser
from django.db.models.deletion import CASCADE
from django.utils import timezone
from django.db import models


class User(AbstractUser):
    pass


class Category(models.Model):
    name = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.name


class AuctionList(models.Model):
    createdAt = models.DateTimeField(default=timezone.now)
    title = models.CharField(max_length=100, null=False)
    description = models.TextField(max_length=300, null=False)
    startingBid = models.DecimalField(max_digits=7, decimal_places=2)
    currentBid = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="listCategories")
    owner = models.ForeignKey(User, on_delete=models.PROTECT, related_name="listCreators")
    buyer = models.ForeignKey(User, null=True, blank=True, on_delete=models.PROTECT)
    isActive = models.BooleanField(default=True, null=False)
    interested = models.ManyToManyField(User, blank=True, related_name="listInterested")

    def __str__(self):
        return self.title


class Bid(models.Model):
    createdAt = models.DateTimeField(default=timezone.now)
    auctionList = models.ForeignKey(AuctionList, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=CASCADE)
    offer = models.DecimalField(max_digits=7, decimal_places=2)


class Comment(models.Model):
    createdAt = models.DateTimeField(default=timezone.now)
    title = models.CharField(max_length=100, null=False)
    content = models.TextField(max_length=300, null=False)
    user = models.ForeignKey(User, on_delete=CASCADE)
    auctionList = models.ForeignKey(AuctionList, on_delete=CASCADE, related_name="listComments")

    def __str__(self):
        return self.title


class Picture(models.Model):
    auctionList = models.ForeignKey(AuctionList, on_delete=CASCADE, related_name="listPictures")
    picture = models.ImageField(upload_to="images/")
    optText = models.CharField(max_length=50)
