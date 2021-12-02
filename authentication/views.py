from django.db.models.aggregates import Sum
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
from django.db.models.functions import TruncMonth
from django.db.models import Count
from rest_framework.views import APIView
from rest_framework.response import Response
from django.views.generic import View

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

class DashboardHomeView(View):
    def get(self, request, *args, **kwargs):
        # import pdb;pdb.set_trace()
        if request.user.role == 'admin':
            return render(request, 'admin_dashboard.html')
        elif request.user.role == 'customer':
            return render(request, 'customer_dashboard.html')
        else:
            return redirect('home')

class ChartData(APIView):

    def get(self, request):
        if request.user.role == 'admin':
            monthly_sale_order = SaleOrder.objects.annotate(month=TruncMonth('order_date')).values('month').annotate(c=Count('id')).values('month', 'c')
            product_total_sale = SaleOrderLine.objects.values('product_id').annotate(quantity = Sum('qty'),price = Sum('subtotal'))
            sale_data, label_sale_data = [], []
            chartLabel = ['January','February', 'March', 'April', 'May', 'June', 'July', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec']
            for month in range(1, 13):
                temp = True
                for sale in monthly_sale_order:
                    if month == sale['month'].month:
                        temp = False
                        label_sale_data.append(sale['c'])
                if temp:
                    label_sale_data.append(0)
                # sale_data.append(sale['month'].month)
            shop_names = []
            for shop in Shop.objects.all():
                shop_names.append(shop.shop_name)
            shop_data = {}
            for shop in shop_names:
                temp_shop = True
                for product in product_total_sale:
                    product_id = Product.objects.get(pk=product['product_id'])
                    if product_id.shop_id.shop_name == shop:
                        temp_shop = False
                        if shop in shop_data.keys():
                            shop_data[shop] = shop_data[shop]+product['price']
                        else:
                            shop_data[shop] = product['price']
                if temp_shop:
                    shop_data[shop] = 0
            data = {
                'labels':  chartLabel,
                'chartdata' : label_sale_data,
                'shop_names' : shop_names,
                'shopchartLabel': 'Total Amount of Sale',
                'shop_data' : [val for val in shop_data.values()]
            }
            return Response(data)
        else:
            return redirect('home')

class CustomerChartData(APIView):

    def get(self, request):
        user = request.user.id
        monthly_sale_order = SaleOrder.objects.filter(customer_id=user).annotate(month=TruncMonth('order_date')).values('month').annotate(c=Count('id')).values('month', 'c')
        product_total_sale = SaleOrderLine.objects.values('product_id').annotate(quantity = Sum('qty'),price = Sum('subtotal'))
        sale_data, label_sale_data = [], []
        chartLabel = ['January','February', 'March', 'April', 'May', 'June', 'July', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec']
        for month in range(1, 13):
            temp = True
            for sale in monthly_sale_order:
                if month == sale['month'].month:
                    temp = False
                    label_sale_data.append(sale['c'])
            if temp:
                label_sale_data.append(0)
        data = {
                'labels':  chartLabel,
                'chartdata' : label_sale_data,
            }
        return Response(data)
