from django import forms
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

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ("name", "description", "image", "price")

    def clean_name(self):
        name = self.cleaned_data["name"]
        for word in FORBIDDEN_WORDS:
            if word.lower() in name.lower():
                raise forms.ValidationError(f"Использование слова '{word}' запрещено.")
        return name

    def clean_description(self):
        description = self.cleaned_data["description"]
        if description:
            for word in FORBIDDEN_WORDS:
                if word.lower() in description.lower():
                    raise forms.ValidationError(f"Использование слова '{word}' запрещено.")
        return description
