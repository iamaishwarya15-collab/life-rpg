from django.db import models
from django.contrib.auth.models import User

class Character(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    level = models.IntegerField(default=1)
    xp = models.IntegerField(default=0)
    gold = models.IntegerField(default=0)

    strength = models.IntegerField(default=1)
    intelligence = models.IntegerField(default=1)
    wisdom = models.IntegerField(default=1)
    creativity = models.IntegerField(default=1)

    streak = models.IntegerField(default=0)
    last_completed_date = models.DateField(null=True, blank=True)

class Quest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=50)

    xp_reward = models.IntegerField(default=10)
    gold_reward = models.IntegerField(default=5)

    completed = models.BooleanField(default=False)

class ShopItem(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.IntegerField(default=10)


class InventoryItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(ShopItem, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

class Achievement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    unlocked = models.BooleanField(default=False)

    