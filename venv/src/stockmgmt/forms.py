from django import forms
from .models import Stock

#add form ni siya
class StockCreateForm(forms.ModelForm):
   class Meta:
     model = Stock
     fields = ['category', 'item_name', 'quantity']

#validation ni siya sa mag duplicate (code ni siaya sa duplication og this field is required)
   def clean_category(self):
       server = self.cleaned_data.get('category')
       if not server:
           raise forms.ValidationError('This field is required')
#       for instance in Stock.objects.all():
#           if instance.category == server:
#              raise forms.ValidationError(str(server) + ' is already created')
       return server

   def clean_item_name(self):
       item_name = self.cleaned_data.get('item_name')
       if not item_name:
           raise forms.ValidationError('This field is required')
       for instance in Stock.objects.all():
           if instance.item_name == item_name:
              raise forms.ValidationError(str(item_name) + ' is already created')
       return item_name
#dira ra kutob

#search form ni siya
class StockSearchForm(forms.ModelForm):
    export_to_CSV = forms.BooleanField(required=False) # code ni siya sa pag export sa excel
    class Meta:
     model = Stock
     fields = ['category', 'item_name']

#update form ni siya
class StockUpdateForm(forms.ModelForm):
	class Meta:
		model = Stock
		fields = ['category', 'item_name']


#form for issueform
class IssueForm(forms.ModelForm):
	class Meta:
		model = Stock
		fields = ['issue_quantity', 'issue_to']

#form for receive form
class ReceiveForm(forms.ModelForm):
	class Meta:
		model = Stock
		fields = ['receive_quantity']


#form for reorder form
class ReorderLevelForm(forms.ModelForm):
	class Meta:
		model = Stock
		fields = ['reorder_level']

