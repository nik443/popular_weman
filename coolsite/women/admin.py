from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import *

# Register your models here - регистрация моделей для возможности их редактирования в админ-панели

class WomenAdmin(admin.ModelAdmin): # в этом классе можно описать отображение модели в админ-панели
    list_display = ('id', 'title', 'time_create', 'get_html_photo', 'is_published') # список полей, которые хотим видеть в админ-панеле
    list_display_links = ('id', 'title') # те поля, по которым мы можем кликнуть и перейти на соотв. запись в админ-панеле
    search_fields = ('title', 'content') # по каким полям будет возномен поиск той или иной информации в админ-панеле
    list_editable = ('is_published',) # поля, которые будут редактируемы непосредственно из списка записей в админ-панеле
    list_filter = ('is_published', 'time_create') # список полей, по которым можно будет фильтровать записи в админ-панеле
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ('time_create', 'time_update', 'get_html_photo') # не радактируемые поля при отображение в админ-панеле
    fields = ('title', 'slug', 'cat', 'content', 'photo', 'is_published', 'get_html_photo', 'time_create', 'time_update') # порядок редактируемых полей при редактировании отдельной записи
    save_on_top = True # установить панель сохранения еще и в верху страницы (по умолч. только внизу)

    # эта пользовательская ф-ия позволяет получить фото при отображении списка объектов Women в админке
    def get_html_photo(self, object): # object - ссылается на текущую запись списка
        if object.photo:
            return mark_safe(f"<img src='{object.photo.url}' width=50>") # mark_safe позволяет не экранировать теги внутри 
        
    get_html_photo.short_description = 'Миниатюра' # заголовок для get_html_photo в админке


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',) # мы должны передавать кортеж, поэтому нужна запятая в конце
    prepopulated_fields = {"slug": ("name",)} # поле слага будет заполнятся автоматически после добавления в БД в админ-панеле


admin.site.register(Women, WomenAdmin) # регистрация приложения в админ-панеле, первым параметром - сама моледь, вторым - вспомогательный класс
admin.site.register(Category, CategoryAdmin)

admin.site.site_title = 'Админ-панель сайта о женщинах' # переопределение контента в заголовках в админке
admin.site.site_header = 'Админ-панель сайта о женщинах'