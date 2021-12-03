from django.views.generic import CreateView, ListView, UpdateView, DetailView, DeleteView
from ..models.products import  Product
from ..models.shops import  Shop
from django.urls import reverse_lazy
# Create your views here.

class ProductCreateView(CreateView):
    '''ProductCreateView class'''
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
    '''ProductListView class'''
    template_name = 'product/shop_list.html'
    model = Product
    ordering = ['id']
    paginate_by = 4

    def get_queryset(self):
        product_objs = self.model.objects.filter(shop_id=\
            self.request.resolver_match.kwargs['pk']).order_by('id')
        return product_objs

class ProductUpdateView(UpdateView):
    '''ProductUpdateView'''
    model = Product
    fields = ['product_name', 'shop_id', 'image', 'is_published']

    def get_success_url(self):
        shop_id = self.object.shop_id
        return reverse_lazy(
            'productlist', kwargs={'pk': shop_id.id})

class ProductDetailsView(DetailView):
    '''ProductDetailsView'''
    model = Product

class ProductDeleteView(DeleteView):
    '''ProductDeleteView'''
    model = Product

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def get_success_url(self):
        shop_id = self.object.shop_id
        return reverse_lazy(
            'productlist', kwargs={'pk': shop_id.id})
