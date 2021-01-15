from django.contrib import admin
from .forms import StockCreateForm
from .models import All_Store

# Register your models here.

from .models import *
'''
class StockCreateAdmin(admin.ModelAdmin):
   list_display = ['category', 'item_name', 'quantity', 'issue_by']
   form = StockCreateForm

   #filter ni sa search
   list_filter = ['category']

   #(this is for search)
   search_fields = ['category', 'item_name']'''

#admin.site.register(Stock, StockCreateAdmin)
admin.site.register(Stock)
admin.site.register(Category)
admin.site.register(Shop_Record)
admin.site.register(All_Store)
admin.site.register(Transit_Record)
admin.site.register(Sold_Items)
admin.site.register(SubCategory)
admin.site.register(Date_Sale)
admin.site.register(Individual_Sold_Item)
