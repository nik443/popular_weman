from django.db import models
from django.urls import reverse

class Women(models.Model):
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    content = models.TextField(blank=True, verbose_name="Текст статьи")
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", verbose_name="Фото")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Время изменения")
    is_published = models.BooleanField(default=True, verbose_name="Публикация")
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name="Категории") # related_name='get_posts' можно указать еще такой параметр чтобы получать все записи из первичной таблице связанные со вторичной, например: Category.objects.get(pk=1).get_posts.all(). По умол для этого используется запись Category.objects.get(pk=1).women_set.all() (имя модели + _set)

    def __str__(self): # метод нужен для вывода в консоль объекта с его title при вызове например, Women.objects.all()
        return self.title

    # такой тип создания ссылок применять только тогда, когда ссылки связаны с записями в БД
    def get_absolute_url(self): # self - ссылка на экземпляр класса Women (на одну запись в БД)
        return reverse('post', kwargs={'post_slug': self.slug})

    class Meta: # Этот подкласс отвечает за отображение данной модели в админ-панели и соответвенно при выводе их оттуда
        verbose_name = 'Известные женщины' # название модели в админ панели
        verbose_name_plural = 'Известные женщины' # название модели во множественном числе (джанго по умолч. добавляет к verbose_name букву s в конце для этого)
        ordering = ['pk'] # сортировка экземпляров модели (по умолч. по возр.) Чтобы по убыв ставится - (минис). Это св-во нужно отключать для того, чтобы корректно выполнять запросы ORM к БД с конструкцией GROUP BY. Для пагинации свойство желательно должно быть включено (хотя бы по id)


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name="Категория")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")

    def __str__(self): # при вызове из связанной таблице вернет поле title, например: Women.objects.get(pk=1).cat - вернет "актрисы"
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['id']
