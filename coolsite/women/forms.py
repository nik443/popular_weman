from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from captcha.fields import CaptchaField

from .models import *

# В форме прописываем только те поля, которые необходимо отобразить для конечного пользователя
# Если форма не связанна с моделью, то наследуем класс forms.Form. А если связана - forms.ModelForm
class AddPostForm(forms.ModelForm):

    # Конструктор модифицировали для того, чтобы у поля cat заменить невыбранную категорию (---) на 'категория не выбрана'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cat'].empty_label = 'Категория не выбрана'

    class Meta: # с помощью класса Meta мы расширяем родительский класс
        model = Women # на какую модель ссылается
        fields = ['title', 'slug', 'content', 'photo', 'is_published', 'cat'] # какие поля отобразить в форме. Если необходимо указать все поля кроме тех которые заполняются автоматичести то: '__all__'. Можно менять последовательность полей
        widgets = { # здесь указываем для какого поля формы будем применять стиль
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'cols': 60, 'rows': 10})
        }

    # пользовательская валидация, происходит после встроенной (у функций save() и is_valid())
    # функция должна начинаться с clean_ + то поле для которого мы делаем валидацию
    def clean_title(self): 
        title = self.cleaned_data['title']
        if len(title) > 200:
            raise ValidationError('Длина превышает 200 символов')
        return title


class RegisterUserForm(UserCreationForm): # UserCreationForm - класс, который работает по умочланию с формой работающей с таблицей auth_user
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Повтор пороля', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = User # User - стандартная модель, которая работает с таблицей auth_user
        fields = ('username', 'email', 'password1', 'password2') # имена этих полей можно посмотреть в админке в коде странице


class LoginUserForm(AuthenticationForm): # AuthenticationForm - встроенная форма django для авторизации. Если необходимы дополнительные поля, то указываем их аналогично
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

class ContactForm(forms.Form):
    name = forms.CharField(label='Имя', max_length=255)
    email = forms.EmailField(label='Email')
    content = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 10}))
    captcha = CaptchaField()
