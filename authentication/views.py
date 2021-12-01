from django.http import response
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView
from django.contrib.auth import get_user_model
from .filters import UserRoleFilter
from django.views import generic
from shop.models.products import Product
from shop.models.shops import Shop
from shop.filters import ProductFilter
from django.http import HttpResponseRedirect
from order.models import SaleOrder, SaleOrderLine
import datetime


# Create your views here.

class UsersList(ListView):
    template_name = 'users/users_list.html'
    model = get_user_model()
    ordering = ['id']

    def get_context_data(self, **kwargs):
        context = super(UsersList, self).get_context_data(**kwargs)
        return context

    def get_queryset(self):
        qs = self.model.objects.all().order_by('id')
        user_filtered_list = UserRoleFilter(self.request.GET, queryset=qs)
        return user_filtered_list
    
    def post(self, request):
        User = get_user_model()
        if self.request.POST.get('user_unapprove'):
            users = User.objects.get(id = self.request.POST.get('user_unapprove'))
            users.allow_by_admin = False
            users.save()
        if self.request.POST.get('user'):
            users = User.objects.get(id = self.request.POST.get('user'))
            users.allow_by_admin = True
            users.save()
        return redirect('userlist')

class HomeView(generic.TemplateView):

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        products = Product.objects.filter(is_published=True)
        shops = Shop.objects.filter(is_approved=True).order_by('id')
        products = ProductFilter(self.request.GET, queryset=products)
        context.update({'products': products, 'shops' : shops})
        return context

    def post(self, request):
        # import pdb;pdb.set_trace()
        product = request.POST.get('product')
        remove = request.POST.get('remove')
        cart = request.session.get('cart')
        if cart:
            quantity = cart.get(product)
            if quantity:
                if remove:
                    if quantity<=1:
                        cart.pop(product)
                    else:
                        cart[product]  = quantity-1
                else:
                    cart[product]  = quantity+1

            else:
                cart[product] = 1
        else:
            cart = {}
            cart[product] = 1
        request.session['cart'] = cart
        return redirect('home')

class UsersDetails(DetailView):
    template_name = 'users/user_details.html'
    model = get_user_model()

    def get_context_data(self, **kwargs):
        context = super(UsersDetails, self).get_context_data(**kwargs)
        cart = self.request.session.get('cart')
        orderlines = {}
        total = 0
        if cart:
            orderlines = {Product.objects.get(pk=line):cart[line] for line in cart}
            total = sum([line.sale_price*orderlines[line] for line in orderlines])
        context.update({'orderlines' : orderlines, 'total' : total})
        return context

    def post(self, request, pk):
        product = request.POST.get('product')
        remove = request.POST.get('remove')
        cart = request.session.get('cart')
        if cart:
            quantity = cart.get(product)
            if quantity:
                if remove:
                    if quantity<=1:
                        cart.pop(product)
                    else:
                        cart[product]  = quantity-1
                else:
                    cart[product]  = quantity+1

            else:
                cart[product] = 1
        else:
            cart = {}
            cart[product] = 1
        request.session['cart'] = cart
        return HttpResponseRedirect(self.request.path_info)

def create_order(request, pk):
    customer = get_user_model().objects.get(pk=pk)
    cart = request.session.get('cart')
    if cart:
        orderlines = {Product.objects.get(pk=line):cart[line] for line in cart}
        lines = []
        for line in orderlines:
            orderline_id = SaleOrderLine(product_id=line, qty=orderlines[line], unit_price=line.sale_price, subtotal=orderlines[line]*line.sale_price)
            orderline_id.save()
            lines.append(orderline_id)
        amount_total = sum([line.subtotal for line in lines])
        order_id = SaleOrder(customer_id=customer, order_status='new', order_date=datetime.datetime.now(), amount_total=amount_total)
        order_id.save()
        for line in lines:
            order_id.orderline_ids.add(line)
        request.session['cart'] = {}
        return redirect('orderdetails', pk=order_id.id)
    return redirect('home')
