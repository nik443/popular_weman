from django.apps import AppConfig


class WomenConfig(AppConfig): # этот класс используется для конфигурации всего приложения
    name = 'women'
    verbose_name = 'Женщины мира' # альтернативное имя приложения, так оно будет отображаться в админ-панели
