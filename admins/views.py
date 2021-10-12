from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from users.models import User
from admins.forms import UserAdminRegistrationForm, UserAdminProfileForm
from django.contrib.auth.decorators import user_passes_test
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator


# Create your views here.
@user_passes_test(lambda u: u.is_staff)
def index(request):
    return render(request, 'admins/index.html')


class UserListView(ListView):
    model = User  # Выбор модели(таблицы бд)
    template_name = 'admins/admin-users-read.html'  # Ренер выбранного шаблона

    def get_context_data(self, *, object_list=None, **kwargs):
        contex = super(UserListView, self).get_context_data(object_list=None, **kwargs)
        contex['title'] = 'Админ-панель - Пользователи'
        return contex

    @method_decorator(user_passes_test(lambda u: u.is_staff))
    def dispatch(self, request, *args, **kwargs):
        return super(UserListView, self).dispatch(request, *args, **kwargs)


class UserCreateView(CreateView):
    model = User
    form_class = UserAdminRegistrationForm
    template_name = 'admins/admin-users-create.html'
    success_url = reverse_lazy('admins:admin_users')

    @method_decorator(user_passes_test(lambda u: u.is_staff))
    def dispatch(self, request, *args, **kwargs):
        return super(UserCreateView, self).dispatch(request, *args, **kwargs)


class UserUpdateView(UpdateView):
    model = User
    form_class = UserAdminProfileForm
    template_name = 'admins/admin-users-update-delete.html'
    success_url = reverse_lazy('admins:admin_users')

    @method_decorator(user_passes_test(lambda u: u.is_staff))
    def dispatch(self, request, *args, **kwargs):
        return super(UserUpdateView, self).dispatch(request, *args, **kwargs)


class UserDeleteView(DeleteView):
    model = User
    template_name = 'admins/admin-users-update-delete.html'
    success_url = reverse_lazy('admins:admin_users')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    @method_decorator(user_passes_test(lambda u: u.is_staff))
    def dispatch(self, request, *args, **kwargs):
        return super(UserDeleteView, self).dispatch(request, *args, **kwargs)

class CategorysListView(ListView):
    pass

class ProductsListView(ListView):
    pass