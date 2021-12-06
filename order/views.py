'''Order's view'''
from django.views.generic import DetailView, ListView
from django.shortcuts import redirect
from .models import SaleOrder

class OrderDetails(DetailView):
    '''OrderDetails for view'''
    model = SaleOrder
    template_name = 'order/order_details.html'


class OrderListView(ListView):
    '''OrderListView for view'''
    # pylint: disable=no-member
    model = SaleOrder
    template_name = 'order/order_list.html'

    def get_queryset(self):
        val = super().get_queryset()
        if self.request.user.role == 'customer':
            order_objs = val.filter(customer_id=self.request.user.id).order_by('id')
            return order_objs
        order_objs = val.order_by('id')
        return order_objs

    def post(self, pk):
        '''Change order status'''
        if self.request.POST.get('ship'):
            order = SaleOrder.objects.get(id=self.request.POST.get('ship'))
            order.order_status = 'ship'
            order.save()
        if self.request.POST.get('deliver'):
            order = self.model.objects.get(id = self.request.POST.get('deliver'))
            order.order_status = 'deliver'
            order.save()
        if self.request.POST.get('cancel'):
            order = self.model.objects.get(id = self.request.POST.get('cancel'))
            order.order_status = 'cancel'
            order.save()
        return redirect('orderlist')
