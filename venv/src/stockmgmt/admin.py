from django.contrib import admin
from .forms import StockCreateForm
# Register your models here.

from .models import *

class StockCreateAdmin(admin.ModelAdmin):
   list_display = ['category', 'item_name', 'quantity', 'issue_by']
   form = StockCreateForm

   #filter ni sa search
   list_filter = ['category']

   #(this is for search)
   search_fields = ['category', 'item_name']

admin.site.register(Stock, StockCreateAdmin)
admin.site.register(Category)
