from django.core.cache import cache

from catalog.models import Product
from config.settings import CACHE_ENABLED



def get_products_from_cache():
    """Получаем данные по продуктам из кэша, если кэш пуст, то получем из БД"""
    if not CACHE_ENABLED:
        return Product.objects.all()
    key = "product_list"
    products = cache.get(key)
    if products is not None:
        return products
    products = list(Product.objects.all())  # преобразуем QuerySet в list для сериализации
    cache.set(key, products, 60 * 15)  # кэшируем на 15 минут
    return products

def get_products_by_category(category_id):
    """Возвращает список всех продуктов в указанной категории с использованием кэширования"""
    if not CACHE_ENABLED:
        return Product.objects.filter(category_id=category_id, status=Product.STATUS_PUBLISHED)

    key = f"products_category_{category_id}"
    products = cache.get(key)
    if products is not None:
        return products

    products = list(Product.objects.filter(category_id=category_id, status=Product.STATUS_PUBLISHED))  # преобразуем в list
    cache.set(key, products, 60 * 15)  # кэшируем на 15 минут
    return products