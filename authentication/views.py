from django.http import response
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView, ListView
from django.template.response import TemplateResponse
from django.contrib.auth import get_user_model
from django.conf import settings
from .filters import UserRoleFilter
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
