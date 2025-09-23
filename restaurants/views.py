from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from .models import Restaurant

class RestaurantListView(ListView):
    model = Restaurant
    paginate_by = 10
    template_name = "restaurants/restaurants_list.html"

    def get_queryset(self):
        return Restaurant.objects.filter(is_active=True).select_related()

class RestaurantDetailView(DetailView):
    model = Restaurant
    queryset = Restaurant.objects.prefetch_related("opening_windows") 