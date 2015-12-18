from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


# class StockItem(models.Model):
#     sku = models.CharField(max_length=200)
#     size = models.IntegerField()
#     colour = models.CharField(max_length=1, choices=Colour_Choices)


class Brand(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name


class Product(models.Model):
    brand = models.ForeignKey(Brand)
    name = models.CharField(max_length=200)
    description = models.TextField()
    current_price = models.DecimalField(max_digits=8, decimal_places=2)

    # For optimal loading, images are stored on a CDN
    # So we introduce getters to find the path lower down
    # thumbnail_filename = models.CharField(max_length=200, default="")
    # image_filename = models.CharField(max_length=200, default="")

    image = models.FileField(
        editable=True
    )

    is_active = models.BooleanField(default=True)

    def __unicode__(self):
        return self.name

    # def get_thumbnail_url(self):
    #     return "{0}/{1}".format(settings.IMG_CDN, self.thumbnail_filename)
    #
    # def get_image_url(self):
    #     return "{0}/{1}".format(settings.IMG_CDN, self.image_filename)


class Order(models.Model):
    SIZES = (
        (u'S', u'Small'),
        (u'M', u'Medium'),
        (u'L', u'Large'),
        (u'XL', u'X-Large'),
    )

    customer = models.ForeignKey(User)

    # If you want to disable referential integrity when deleting products then add
    # to FK: blank=True, null=True, on_delete=models.SET_NULL
    product = models.ForeignKey(Product)

    size = models.CharField(max_length=2, choices=SIZES)
    price = models.DecimalField(max_digits=8, decimal_places=2)

    create_date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "{0}".format(self.customer.username)