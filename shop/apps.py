from django.apps import AppConfig


class ShopConfig(AppConfig):
    verbose_name = "Товары магазина"
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'shop'
