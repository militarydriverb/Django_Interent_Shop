from django.urls import path
from catalog.apps import CatalogConfig
from . import views
# from catalog.views import cars, car_detail, add_product, edit_product
from catalog.views import ProductsListView, ProductDetailView, ProductCreateView, ProductUpdateView, ProductDeleteView, \
    HomeView, ContactsView

app_name = CatalogConfig.name

urlpatterns = [
    path("", ProductsListView.as_view(), name="cars"),
    path("home/", HomeView.as_view(), name="home"),
    path("contacts/", ContactsView.as_view(), name="contacts"),
    path("cars/<int:pk>/", ProductDetailView.as_view(), name="car_detail"),
    path("add/", ProductCreateView.as_view(), name="add_product"),
    path("edit/<int:pk>/update/", ProductUpdateView.as_view(), name="edit_product"),
    path("delete/<int:pk>/delete/", ProductDeleteView.as_view(), name="delete_product"),
]
