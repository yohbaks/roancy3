from django.db import models
from django.utils.text import slugify
from django.dispatch import receiver
from django.db.models import signals
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.urls import reverse



# Create your models here.

#mao ni sya ang drop choice box na  mano mano
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
		('Maasin', 'Maasin')

)




#mao ni sya ang pag crate category model na name , sa frontend pag add og category
class Category(models.Model):
	name = models.CharField(max_length=50, blank=True, null=True)
	def __str__(self):
		return self.name


#the database tables is here

class Stock(models.Model):
	category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True)
	item_name = models.CharField(max_length=50, blank=True, null=True)
	quantity = models.IntegerField(default='0', blank=True, null=True)
	receive_quantity = models.IntegerField(default='0', blank=True, null=True)
	receive_by = models.CharField(max_length=50, blank=True, null=True)
	issue_quantity = models.IntegerField(default='0', blank=True, null=True)
	issue_by = models.CharField(max_length=50, blank=True, null=True,choices=issue_to_category)
	issue_to = models.CharField(max_length=50, blank=True, null=True, choices=issue_to_category)
	phone_number = models.CharField(max_length=50, blank=True, null=True)
	created_by = models.CharField(max_length=50, blank=True, null=True)
	reorder_level = models.IntegerField(default='0', blank=True, null=True)
	last_updated = models.DateTimeField(auto_now_add=False, auto_now=True)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
	price = models.IntegerField(default='0', blank=True, null=True)

	def __str__(self):
		return self.item_name


class All_Store(models.Model):
	name=models.CharField(max_length=100,blank=True,null=True,verbose_name='Store name',choices=issue_to_category)
	products=models.ManyToManyField(Stock,blank=True)
	slug=models.SlugField(unique=True, null=False, default='na')

	def get_absolute_url(self):
		return reverse('store', kwargs={'slug': self.slug})

	def __str__(self):
		return self.name

@receiver(signals.pre_save, sender=All_Store)
def populate_slug(sender, instance, **kwargs):
    instance.slug = slugify(instance.name)