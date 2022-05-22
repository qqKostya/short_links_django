import graphene

import shortener.schema


# главный класс Query. Он будет хранить, через наследование, все запросы и будущие операции
class Query(shortener.schema.Query, graphene.ObjectType):
    pass


class Mutation(shortener.schema.Mutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
