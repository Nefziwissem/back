# products/schema.py
import graphene
from graphene_django.types import DjangoObjectType
from .models import Product

class ProductType(DjangoObjectType):
    class Meta:
        model = Product

class Query(graphene.ObjectType):
    all_products = graphene.List(ProductType)

    def resolve_all_products(self, info, **kwargs):
        return Product.objects.all()

class CreateProduct(graphene.Mutation):
    product = graphene.Field(ProductType)

    class Arguments:
        name = graphene.String(required=True)
        price = graphene.Float(required=True)
        image = graphene.String(required=False)  # Handle image uploading separately

    def mutate(self, info, name, price, image=None):
        product = Product(name=name, price=price, image=image)
        product.save()
        return CreateProduct(product=product)

class Mutation(graphene.ObjectType):
    create_product = CreateProduct.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
