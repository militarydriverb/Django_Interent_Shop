from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

from catalog.apps import CatalogConfig
from catalog.forms import ProductForm
from catalog.models import Product


def home(request):
    return render(request, "home.html")


def contacts(request):
    if request.method == "POST":
        name = request.POST.get("name")
        message = request.POST.get("message")

        return HttpResponse(f"Спасибо {name}! Ваши данные успешно учтены.")
    return render(request, "contacts.html")


def cars(request):
    cars  = Product.objects.all()
    context = {"cars": cars}
    return render(request, "cars_list.html", context)


def car_detail(request,pk):
    car = get_object_or_404(Product, pk=pk)
    context = {"car": car}
    return render(request, "car_detail.html", context)


def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/')  # перенаправляем обратно на главную страницу
    else:
        form = ProductForm()
    return render(request, 'add_product.html', {'form': form})


def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('catalog:cars')  # перенаправляем на список продуктов
    else:
        form = ProductForm(instance=product)
    return render(request, 'edit_product.html', {'form': form})

