from django.db import models
from django.contrib.auth.models import User


PUBLICITY_CHOICES = [
    ('public', 'Public'),
    ('private', 'Private')
]


class Formula(models.Model):
    name = models.CharField(max_length=50, null=True)
    value = models.TextField()
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)


class Variable(models.Model):
    value = models.TextField()
    name = models.CharField(max_length=50)
    formula = models.ForeignKey(Formula, on_delete=models.CASCADE)