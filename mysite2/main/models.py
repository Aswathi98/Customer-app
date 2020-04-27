from django.db import models
from datetime import datetime

# Create your models here.
class Customer(models.Model):
    customer_name = models.CharField(max_length=200, default="Company Name")
    customer_content = models.TextField(null=True, blank=True)
    customer_published = models.DateTimeField("date published", default=datetime.now)
    customer_imageurl = models.CharField(max_length=200, default="static/main/images/no-image.jpg")
    customer_link = models.CharField(max_length=200, default="https://en.wikipedia.org/wiki/ConocoPhillips", null=True, blank=True)
    pol = models.FloatField(null=True,blank=True)
    sub = models.FloatField(null=True,blank=True)
    def __str__(self):
        return self.customer_name