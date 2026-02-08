from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.shortcuts import render, get_object_or_404, redirect

from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.core.exceptions import PermissionDenied

from catalog.apps import CatalogConfig
from catalog.forms import ProductForm, ProductModeratorForm
from catalog.models import Product, Category
from catalog.services import get_products_from_cache, get_products_by_category


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
    template_name = 'catalog/product_list.html'

    def get_queryset(self):
        return get_products_from_cache()


# def car_detail(request, pk):
#     car = get_object_or_404(Product, pk=pk)
#     context = {"car": car}
#     return render(request, "car_detail.html", context)


class ProductDetailView(DetailView):
    model = Product

    def get_object(self, queryset=None):
        """Переопределяем метод для получения объекта из кэша"""
        pk = self.kwargs.get('pk')
        products = get_products_from_cache()
        for product in products:
            if product.pk == pk:
                return product
        # Если не найдено в кэше, получаем из БД
        return get_object_or_404(Product, pk=pk)


# def add_product(request):
#     if request.method == "POST":
#         form = ProductForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect("/")  # перенаправляем обратно на главную страницу
#     else:
#         form = ProductForm()
#     return render(request, "add_product.html", {"form": form})


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    # fields = ["name", "description", "category", "price", "image"]
    form_class = ProductForm
    success_url = reverse_lazy("catalog:cars")

    def form_valid(self, form):
        form.instance.owner = self.request.user  # автоматически устанавливаем владельца
        return super().form_valid(form)

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

class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    # fields = ["name", "description", "category", "price", "image"]
    form_class = ProductForm
    success_url = reverse_lazy("catalog:cars")

    def get_form_class(self):
        user = self.request.user
        if user == self.object.owner:
            return ProductForm
        if user.has_perm("catalog.can_unpublish_product") and user.has_perm("catalog.can_delete_any_product"):
            return ProductModeratorForm
        raise PermissionDenied


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    success_url = reverse_lazy("catalog:cars")

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        if user == self.get_object().owner or (user.has_perm("catalog.can_unpublish_product") and user.has_perm("catalog.can_delete_any_product")):
            return super().dispatch(request, *args, **kwargs)
        raise PermissionDenied

class ProductsByCategoryView(ListView):
    """Представление для отображения продуктов в указанной категории"""
    model = Product
    template_name = 'catalog/products_by_category.html'
    context_object_name = 'products'

    def get_queryset(self):
        category_id = self.kwargs['category_id']
        return get_products_by_category(category_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = get_object_or_404(Category, id=self.kwargs['category_id'])
        return context
