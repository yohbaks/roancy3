from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.http import HttpResponse  # sa excel ni sya na import
from django.contrib import messages  # sa notifacation ni siya
import csv
import json
from django.contrib.auth.decorators import login_required
import pytz
from datetime import datetime
import logging
import traceback
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

@login_required
# Create your views here.
# home view ni sya bai
def home(request):
    title = 'Welcome to Roancy Application'
    all_store = All_Store.objects.all()

    context = {
        "title": title,
        'stores': all_store,
    }
    return render(request, "home.html", context)


def store(request, slug):
    store = All_Store.objects.get(slug=slug)
    this_store_items = Stock.objects.filter(issue_to_model=store)
    form = StockSearchForm(request.POST or None)
    print(this_store_items)
    store_record = Shop_Record.objects.filter(store=store)
    all_store = All_Store.objects.all()
    header=store.name+' STOCKS'
    page = request.GET.get('page', 1)
    paginator = Paginator(this_store_items, 10)
    try:
        page_queryset = paginator.page(page)
    except PageNotAnInteger:
        page_queryset = paginator.page(1)
    except EmptyPage:
        page_queryset = paginator.page(paginator.num_pages)
    context = {
        'header':header,
        'slug':slug,
        'form':form,
        'store': store,
        'stores':all_store,
        'products': page_queryset,
        'store_record': store_record,
    }
    if request.method == 'POST':

        queryset = Stock.objects.filter( category__pk=form['category'].value(),
            item_name__icontains=form['item_name'].value()
        )

        if form['export_to_CSV'].value() == True:
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
            "products": queryset,
        }
    template = 'cogon.html'
    return render(request, template, context)


# views sa pag search, please refer to the forms "StockSearchForm"
@login_required
def list_items(request):
    header = 'BODEGA STOCKS'
    form = StockSearchForm(request.POST or None)
    queryset = Stock.objects.all()
    all_store = All_Store.objects.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(queryset, 10)
    try:
        page_queryset = paginator.page(page)
    except PageNotAnInteger:
        page_queryset = paginator.page(1)
    except EmptyPage:
        page_queryset = paginator.page(paginator.num_pages)
    context = {
        "header": header,
        "queryset": page_queryset,
        'stores':all_store,
        "form": form,
    }
    if request.method == 'POST':  # code ni siya if the search box is click

        queryset = Stock.objects.filter(  category__pk=form['category'].value(),
            item_name__icontains=form['item_name'].value()
        )
        print(queryset)
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
            "queryset": page_queryset,
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
    all_store = All_Store.objects.all()
    context = {
        "form": form,
        "title": "Add Item Profile",
        'stores':all_store,
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
    all_store = All_Store.objects.all()
    queryset = Stock.objects.get(id=pk)
    if request.method == 'POST':
        queryset.delete()
        messages.success(request, 'Successfully Deleted')
        return redirect('/list_items')
    context={
        'stores':all_store,
    }
    return render(request, 'delete_items.html',context)


# stock_detail ni siya
def shop_stock_detail(request, pk):
    queryset = Stock.objects.get(id=pk)
    remainnig=Shop_Record.objects.get(product__pk=pk,store=queryset.issue_to_model).remaining_items
    reoder_level=Shop_Record.objects.get(product__pk=pk,store=queryset.issue_to_model).reoder_level
    shop_record=Shop_Record.objects.get(product__pk=pk,store=queryset.issue_to_model)
    all_store = All_Store.objects.all()
    context = {
        "queryset": queryset,
        'remaining':remainnig,
        'stores':all_store,
        'shop_record':shop_record,
        'reoder_level':reoder_level,
    }
    return render(request, "shop_stock_detail.html", context)


def stock_detail(request, pk):
    queryset = Stock.objects.get(id=pk)
    print(queryset.issue_to_model)
    try:
        remainnig=Shop_Record.objects.get(product__pk=pk,store=queryset.issue_by_model).remaining_items
    except:
        remainnig=queryset.quantity
    all_store = All_Store.objects.all()
    context = {
        "queryset": queryset,
        'remaining': remainnig,
        'stores':all_store,
    }
    return render(request, "stock_detail.html", context)


# mao ni siya ang code sa view sa receive and issue item

def issue_items(request, pk):
    queryset = Stock.objects.get(id=pk)
    form = IssueForm(request.POST or None, instance=queryset)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.quantity -= instance.issue_quantity
        # instance.cogon_quantity += instance.issue_quantity
        instance.issue_by = str(request.user)
        if instance.quantity < 0:
            messages.success(request, "You sold more items than those available in the store. ")
            return redirect('/stock_detail/' + str(instance.id))
        messages.success(request, "Issued SUCCESSFULLY. " + str(instance.quantity) + " " + str(
            instance.item_name) + "s now left in Bodega")

        instance.save()

        print(queryset,queryset.issue_to_model)
        new_shop_record=Shop_Record.objects.get(product=queryset,store=queryset.issue_to_model)

        new_shop_record.store=queryset.issue_to_model
        new_shop_record.product=queryset
        new_shop_record.remaining_items+=instance.issue_quantity
        new_shop_record.save()

        return redirect('/stock_detail/' + str(instance.id))
    # return HttpResponseRedirect(instance.get_absolute_url())
    all_store = All_Store.objects.all()
    context = {
        'stores':all_store,
        "title": 'Issue ' + str(queryset.item_name),
        "queryset": queryset,
        "form": form,
        "username": 'Issue By: ' + str(request.user),
    }
    return render(request, "sell_items.html", context)


def sell_items(request, pk):
    queryset = Stock.objects.get(id=pk)

    form = ReceiveForm(request.POST or None, instance=queryset)
    if form.is_valid():
        instance = form.save(commit=False)
        #instance.quantity -= instance.receive_quantity

        print(instance.quantity)
        print(instance.receive_quantity)
        print(instance)

        queryset.save()
        individual_sale=Individual_Sold_Item()
        individual_sale.store=instance.issue_to_model
        individual_sale.product=instance
        individual_sale.quantity=instance.receive_quantity
        individual_sale.save()

        date_today = pytz.timezone('Asia/Manila')
        today_date = datetime.now(tz=date_today).date()

        try:
            date_sale=Date_Sale.objects.get(date=today_date,store=instance.issue_to_model)
            date_sale.daily_sales_total+=instance.receive_quantity*instance.price
            date_sale.daily_quantity_total+=instance.receive_quantity
            date_sale.save()
        except:
            logging.error(traceback.format_exc())
            date_sale=Date_Sale()
            date_sale.date=today_date
            date_sale.store=instance.issue_to_model
            date_sale.daily_sales_total=instance.receive_quantity*instance.price
            date_sale.daily_quantity_total=instance.receive_quantity
            date_sale.save()

        shop_record=Shop_Record.objects.get(product__pk=instance.pk,store=instance.issue_to_model)
        old_quantity=shop_record.remaining_items
        sold_items_quantity=instance.receive_quantity
        new_quantity=old_quantity-sold_items_quantity
        if new_quantity<0:
            messages.success(request, "You sold more items than those available in the store. " )
            return redirect('/shop_stock_detail/' + str(instance.id))
        else:

            shop_record.remaining_items-=instance.receive_quantity
            shop_record.save()
        messages.success(request, "Sold SUCCESSFULLY. " + str(shop_record.remaining_items) + " " + str(
            instance.item_name) + "s now in Store")
        try:
            sold_items=Sold_Items.objects.get(store=queryset.issue_to_model,product=queryset)

            sold_items.product = queryset
            sold_items.store = queryset.issue_to_model
            sold_items.quantity += instance.receive_quantity
            sold_items.save()
        except:
            sold_items = Sold_Items()
            sold_items.product = queryset
            sold_items.store = queryset.issue_to_model
            sold_items.quantity = instance.receive_quantity
            sold_items.save()

        return redirect('/shop_stock_detail/' + str(instance.id))
    # return HttpResponseRedirect(instance.get_absolute_url())
    all_store = All_Store.objects.all()
    context = {
        'stores':all_store,
        "title": 'Sell ' + str(queryset.item_name) + ' Items',
        "instance": queryset,
        "form": form,
        "username": 'Sell By: ' + str(request.user),
    }
    return render(request, "add_items.html", context)
def sold_more_items():
    template='excess.html'
    return render(request,template)

def receive_items(request, pk):
    queryset = Stock.objects.get(id=pk)
    form = ReceiveForm(request.POST or None, instance=queryset)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.quantity += instance.receive_quantity
        try:
            shop_record=Shop_Record.objects.get(product__pk=pk,store=queryset.issue_by_model)
        except:
            shop_record=Shop_Record()

        instance.save()

        shop_record.store = instance.issue_to_model
        shop_record.product = queryset
        shop_record.remaining_items += instance.receive_quantity
        shop_record.save()
        messages.success(request, "Received SUCCESSFULLY. " + str(instance.quantity) + " " + str(
            instance.item_name) + "s now in Store")

        return redirect('/stock_detail/' + str(instance.id))
    # return HttpResponseRedirect(instance.get_absolute_url())
    all_store = All_Store.objects.all()
    context = {
        'stores':all_store,
        "title": 'Receive ' + str(queryset.item_name) + ' to the Bodega',
        "instance": queryset,
        "form": form,
        "username": 'Receive By: ' + str(request.user),
    }
    return render(request, "add_items.html", context)


# reorder level views
def reorder_level(request, pk):
    queryset = Stock.objects.get(id=pk)
    form = ReorderLevelForm(request.POST or None, instance=queryset)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "Reorder level for " + str(instance.item_name) + " is updated to " + str(
            instance.reorder_level))

        return redirect("/list_items")
    all_store = All_Store.objects.all()
    context = {
        'stores':all_store,
        "instance": queryset,
        "form": form,
    }
    return render(request, "add_items.html", context)


def shop_reoder_level(request,slug,pk):

    queryset=Shop_Record.objects.get(store__slug=slug,product__id=pk)
    form = ShopReoderLevelForm(request.POST or None, instance=queryset)
    if form.is_valid():
        instance = form.save(commit=False)

        instance.save()
        messages.success(request, "Reorder level for " + str(instance.product.item_name) + " is updated to " + str(
            instance.reoder_level))

        return redirect("/shop_stock_detail/"+str(instance.product.pk))
    all_store = All_Store.objects.all()
    context = {
        'stores':all_store,
        "instance": queryset,
        "form": form,
    }
    return render(request, "add_items.html", context)


def cogon_items(request):
    title = 'List of Items'
    queryset = Stock.objects.filter(issue_to__icontains='Cogon')
    all_store = All_Store.objects.all()
    context = {
        'stores':all_store,
        "title": title,
        "queryset": queryset,
    }
    return render(request, "cogon_items.html", context)

#    queryset = Stock.objects.filter(  # category__icontains=form['category'].value(),
#        issue_to__icontains='Cogon'
#    )

def daily_sales(request,pk,store_id):
    queryset=Stock.objects.filter(pk=pk)
    sales_record=Sold_Items.objects.filter(store__pk=store_id)
    all_store = All_Store.objects.all()
    context={
        'stores':all_store,
        'queryset':queryset,
        'sales_record':sales_record,
    }
    template='daily_sales.html'
    return render(request,template,context)

def search_view(request,slug):
    term=request.GET.get('search')
    all_items=Stock.objects.filter(item_name__icontains=term,issue_to_model__slug=slug)
    all_store = All_Store.objects.all()
    context={
        'stores':all_store,
        'products':all_items,
        'slug': slug,
    }
    return render(request,'cogon.html',context)

def all_daily_sales(request):

    date_sale = Date_Sale.objects.all()
    form = AllSaleSearchForm(request.POST or None)
    header='ALL DAILY SALES: '+str(date_sale.last().date)
    all_store = All_Store.objects.all()
    if form.is_valid:
        picked_date=form['date'].value()
        date_sale=Date_Sale.objects.filter(date=picked_date)
        print(date_sale)

    context = {
        'stores':all_store,
        'date_sale': date_sale,
        'header':header,
        'form':form,
    }

    template = 'all_sales.html'
    return render(request, template, context)


def shop_sold_items(request,slug):
    store=All_Store.objects.get(slug=slug)
    date_sale=Individual_Sold_Item.objects.filter(store=store)
    print(date_sale)
    header = 'ALL DAILY SALES: ' + date_sale.last().store.name
    all_store = All_Store.objects.all()
    context={
        'header':header,
        'queryset':date_sale,
        'stores':all_store,
    }
    template='shop_sold_items.html'
    return render(request,template,context)

def get_subcategory(request):
    id=request.GET('id','')
    results=list(SubCategory.objects.filter(category__id=int(id)).values('id','name'))
    return HttpResponse(json.dumps(results),context_type='application/json')

def load_sub_caegories(request):
    print('it was succesful')
    print(request)
    print(request)
    category_id=request.GET.get('category')
    sub_categories=SubCategory.objects.filter(category__id=category_id).order_by('name')
    return render(request,'sub_categories_dropdown_list.html',{'sub_categories':sub_categories})