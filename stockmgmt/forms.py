from django import forms
from .models import Stock, SubCategory, Sold_Items, Date_Sale, Shop_Record
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

#add form ni siya

class SignUpForm(UserCreationForm):
    first_name=forms.CharField(max_length=30,required=True)
    last_name=forms.CharField(max_length=30,required=True)
    email=forms.EmailField(max_length=255,required=True)
    class Meta:
        model=User
        fields=['username','first_name','last_name','email','password1','password2',]


class StockCreateForm(forms.ModelForm):
   class Meta:
     model = Stock
     fields = ['category','sub_category', 'item_name', 'price']

   def __init__(self,*args,**kwargs):
       super(StockCreateForm, self).__init__(*args,**kwargs)
       self.fields['sub_category'].queryset=SubCategory.objects.none()
       if 'category' in self.data:
           try:
               category_id=int(self.data.get('category'))
               self.fields['sub_category'].queryset=SubCategory.objects.filter(category__id=category_id).order_by('name')
           except (ValueError, TypeError):
               pass
       elif self.instance.pk:
           self.fields['sub_category'].queryset=self.instance.category_set.order_by('name')

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

#fklsjdlfl
class StockSearchForm(forms.ModelForm):
    export_to_CSV = forms.BooleanField(required=False) # code ni siya sa pag export sa excel
    class Meta:
     model = Stock
     fields = ['category', 'item_name']

class AllSaleSearchForm(forms.Form):

    date = forms.DateField(
        input_formats=['%Y-%m-%d'],
        widget=forms.DateInput(attrs={
            'type':'date',
            'class':'form_input',
            'data-target':'#datetimepicker'
        })
    )
    class Meta:
        model=Date_Sale
        fields=['date']


#update form ni siya
class StockUpdateForm(forms.ModelForm):
	class Meta:
		model = Stock
		fields = ['category', 'item_name','price']


#form for issueform
class IssueForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super(IssueForm, self).__init__(*args,**kwargs)
        instance=getattr(self,'sub_category',None)
        self.fields['sub_category'].disabled=True
    class Meta:
        model = Stock
        fields = ['sub_category','issue_quantity', 'issue_to']


#form for receive form
class ReceiveForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super(ReceiveForm, self).__init__(*args,**kwargs)
        instance=getattr(self,'sub_category',None)
        self.fields['sub_category'].disabled=True
    class Meta:
        model = Stock
        fields = ['sub_category','receive_quantity']


#form for reorder form
class ReorderLevelForm(forms.ModelForm):
	class Meta:
		model = Stock
		fields = ['reorder_level']


class ShopReoderLevelForm(forms.ModelForm):
    class Meta:
        model=Shop_Record
        fields=['reoder_level']

