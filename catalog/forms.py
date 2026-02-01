from django import forms
from django.forms.fields import BooleanField

from .models import Product

FORBIDDEN_WORDS = [
    "казино",
    "криптовалюта",
    "крипта",
    "биржа",
    "дешево",
    "бесплатно",
    "обман",
    "полиция",
    "радар",
]

class StyleFormMixin():
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, BooleanField):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'



class ProductForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Product
        fields = ("name", "description", "category" ,"image", "price")


class ProductModeratorForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Product
        fields = ("status",)


    def clean_name(self):
        name = self.cleaned_data["name"]
        for word in FORBIDDEN_WORDS:
            if word.lower() in name.lower():
                raise forms.ValidationError(f"Word usage '{word}' forbidden.")
        return name

    def clean_description(self):
        description = self.cleaned_data["description"]
        if description:
            for word in FORBIDDEN_WORDS:
                if word.lower() in description.lower():
                    raise forms.ValidationError(f"Word usage '{word}' forbidden.")
        return description

    def clean_price(self):
        price = self.cleaned_data["price"]
        if not isinstance(price, (int, float)) or price <= 0:
            raise forms.ValidationError("Price must be a positive number.")
        return price

    def clean_image(self):
        image = self.cleaned_data.get("image")
        if image:
            # Проверка размера файла (максимум 5 МБ)
            if image.size > 5 * 1024 * 1024:
                raise forms.ValidationError("Image size should not exceed 5 MB.")
            
            # Проверка формата файла
            import os
            ext = os.path.splitext(image.name)[1].lower()
            if ext not in [".jpg", ".jpeg", ".png"]:
                raise forms.ValidationError("Only JPEG and PNG formats are permitted.")
        return image