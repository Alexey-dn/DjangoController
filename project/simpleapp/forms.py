"""
Для рабочих проектов советуем всё-таки потратить время и перечислить поля в fields,
чтобы не было ситуации, что вы добавили новое поле в модель, которое нельзя редактировать пользователям,
а из-за fields = ‘__all__’ это поле стало автоматически доступным для редактирования через форму.
Примером такого поля может быть время создания товара. Странно, если пользователь будет иметь возможность
его редактировать.
В зависимости от того, как мы расположим поля в списке, в таком порядке они и будут выведены на странице.
Это значит, мы сможем удобнее и логичнее вывести данные для заполнения.
"""

from django import forms
from django.core.exceptions import ValidationError

from .models import Product


class ProductForm(forms.ModelForm):
    description = forms.CharField(min_length=20)

    class Meta:
        model = Product
        fields = [
            'name',
            'description',
            'category',
            'quantity',
            'price',
        ]

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get("name")
        description = cleaned_data.get("description")

        if name == description:
            raise ValidationError(
                "Описание не должно быть идентично названию."
            )

        return cleaned_data
