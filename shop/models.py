from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse

def translit_to_eng(s: str) -> str:
    d = {
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo',
        'ж': 'zh', 'з': 'zh', 'и': 'i', 'й': 'iy', 'к': 'k', 'л': 'l',
        'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't',
        'у': 'u', 'ф': 'f', 'х': 'h', 'ц': 'c', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch',
        'ъ': '', 'ы': 'y', 'ь': '', 'э': 'e', 'ю': 'yu', 'я': 'ya',
    }
    return ''.join(map(lambda x: d[x] if d.get(x, False) else x, s.lower()))
class StockManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(in_stock=Item.Status.STOCK)



class Item(models.Model):
    class Status(models.IntegerChoices):
        DRAFT = 0, 'Отсутствует'
        STOCK = 1, 'В наличии'

    title = models.CharField(max_length=100, verbose_name="Заголовок")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="slug")
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', default=None, blank=True,
                              null=True, verbose_name='Фото')
    content = models.CharField(max_length=255, verbose_name="Текст описания")
    price = models.FloatField(blank=True, verbose_name="Цена")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Время обновления")
    in_stock = models.BooleanField(choices=tuple(map(lambda x: (bool(x[0]), x[1]), Status.choices)),
                                   default=Status.STOCK, verbose_name="Наличие")
    cat = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='posts', verbose_name="Категория")
    tags = models.ManyToManyField('TagPost', blank=True, related_name='tags', verbose_name="Тэг")
    person_model = models.OneToOneField('PersonModel', on_delete=models.SET_NULL, null=True, blank=True,
                                        related_name='item', verbose_name="Модель примерки")
    author = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL,
                               related_name='posts', null=True, default=None)


    objects = models.Manager()
    stock = StockManager()


    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})

    #def save(self, *args, **kwargs):
        #self.slug = slugify(translit_to_eng(self.title))
        #super().save(*args, **kwargs)


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Категория")
    slug = models.SlugField(max_length=50, unique=True, db_index=True, verbose_name="slug")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})


class TagPost(models.Model):
    tag = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    def __str__(self):
        return self.tag

    def get_absolute_url(self):
        return reverse('tag', kwargs={'tag_slug': self.slug})


class PersonModel(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField(null=True)
    m_count = models.IntegerField(blank=True,default=0)

    def __str__(self):
        return self.name


class UploadFiles(models.Model):
    file = models.FileField(upload_to='uploads_model')