from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.http import HttpResponse  # sa excel ni sya na import
from django.contrib import messages  # sa notifacation ni siya
import csv
from django.contrib.auth.decorators import login_required
@login_required


# Create your views here.
# home view ni sya bai
def home(request):
    title = 'Welcome to Roancy Application'
    all_store = All_Store.objects.all()

    context = {
        "title": title,
        'stores':all_store,
    }
    return render(request, "home.html", context)

def store(request,slug):
    store=All_Store.objects.get(slug=slug)
    this_store_items=store.products.all()
    context={
        'products':this_store_items,
    }
    template='cogon.html'
    return render(request,template,context)

# views sa pag search, please refer to the forms "StockSearchForm"
@login_required
def list_items(request):
    header = 'BODEGA STOCKS'
    form = StockSearchForm(request.POST or None)
    queryset = Stock.objects.all()
    context = {
        "header": header,
        "queryset": queryset,
        "form": form,
    }
    if request.method == 'POST':  # code ni siya if the search box is click
        queryset = Stock.objects.filter(  # category__icontains=form['category'].value(),
            item_name__icontains=form['item_name'].value()
        )
        if form['export_to_CSV'].value() == True:  # code ni siya if the select box excel is selected
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="List of stock.csv"'
            writer = csv.writer(response)
            writer.writerow(['CATEGORY', 'ITEM NAME', 'QUANTITY'])
            instance = queryset
            for stock in instance:
                writer.writerow([stock.category, stock.item_name, stock.quantity])
            return response

        context = {
            "form": form,
            "header": header,
            "queryset": queryset,
        }
    return render(request, "list_items.html", context)

# views sa pag add og item, please refer to the forms "StockCreateForm"
@login_required
def add_items(request):
    form = StockCreateForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Successfully Saved')
        return redirect('/list_items')
    context = {
        "form": form,
        "title": "Add Item Profile",
    }
    return render(request, "add_items.html", context)


# views sa pag add og item, please refer to the forms "StockUpdateForm"
def update_items(request, pk):
    queryset = Stock.objects.get(id=pk)
    form = StockUpdateForm(instance=queryset)
    if request.method == 'POST':
        form = StockUpdateForm(request.POST, instance=queryset)
        if form.is_valid():
            form.save()
            messages.success(request, 'Sucessfully Updated')
            return redirect('/list_items')

    context = {
        'form': form
    }
    return render(request, 'add_items.html', context)


# views ni siya sa delete
def delete_items(request, pk):
    queryset = Stock.objects.get(id=pk)
    if request.method == 'POST':
        queryset.delete()
        messages.success(request, 'Successfully Deleted')
        return redirect('/list_items')
    return render(request, 'delete_items.html')

#stock_detail ni siya
def stock_detail(request, pk):
	queryset = Stock.objects.get(id=pk)
	context = {
		"queryset": queryset,
	}
	return render(request, "stock_detail.html", context)



#mao ni siya ang code sa view sa receive and issue item

def issue_items(request, pk):
	queryset = Stock.objects.get(id=pk)
	form = IssueForm(request.POST or None, instance=queryset)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.quantity -= instance.issue_quantity
        #instance.cogon_quantity += instance.issue_quantity
		instance.issue_by = str(request.user)
		messages.success(request, "Issued SUCCESSFULLY. " + str(instance.quantity) + " " + str(instance.item_name) + "s now left in Bodega")
		instance.save()

		return redirect('/stock_detail/'+str(instance.id))
		# return HttpResponseRedirect(instance.get_absolute_url())

	context = {
		"title": 'Issue ' + str(queryset.item_name),
		"queryset": queryset,
		"form": form,
		"username": 'Issue By: ' + str(request.user),
	}
	return render(request, "add_items.html", context)



def receive_items(request, pk):
	queryset = Stock.objects.get(id=pk)
	form = ReceiveForm(request.POST or None, instance=queryset)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.quantity += instance.receive_quantity
		instance.save()
		messages.success(request, "Received SUCCESSFULLY. " + str(instance.quantity) + " " + str(instance.item_name)+"s now in Store")

		return redirect('/stock_detail/'+str(instance.id))
		# return HttpResponseRedirect(instance.get_absolute_url())
	context = {
			"title": 'Receive ' + str(queryset.item_name) + ' to the Bodega',
			"instance": queryset,
			"form": form,
			"username": 'Receive By: ' + str(request.user),
		}
	return render(request, "add_items.html", context)

#reorder level views
def reorder_level(request, pk):
	queryset = Stock.objects.get(id=pk)
	form = ReorderLevelForm(request.POST or None, instance=queryset)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()
		messages.success(request, "Reorder level for " + str(instance.item_name) + " is updated to " + str(instance.reorder_level))

		return redirect("/list_items")
	context = {
			"instance": queryset,
			"form": form,
		}
	return render(request, "add_items.html", context)

def cogon_items(request):
	title = 'List of Items'
	queryset = Stock.objects.filter(issue_to__icontains='Cogon')
	context = {
		"title": title,
		"queryset": queryset,
	}
	return render(request, "cogon_items.html", context)

    #    queryset = Stock.objects.filter(  # category__icontains=form['category'].value(),
    #        issue_to__icontains='Cogon'
    #    )