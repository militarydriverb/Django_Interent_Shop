from django.urls import path
from catalog.apps import CatalogConfig
from . import views
from catalog.views import cars, car_detail, add_product, edit_product

app_name = CatalogConfig.name

urlpatterns = [
    path("", cars, name="cars"),
    path("home/", views.home, name="home"),
    path("contacts/", views.contacts, name="contacts"),
    path("cars/<int:pk>/", car_detail, name="car_detail"),
    path("add/", add_product, name="add_product"),
    path("edit/<int:pk>/", edit_product, name="edit_product"),
]
