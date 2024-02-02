from django.contrib import admin
from django.urls import path, include, re_path, register_converter

from . import views
from . import converters

register_converter(converters.FourDigitYearConverter, "year4")


urlpatterns = [
    path('', views.ItemHome.as_view(), name='home'),
    path('about/', views.about, name="about"),
    path('addpage/', views.AddPage.as_view(), name='add_page'),
    path('contact/', views.contact, name='contact'),
    path('login/', views.login, name='login'),
    path('post/<slug:post_slug>/', views.ShowPost.as_view(), name='post'),
    path('category/<slug:cat_slug>/', views.ItemCategory.as_view(), name='category'),
    path('tag/<slug:tag_slug>/', views.TagPostList.as_view(), name='tag'),
    path('edit/<slug:slug>/', views.UpdatePage.as_view(), name='editpage'),
    path('delete/<slug:slug>/', views.DeletePage.as_view(), name='deletepage'),
]