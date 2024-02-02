from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.utils.deconstruct import deconstructible

from .models import Category, PersonModel, Item


@deconstructible
class RussianValidator:
    ALLOWED_CHARS = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдеёжзийклмнопрстуфхцчшщъыьэюя0123456789- "
    code = 'russian'

    def __init__(self, message=None):
        self.message = message if message else "Должны быть только русские символы, дефис, пробел"

    def __call__(self, value, *args, **kwargs):
        if not (set(value) <= set(self.ALLOWED_CHARS)):
            raise ValidationError(self.message, code=self.code)

class AddPostForm(forms.ModelForm):
    #title = forms.CharField(max_length=255, min_length=3,label='Название', widget=forms.TextInput(attrs={'class': 'form-input'}), error_messages={'min_length': "Слишклм короткий",'required': 'Без названия нельзя',})
    #slug = forms.SlugField(max_length=255, label='URL', validators=[MinLengthValidator(3, message='Минумум 3 символа'),MaxLengthValidator(100, message='Максимум 100 символов'),])
    #price = forms.FloatField()
    #content = forms.CharField(widget=forms.Textarea(attrs={'cols': 50, 'rows': 5}), required=False, label='Описание')
    #in_stock = forms.BooleanField(required=False, label='Статус', initial=True)
    cat = forms.ModelChoiceField(queryset=Category.objects.all(), label='Категория', empty_label='Не выбрана')
    person_model = forms.ModelChoiceField(queryset=PersonModel.objects.all(),  required=False, label='Модель', empty_label='Модели нет')

    class Meta:
        model = Item
        fields = ['title', 'slug', 'content', 'photo', 'price', 'in_stock', 'cat', 'person_model', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'cols': 50, 'rows': 5}),
        }
        labels = {
            'slug': 'URL',
        }

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) > 50:
            raise ValidationError("Длина больше 50")
        return title


class UploadFileForm(forms.Form):
    file = forms.ImageField(label='Файл')