from django.shortcuts import render

from django.shortcuts import get_object_or_404, redirect

from .models import URL


# Он получает аргумент с именем url_hash из URL, запрошенного пользователем. 
# Внутри функции первая строка пытается получить URL из базы данных, используя аргумент url_hash. 
# Если он не будет найден, клиент получает ошибку 404, что означает, что ресурс отсутствует. 
# Затем он увеличивает значение свойства clicked для URL, что позволяет отслеживать, сколько раз был использован URL. 
# В конце он перенаправляет клиента на запрошенный URL-адрес.
def root(request, url_hash):
    url = get_object_or_404(URL, url_hash=url_hash)
    url.clicked()

    return redirect(url.full_url)
