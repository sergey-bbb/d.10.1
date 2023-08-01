from django import forms
from .models import News
from django.core.exceptions import ValidationError

class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = [
            'name',
            'author',
            'category',
            'data',


        ]

    def clean(self):
        cleaned_data = super().clean()
        description = cleaned_data.get("description")
        name = cleaned_data.get("name")

        if name == description:
            raise ValidationError(
                "Описание не должно быть идентично названию."
            )

        return cleaned_data