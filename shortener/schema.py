import graphene
from graphene_django import DjangoObjectType
from django.db.models import Q

from .models import URL





# Создаем новый тип GraphQL для модели URL
class URLType(DjangoObjectType):
    class Meta:
        model = URL



# Этот код создает класс Query с одним полем urls, 
# который представляет собой список с ранее определенным типом URLType. 
# При обработке запроса с помощью метода resolve_urls вы возвращаете все URL, сохраненные в базе данных.
class Query(graphene.ObjectType):
    urls = graphene.List(URLType, url=graphene.String(), first=graphene.Int(), skip=graphene.Int())

    def resolve_urls(self, info, url=None, first=None, skip=None, **kwargs):
        queryset = URL.objects.all()

        if url:
            _filter = Q(full_url__icontains=url)
            queryset = queryset.filter(_filter)

        if first:
            queryset = queryset[:first]

        if skip:
            queryset = queryset[skip:]

        return queryset



'''
Этот класс наследует вспомогательный класс graphene.Mutation для использования возможностей мутаций GraphQL. 
Также у него есть имя свойства url, определяющее содержание, возвращаемое сервером после завершения мутации.
В этом случае это структура данных с типом URLType.
'''
class CreateURL(graphene.Mutation):
    url = graphene.Field(URLType)

    # Он определяет, какие данные будут приниматься сервером. 
    # Здесь мы ожидаете параметр full_url со строковым содержанием
    class Arguments:
        full_url = graphene.String()


    # Этот метод mutate выполняет большой объем работы, получая данные от клиента и сохраняя их в базу данных. 
    # В результате он возвращает сам класс, содержащий вновь созданный элемент.
    def mutate(self, info, full_url):
        url = URL(full_url=full_url)
        url.save()


# класс Mutation для хранения всех мутаций приложения
class Mutation(graphene.ObjectType):
    create_url = CreateURL.Field()