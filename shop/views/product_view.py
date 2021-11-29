import django
from django.db import models
from django.db.models import fields
from django.shortcuts import render, redirect
from django.views.generic import CreateView, ListView, UpdateView, DetailView
from django_filters import filters
from ..models.products import  Product
from django.conf import settings
from ..filters import ShopFilter
# Create your views here.

class ProductCreateView(CreateView):
    model = Product
    success_url = "/"
    fields = ('product_name', 'image', 'shop_id', 'purchase_price', 'sale_price', 'mfg_date', 'expiry_date')

    # def form_valid(self, form):
    #     form.instance.shop_owner = self.request.user
    #     return super().form_valid(form)

class ProductListView(ListView):
    template_name = 'product/shop_list.html'
    model = Product
    ordering = ['id']

    # def get_queryset(self):
        # qs = self.model.objects.all().order_by('id')
        # shop_filtered_list = ShopFilter(self.request.GET, queryset=qs)
        # return shop_filtered_list

    # def post(self, request):
    #     if self.request.POST.get('shop_unapprove'):
    #         shops = self.model.objects.get(id = self.request.POST.get('shop_unapprove'))
    #         shops.is_approved = False
    #         shops.save()
    #     if self.request.POST.get('approve'):
    #         shops = self.model.objects.get(id = self.request.POST.get('approve'))
    #         shops.is_approved = True
    #         shops.save()
    #     return redirect('shoplist')

class ProductUpdateView(UpdateView):
    model = Product
    fields = ['shop_owner', 'image']
    success_url = '/shops/shop_list'

class ProductDetailsView(DetailView):
    model = Product
