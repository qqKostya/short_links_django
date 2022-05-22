from django.db import models
from hashlib import md5

from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

from graphql import GraphQLError


class URL(models.Model):
    full_url = models.URLField(unique=True)  # URL для сокращения.
    url_hash = models.URLField(unique=True)  # краткий хэш, представляющий полный URL.
    clicks = models.IntegerField(default=0)  # сколько раз был использован короткий URL.
    created_at = models.DateTimeField(auto_now_add=True)  # дата и время создания URL.

    # отслеживаем, сколько раз была использована ссылка
    def clicked(self):
        self.clicks += 1
        self.save()

    # Генерируем url_hash, применив алгоритм хеширования MD5 для поля full_url​​​ и используя только первые 10 символов,
    # которые возвращает метод save() модели, выполняемый каждый раз, когда Django сохраняет запись в базе данных
    def save(self, *args, **kwargs):
        if not self.id:
            self.url_hash = md5(self.full_url.encode()).hexdigest()[:10]

        # этот код инициализирует URLValidator в переменной validate.
        # Внутри блока try/except​​​ с помощью метода validate()​​​ выполняете валидацию полученного URL-адреса
        # и генерируете исключение GraphQLError с заданным сообщением invalid url​​​, если что-то пойдет не так.
        validate = URLValidator()
        try:
            validate(self.full_url)
        except ValidationError as e:
            raise GraphQLError("invalid url")

        return super().save(*args, **kwargs)
