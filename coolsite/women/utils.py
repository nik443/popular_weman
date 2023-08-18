# В этом файле прописаны миксины (премиси к классам-представлениям)
from django.db.models import Count

from women.models import *

menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить статью", 'url_name': 'add_page'},
        {'title': "Обратная связь", 'url_name': 'contact'},
]

class DataMixin:
    paginate_by = 2 # кол-во объектов women, которое будет размещено на странице

    def get_user_context(self, **kwargs):
        context = kwargs
        cats = Category.objects.annotate(Count('women')) 

        # эта часть кода делает так, что неавторизованный пользователь не увидит пункт меню "Добавить статью"
        user_menu = menu.copy()
        if not self.request.user.is_authenticated:
            user_menu.pop(1)
        context['menu'] = user_menu

        context['cats'] = cats
        if 'cat_selected' not in context:
            context['cat_selected'] = 0
        return context
