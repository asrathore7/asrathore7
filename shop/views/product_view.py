import django
from django.db import models
from django.db.models import fields
from django.shortcuts import render, redirect
from django.views.generic import CreateView, ListView, UpdateView, DetailView, DeleteView
from django_filters import filters
from ..models.products import  Product
from ..models.shops import  Shop
from django.conf import settings
from ..filters import ShopFilter
from django.urls import reverse_lazy
# Create your views here.

class ProductCreateView(CreateView):
    model = Product
    success_url = "/"
    fields = ('product_name', 'image', 'shop_id', 'purchase_price', 'sale_price', 'is_published')

    def get_initial(self):
        shop_id = Shop.objects.filter(id=self.kwargs['pk'])
        return {
            'shop_id':shop_id[0].id,
        }

    def get_success_url(self):
        shop_id = self.object.shop_id
        return reverse_lazy( 'productlist', kwargs={'pk': shop_id.id})

class ProductListView(ListView):
    template_name = 'product/shop_list.html'
    model = Product
    ordering = ['id']

    def get_queryset(self):
        product_objs = self.model.objects.filter(shop_id=self.request.resolver_match.kwargs['pk']).order_by('id')
        return product_objs

class ProductUpdateView(UpdateView):
    model = Product
    fields = ['product_name', 'shop_id', 'image', 'is_published']

    def get_success_url(self):
        shop_id = self.object.shop_id
        return reverse_lazy( 'productlist', kwargs={'pk': shop_id.id})

class ProductDetailsView(DetailView):
    model = Product

class ProductDeleteView(DeleteView):
    model = Product

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def get_success_url(self):
        shop_id = self.object.shop_id
        return reverse_lazy( 'productlist', kwargs={'pk': shop_id.id})
