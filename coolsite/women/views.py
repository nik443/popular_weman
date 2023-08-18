from typing import Any, Dict
# from django.contrib.auth.forms import UserCreationForm - стандартная форма регистрации пользователя
from django.db.models.query import QuerySet
from django.forms.models import BaseModelForm
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView # ListView - список постов, DetailView - отображение отдельного поста, CreateView - для добавления новой записи в БД
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin # встроенный в django миксин, позволяющий получить доступ к странице только авторизованным пользователям
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout, login
from django.core.paginator import Paginator

from .models import *
from .forms import *
from .utils import *

# этот класс представлений идиально подходит для отображения списка записей
class WomenHome(DataMixin, ListView): # в этот класс уже встроена пагинация. Если в классе используется пагинации, то класс автоматически передает в context параметры: paginator и page_obj, которые содержат список объектов для текущей страницы 
    model = Women # связываем с моделью Women
    template_name = 'women/index.html' # имя подключаемого шаблона
    context_object_name = 'posts' # имя переменной, которой будет передан список объектов Women

    def get_context_data(self, **kwargs): # с помощью этой встроенной ф-ии можно передать параметры в шаблон
        context = super().get_context_data(**kwargs) 
        c_def = self.get_user_context(title='Главная страница')
        return dict(list(context.items()) + list(c_def.items()))
    
    def get_queryset(self): # эта функция фильтрует получаемые из БД объекты Women (изначально получаем все объекты в model а далее уже их фильтруем с помощью этой функции)
        return Women.objects.filter(is_published=True).select_related('cat') # .select_related('cat') позволяет подгружать еще и данные из таблицы category по внешнему ключу cat, делается это для того чтобы не происходило дублирование отложенных запросов к БД. Этот метод подходит для связи "один ко многим"


def about(request): 
    # Использование пагинации в функция-представлений немного сложнее, чем в классах
    contact_list = Women.objects.all()
    paginator = Paginator(contact_list, 3) # 3 - кол-во объектов, которое будет размещено на стр
    page_number = request.GET.get('page') # получаем номер страницы, которая должна быть представлена (для пагинации)
    page_obj = paginator.get_page(page_number) # получаем страницу, которая должна быть представлена

    return render(request, 'women/about.html', {
        'page_obj': page_obj, 'menu': menu, 'title': 'О сайте'})


class AddPage(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm # имя класса формы, с которой будет работать наш класс
    template_name = 'women/addpage.html'
    success_url = reverse_lazy('home') # выполняет построение маршрута только тогда, когда он понадобится и когда он будет существовать. В момент добавления записи маршрут еще не существует, поэтому обычная ф-ия reverse здесь не поможет
    login_url = reverse_lazy('home') # (это атрибут встроенного миксина LoginRequiredMixin) в случае если пользователь не авторизован, то он будет перенаправлен по этому адресу 
    raise_exception = True # (это атрибут встроенного миксина LoginRequiredMixin) в случае если пользователь не авторизован, то будет выбрашено исключение 403 (доступ запрещен)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Добавить статью')
        return dict(list(context.items()) + list(c_def.items()))


class ContactFormView(DataMixin, FormView):
    form_class = ContactForm
    template_name = 'women/contact.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Обратная связь')
        return dict(list(context.items()) + list(c_def.items()))
    
    def form_valid(self, form):
        print(form.cleaned_data)
        return redirect('home')


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')


class ShowPost(DataMixin, DetailView):
    model = Women
    template_name = 'women/post.html'
    slug_url_kwarg = 'post_slug' # переменная для получения слага записи
    # pk_url_kwarg = 'post_pk' # переменная для получения id записи
    context_object_name = 'post' # в эту переменную помещается объект записи

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['post'])
        return dict(list(context.items()) + list(c_def.items()))


class WomenCategory(DataMixin, ListView):
    model = Women 
    template_name = 'women/index.html' 
    context_object_name = 'posts'
    allow_empty = False # если список posts будет пуст (не найдет ни одной записи в БД), то выдаст ошибку 404 и нижестоящие ф-ии не выполнятся

    def get_queryset(self):
        return Women.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True) # через словарь kwargs можем получить все, передаваемые при переходе на страницу, параметры. Конструкция cat__slug говорит о том, что через поле cat модели Women мы связываемся с полем slug модели Category

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 
        c = Category.get(slug=self.kwargs['cat_slug'])
        c_def = self.get_user_context(title='Категория - ' + str(c.name), # cat - объект, хранящий название категории
                                        cat_selected = c.pk)     
        return dict(list(context.items()) + list(c_def.items()))


class RegisterUser(DataMixin, CreateView): # CreateView - класс, необходимый для занесения данных с формы в БД
    form_class = RegisterUserForm # класс для работы с формой (еще есть класс UserCreationForm он встроенный, поля можно посмотреть в таблице auth_user)
    template_name = 'women/register.html'
    success_url = reverse_lazy('login') # перенаправление пользователя в случае успешной регистрации

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Регистрация')
        return dict(list(context.items()) + list(c_def.items()))
    
    def form_valid(self, form): # встроенный метод django - вызывается в случае успешной проверки формы регистрации (по задамке при успешной регистрации надо сразу и авторизировать пользователя)
        user = form.save() # сохранение формы в БД
        login(self.request, user) # авторизация пользователя
        return redirect('home')
    

class LoginUser(DataMixin, LoginView): # LoginView - встроенный класс для авторизации пользователей
    form_class = LoginUserForm
    template_name = 'women/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Авторизация')
        return dict(list(context.items()) + list(c_def.items()))
    
    def get_success_url(self): # функция перенаправления пользователя в случае успешной авторизации
        return reverse_lazy('home')
    

def logout_user(request):
    logout(request) # встроенная ф-ия django позволяющая пользователю выйти из авторизованного аккаунта
    return redirect('login') # по какому маршруту происходит перенаправление