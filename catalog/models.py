from django.db import models

# Create your models here.

class Category(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Category Name',
        help_text='Enter Category Name'
    )
    description = models.TextField(
        verbose_name='Category Description',
        help_text='Enter Category Description',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
            return self.name


class Product(models.Model):
    name = models.CharField(max_length=200,verbose_name='Product Name', help_text='Enter Product Name')
    description = models.TextField(
        verbose_name='Product Description',
        help_text='Enter Product Description',
        null=True,
        blank=True
    )
    image = models.ImageField(
        upload_to='catalog/product_images',
        verbose_name='Product Image',
        help_text='Upload Product Image',
        null=True,
        blank=True
    )
    category = models.ForeignKey(
        "Category",
        on_delete=models.SET_NULL,
        verbose_name='Category',
        help_text='Enter Category',
        null=True,
        blank=True,
        related_name='products'
        )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        ordering = ['category','name']

    def __str__(self):
        return f"{self.name}, {self.category}"

