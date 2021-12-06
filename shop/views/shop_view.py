'''Shop related code'''
from django.shortcuts import redirect
from django.views.generic import CreateView, ListView, UpdateView, DetailView
from ..models.shops import  Shop
from ..filters import ShopFilter
# Create your views here.

class ShopCreateView(CreateView):
    '''Add doc string ShopCreateView'''
    model = Shop
    success_url = "/"
    fields = ('shop_name', 'shop_owner',
        'image', 'street', 'street1',
        'pin_code', 'city', 'country'
    )

    def form_valid(self, form):
        form.instance.shop_owner = self.request.user
        return super().form_valid(form)

    def get_initial(self):
        return {'shop_owner': self.request.user}


class ShopListView(ListView):
    '''Add doc string ShopListView'''

    template_name = 'shop/shop_list.html'
    model = Shop
    ordering = ['id']

    def get_queryset(self):
        if self.request.user.role == 'shop':
            user = self.request.user
            shop_ids = self.model.objects.filter(
                shop_owner=user).order_by('id')
            shop_filtered_list = ShopFilter(
                self.request.GET, queryset=shop_ids)
            return shop_filtered_list
        shop_ids = self.model.objects.all().order_by('id')
        shop_filtered_list = ShopFilter(
            self.request.GET, queryset=shop_ids)
        return shop_filtered_list

    def post(self):
        '''Change shop approvel'''
        if self.request.POST.get('shop_unapprove'):
            shops = self.model.objects.get(
                id = self.request.POST.get('shop_unapprove'))
            shops.is_approved = False
            shops.save()
        if self.request.POST.get('approve'):
            shops = self.model.objects.get(
                id = self.request.POST.get('approve'))
            shops.is_approved = True
            shops.save()
        return redirect('shoplist')

class ShopUpdateView(UpdateView):
    '''Add doc string ShopUpdateView'''

    model = Shop
    fields = ['shop_owner', 'image']
    success_url = '/shops/shop_list'

class ShopDetailsView(DetailView):
    '''Add doc string ShopDetailsView'''

    model = Shop
