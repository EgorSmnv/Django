from django.contrib import admin, messages
from django.utils.safestring import mark_safe

from shop.models import Item, Category, PersonModel


class PersonModelFilter(admin.SimpleListFilter):
    title = "Статус модели"
    parameter_name = "status"

    def lookups(self, request, model_admin):
        return [
            ('have', 'Есть'),
            ('empty', 'Отсутствует'),
        ]

    def queryset(self, request, queryset):
        if self.value() == 'have':
            return queryset.filter(person_model__isnull=False)
        elif self.value() == 'empty':
            return queryset.filter(person_model__isnull=True)

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    fields = ['title', 'content', 'photo', 'post_photo', 'price', 'slug', 'cat', 'person_model', 'tags', 'author']
    readonly_fields = ['post_photo']
    prepopulated_fields = {"slug": ('title', )}
    #filter_horizontal = ['tags',]
    filter_vertical = ['tags',]
    list_display = ("title", 'post_photo', "time_create", "in_stock", "cat")
    list_display_links = ('title',)
    ordering = ['time_create', 'title']
    list_editable = ('in_stock',)
    list_per_page = 5
    actions = ['set_stock', 'set_draft',]
    search_fields = ['title', 'cat__name']
    list_filter = [PersonModelFilter, 'cat__name', 'in_stock',]
    save_on_top = True

    @admin.display(description="Краткое описание", ordering="content")
    def brief_info(self, item: Item):
        return f"Описание {len(item.content)} символов."

    @admin.display(description='Фото')
    def post_photo(self, item: Item):
        if item.photo:
            return mark_safe(f"<img src='{item.photo.url}' width=50>")
        return "Без фото"

    @admin.action(description="Установить в наличие")
    def set_stock(self, request, queryset):
        count = queryset.update(in_stock=Item.Status.STOCK)
        self.message_user(request, f"Изменено {count} записей.")

    @admin.action(description="Убрать из наличия")
    def set_draft(self, request, queryset):
        count = queryset.update(in_stock=Item.Status.DRAFT)
        self.message_user(request, f"Убрано с наличия {count} записей.", messages.WARNING)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    list_display_links = ('id', 'name')


@admin.register(PersonModel)
class PersonModelAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    list_display_links = ('id', 'name')
#admin.site.register(Item, ItemAdmin)