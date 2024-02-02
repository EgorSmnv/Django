from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.template.loader import render_to_string
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, FormView, CreateView, UpdateView, DeleteView

from .forms import AddPostForm, UploadFileForm
from .models import Item, Category, TagPost, UploadFiles
from .utils import DataMixin


class MyClass:
    def __init__(self,a,b):
        self.a = a
        self.b = b


"""def index(request):
    posts = Item.stock.all().select_related('cat')

    data = {
        'title': 'Главная страница',
        'menu': menu,
        'posts': posts,
        'cat_selected': 0,
    }
    return render(request, 'shop/index.html', context=data)"""

class ItemHome(DataMixin, ListView):
    #model = Item
    template_name = 'shop/index.html'
    context_object_name = 'posts'
    title_page = 'Главная страница'
    cat_selected = 0

    def get_queryset(self):
        return Item.stock.all().select_related('cat')


    """def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная страница'
        context['menu'] = menu
        context['posts'] = Item.stock.all().select_related('cat')
        context['cat_selected'] = int(self.request.GET.get('cat_id', 0))
        return context"""

    #def handle_uploaded_file(f):
#    with open(f"uploads/{f.name}", 'wb+') as destination:
#        for chunk in f.chunks():
#            destination.write(chunk)

@login_required
def about(request):
    contact_list = Item.stock.all()
    paginator = Paginator(contact_list, 3)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    """if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            fp = UploadFiles(file=form.cleaned_data['file'])
            fp.save()
    else:
        form = UploadFileForm()"""
    return render(request, 'shop/about.html',
                  {'title': 'abot site', 'page_obj': page_obj})

'''def addpage(request):
    if request.method == 'POST':
        form = AddPostForm(request.POST, request.FILES)
        if form.is_valid():
            #print(form.cleaned_data)

            """try:
                Item.objects.create(**form.cleaned_data)
                return redirect('home')
            except Exception as  E:
                form.add_error(None, "Ошибка добавления")
                print(E)"""
            form.save()
            return redirect('home')
    else:
        form = AddPostForm()

    data = {
        'title': 'Добавление статьи',
        'menu': menu,
        'form': form,
    }
    return render(request, 'shop/addpage.html', data)'''

"""class AddPage(View):
    def get(self, request):
        form = AddPostForm()
        data = {
            'title': 'Добавление статьи',
            'menu': menu,
            'form': form,
        }
        return render(request, 'shop/addpage.html', data)

    def post(self,request):
        form = AddPostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
        data = {
            'title': 'Добавление статьи',
            'menu': menu,
            'form': form,
        }
        return render(request, 'shop/addpage.html', data)"""

class AddPage(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    #model = Item
    #fields = '__all__'
    template_name = 'shop/addpage.html'
    #success_url = reverse_lazy('home')
    title_page = 'Добавление статьи'

    def form_valid(self, form):
        w = form.save(commit=False)
        w.author = self.request.user
        return super().form_valid(form)

class UpdatePage(DataMixin, UpdateView):
    model = Item
    fields = ['title', 'content', 'photo', 'in_stock', 'cat']
    template_name = 'shop/addpage.html'
    success_url = reverse_lazy('home')
    title_page = 'Редактирование статьи'


class DeletePage(DataMixin, DeleteView):
    model = Item
    template_name = 'shop/addpage.html'
    success_url = reverse_lazy('home')
    title_page = 'Удаление записи'


def contact(request):
    return HttpResponse("Обратная связь")

def login(request):
    return HttpResponse("Авторизация")

def show_post(request, post_slug):
    post = get_object_or_404(Item, slug=post_slug)

    data ={
        'name': post.title,
        'post': post,
        'cat_selected': 1,
    }

    return render(request, 'shop/post.html', data)

class ShowPost(DataMixin, DetailView):
    template_name = 'shop/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, title=context['post'].title)

    def get_object(self, queryset=None):
        return get_object_or_404(Item.stock, slug=self.kwargs[self.slug_url_kwarg])

def show_category(request, cat_slug):
    category = get_object_or_404(Category, slug=cat_slug)
    posts = Item.stock.filter(cat_id=category.pk).select_related('cat')

    data = {
        'title': f'Категория: {category.name}',
        'posts': posts,
        'cat_selected': category.pk,
    }
    return render(request, 'shop/index.html', context=data)

class ItemCategory(DataMixin, ListView):
    template_name = 'shop/index.html'
    context_object_name = 'posts'
    allow_empty = False


    def get_queryset(self):
        return Item.stock.filter(cat__slug=self.kwargs['cat_slug']).select_related('cat')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cat = context['posts'][0].cat
        return self.get_mixin_context(context,
                                      title='Категория - ' + cat.name,
                                      cat_selected=cat.pk
                                      )


def categories(request, cat_id):
    return HttpResponse(f"<h1>Категории</h1><p> id: {cat_id}</p>")

def categories_by_slug(request, cat_slug):
    print(request.GET)
    return HttpResponse(f"<h1>Категории</h1><p> slug: {cat_slug}</p>")

def archive(request, year):
    if year > 2023:
        uri = reverse('cats', args=('music',))
        return HttpResponseRedirect(uri)
    return HttpResponse(f"<h1>Архив по годам</h1><p> {year}</p>")


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Старница не найдена</h1>")


def show_tag_postlist(request, tag_slug):
    tag = get_object_or_404(TagPost, slug=tag_slug)
    posts = tag.tags.filter(in_stock=Item.Status.STOCK).select_related('cat')

    data= {
        'title': f"Tag: {tag.tag}",
        'posts': posts,
        'cat_selected': None,
    }

    return render(request, 'shop/index.html', context=data)

class TagPostList(DataMixin, ListView):
    template_name = 'shop/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Item.stock.filter(tags__slug=self.kwargs['tag_slug']).select_related('cat')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #tag = TagPost.objects.get(pk=context['posts'][0].tags.through.objects.all()[0].tagpost_id)
        tag = context['posts'][0].tags.all()[0]
        return self.get_mixin_context(context, title='Тэг - ' + tag.tag)
