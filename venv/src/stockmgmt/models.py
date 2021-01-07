from django.db import models
from django.utils.text import slugify
from django.dispatch import receiver
from django.db.models import signals
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.urls import reverse
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import signals
import logging
import os
import traceback

# Create your models here.

# mao ni sya ang drop choice box na  mano mano
category_choice = (
    ('Furniture', 'Furniture'),
    ('IT Equipment', 'IT Equipment'),
    ('Phone', 'Phone'),
    ('Electronics', 'Electronics')
)
issue_to_category = (
    ('Cogon', 'Cogon'),
    ('Kanangga', 'kanangga'),
    ('Albuera', 'Albuera'),
    ('Maasin', 'Maasin'),
    ('BODEGA', 'BODEGA'),

)


# mao ni sya ang pag crate category model na name , sa frontend pag add og category
class Category(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.name


# the database tables is here
class All_Store(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True, verbose_name='Store name', choices=issue_to_category)

    slug = models.SlugField(unique=True, null=False, default='na')

    def get_absolute_url(self):
        return reverse('store', kwargs={'slug': self.slug})

    def __str__(self):
        return self.name


@receiver(signals.pre_save, sender=All_Store)
def populate_slug(sender, instance, **kwargs):
    instance.slug = slugify(instance.name)


class Stock(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True)
    item_name = models.CharField(max_length=50, blank=True, null=True)
    quantity = models.IntegerField(default='0', blank=True, null=True)
    receive_quantity = models.IntegerField(default='0', blank=True, null=True)
    receive_by = models.CharField(max_length=50, blank=True, null=True)
    issue_quantity = models.IntegerField(default='0', blank=True, null=True)
    issue_by = models.CharField(max_length=50, blank=True, null=True, choices=issue_to_category)
    issue_by_model = models.ForeignKey(All_Store, on_delete=models.CASCADE, blank=True, null=True,
                                       related_name='issue_to_model')
    ordered_items=models.IntegerField(blank=True, null=True,default=0)
    issue_to = models.CharField(max_length=50, blank=True, null=True, choices=issue_to_category)
    issue_to_model = models.ForeignKey(All_Store, on_delete=models.CASCADE, blank=True, null=True,
                                       related_name='issue_by_model')
    phone_number = models.CharField(max_length=50, blank=True, null=True)
    created_by = models.CharField(max_length=50, blank=True, null=True)
    reorder_level = models.IntegerField(default='0', blank=True, null=True)
    last_updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    price = models.IntegerField(default='0', blank=True, null=True)

    def __str__(self):
        return self.item_name

    def save(self, *args, **kwargs):
        issue_by_shop = All_Store.objects.get(name__iexact='BODEGA')
        print(self.issue_by)
        print(self.issue_to)
        try:
            issue_to_shop = All_Store.objects.get(name=self.issue_to)
        except:
            issue_to_shop = All_Store.objects.get(name='BODEGA')

        self.issue_by_model = issue_by_shop

        self.issue_to_model = issue_to_shop


        super(Stock, self).save(*args, **kwargs)

@receiver(post_save, sender=Stock)
def create_shop_record(sender, instance, created, **kwargs):
    if created:
        print(kwargs)
        print(instance)
        print(sender)
        shop_record = Shop_Record()
        shop_record.product=instance
        shop_record.store = instance.issue_to_model
        shop_record.remaining_items =0
        shop_record.save()




@receiver(signals.post_save, sender=Stock)
def populate_slug(sender, instance, **kwargs):
    pass


class Transit_Record(models.Model):
    store = models.ForeignKey(All_Store, blank=True, null=True, on_delete=models.CASCADE)
    product = models.ForeignKey(Stock, blank=True, null=True, on_delete=models.CASCADE)
    remaining_items = models.IntegerField(default=0)

    def __str__(self):
        return str(self.remaining_items) + ' ' + self.product.item_name + ' in ' + self.store.name + ' remaining'


class Shop_Record(models.Model):
    store = models.ForeignKey(All_Store, blank=True, null=True, on_delete=models.CASCADE)
    product = models.ForeignKey(Stock, blank=True, null=True, on_delete=models.CASCADE)
    remaining_items = models.IntegerField(default=0)

    def __str__(self):

        return str(self.remaining_items) + ' ' + self.product.item_name + ' in ' + self.store.name + ' remaining'


class Sold_Items(models.Model):
    store = models.ForeignKey(All_Store, blank=True, null=True, on_delete=models.CASCADE)
    product = models.ForeignKey(Stock, blank=True, null=True, on_delete=models.CASCADE)
    quantity = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.store.name + ' ' + self.product.item_name

    def save(self, *args, **kwargs):
        stock_item = Stock.objects.get(pk=self.product.pk)
        print(stock_item.issue_quantity)

        #stock_item.issue_quantity -= self.quantity
        print(stock_item.issue_quantity)
        stock_item.save()

        super(Sold_Items, self).save(*args, **kwargs)
