from django.http import HttpResponse
from django.views import View
from django.shortcuts import render, get_object_or_404, redirect

from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView

from catalog.apps import CatalogConfig
from catalog.forms import ProductForm
from catalog.models import Product


# def home(request):
#     return render(request, "catalog/home.html")

class HomeView(TemplateView):
    template_name = 'catalog/home.html'


# def contacts(request):
#     if request.method == "POST":
#         name = request.POST.get("name")
#         message = request.POST.get("message")
#
#         return HttpResponse(f"Спасибо {name}! Ваши данные успешно учтены.")
#     return render(request, "catalog/contacts.html")


class ContactsView(View):
    def get(self, request):
        return render(request, "catalog/contacts.html")

    def post(self, request):
        name = request.POST.get("name")
        message = request.POST.get("message")

        # Передаем сообщение в шаблон
        return render(request, "catalog/contacts.html", {
            'success_message': f"Спасибо {name}! Ваши данные успешно учтены."
        }
                      )



# def cars(request):
#     cars = Product.objects.all()
#     context = {"cars": cars}
#     return render(request, "cars_list.html", context)

# CBV реализация

class ProductsListView(ListView):
    model = Product



# def car_detail(request, pk):
#     car = get_object_or_404(Product, pk=pk)
#     context = {"car": car}
#     return render(request, "car_detail.html", context)


class ProductDetailView(DetailView):
    model = Product


# def add_product(request):
#     if request.method == "POST":
#         form = ProductForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect("/")  # перенаправляем обратно на главную страницу
#     else:
#         form = ProductForm()
#     return render(request, "add_product.html", {"form": form})


class ProductCreateView(CreateView):
    model = Product
    fields = ["name", "description", "category", "price", "image"]
    success_url = reverse_lazy("catalog:cars")


# def edit_product(request, pk):
#     product = get_object_or_404(Product, pk=pk)
#     if request.method == "POST":
#         form = ProductForm(request.POST, request.FILES, instance=product)
#         if form.is_valid():
#             form.save()
#             return redirect("catalog:cars")  # перенаправляем на список продуктов
#     else:
#         form = ProductForm(instance=product)
#     return render(request, "edit_product.html", {"form": form})

class ProductUpdateView(UpdateView):
    model = Product
    fields = ["name", "description", "category", "price", "image"]
    success_url = reverse_lazy("catalog:cars")


class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy("catalog:cars")
