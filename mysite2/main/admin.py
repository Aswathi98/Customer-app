from django.contrib import admin
from .models import Customer
from tinymce.widgets import TinyMCE
from django.db import models

# Register your models here.



class CustomerAdmin(admin.ModelAdmin):

    fieldsets = [
        ("Title/date", {'fields': ["customer_name", "customer_published"]}),
        ("image location", {'fields': ["customer_imageurl"]}),
        ("scrap url", {'fields': ["customer_link"]}),
        ("Content", {"fields": ["customer_content"]}),
        ("pol",{'fields':["pol"]}),
        ("sub",{'fields':["sub"]})
    ]

    formfield_overrides = {
        models.TextField: {'widget': TinyMCE()},
        }


admin.site.register(Customer,CustomerAdmin)
