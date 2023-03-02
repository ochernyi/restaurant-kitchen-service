from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from rest_framework.generics import get_object_or_404

from kitchen.forms import DishForm, UserCreationForm
from kitchen.models import User, Dish, DishType


@login_required
def index(request):
    num_users = User.objects.count()
    num_dish = Dish.objects.count()
    num_dish_type = DishType.objects.count()

    context = {
        "num_users": num_users,
        "num_dish": num_dish,
        "num_dish_type": num_dish_type,
    }

    return render(request, "kitchen/index.html", context=context)


class UserListView(LoginRequiredMixin, generic.ListView):
    model = User
    paginate_by = 5


class UserDetailView(LoginRequiredMixin, generic.DetailView):
    model = User
    queryset = User.objects.all().prefetch_related("dishes")


class UserCreateView(LoginRequiredMixin, generic.CreateView):
    model = User
    form_class = UserCreationForm
    success_url = reverse_lazy("kitchen:user-list")


class UserUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = User
    form_class = UserCreationForm
    success_url = reverse_lazy("kitchen:user-list")


class UserDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = User
    success_url = reverse_lazy("kitchen:user-list")


class DishListView(LoginRequiredMixin, generic.ListView):
    model = Dish
    paginate_by = 5


class DishDetailView(LoginRequiredMixin, generic.DetailView):
    model = Dish


class DishCreateView(LoginRequiredMixin, generic.CreateView):
    model = Dish
    form_class = DishForm
    success_url = reverse_lazy("kitchen:dish-list")


class DishUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Dish
    form_class = DishForm
    success_url = reverse_lazy("kitchen:dish-list")


class DishDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Dish
    success_url = reverse_lazy("kitchen:dish-list")


class DishTypeListView(LoginRequiredMixin, generic.ListView):
    model = DishType
    context_object_name = "dish_type_list"
    template_name = "kitchen/dish_type_list.html"
    paginate_by = 5


class DishTypeCreateView(LoginRequiredMixin, generic.CreateView):
    model = DishType
    fields = "__all__"
    success_url = reverse_lazy("kitchen:dish-type-list")
    template_name = "kitchen/dish_type_form.html"


class DishTypeUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = DishType
    fields = "__all__"
    success_url = reverse_lazy("kitchen:dish-type-list")
    template_name = "kitchen/dish_type_form.html"


class DishTypeDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = DishType
    success_url = reverse_lazy("kitchen:dish-type-list")
    template_name = "kitchen/dish_type_confirm_delete.html"


@login_required
def toggle_assign_to_dish(request, pk):
    user = get_object_or_404(User, id=request.user.id)
    if Dish.objects.get(id=pk) in user.dishes.all():
        user.dishes.remove(pk)
    else:
        user.dishes.add(pk)
    return HttpResponseRedirect(reverse_lazy("kitchen:dish-detail", args=[pk]))
