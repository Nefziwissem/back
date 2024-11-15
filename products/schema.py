import graphene
from graphene_file_upload.scalars import Upload
from .models import Product
from graphene_django.types import DjangoObjectType

class ProductType(DjangoObjectType):
    class Meta:
        model = Product
from decimal import Decimal

class CreateProduct(graphene.Mutation):
    product = graphene.Field(ProductType)

    class Arguments:
        name = graphene.String(required=True)
        price = graphene.Float(required=True)  # Vous pouvez garder Float ici pour GraphQL
        image = Upload(required=False)

    def mutate(self, info, name, price, image=None):
        product = Product(name=name, price=Decimal(price))  # Conversion explicite ici
        if image:
            product.image = image
        product.save()
        return CreateProduct(product=product)


class DeleteProduct(graphene.Mutation):
    success = graphene.Boolean()

    class Arguments:
        id = graphene.ID(required=True)

    def mutate(self, info, id):
        try:
            product = Product.objects.get(pk=id)
            product.delete()
            return DeleteProduct(success=True)
        except Product.DoesNotExist:
            return DeleteProduct(success=False)

class UpdateProduct(graphene.Mutation):
    product = graphene.Field(ProductType)

    class Arguments:
        id = graphene.ID(required=True)
        name = graphene.String(required=False)
        price = graphene.Float(required=False)
        image = Upload(required=False)

    def mutate(self, info, id, name=None, price=None, image=None):
        try:
            product = Product.objects.get(pk=id)
            if name:
                product.name = name
            if price:
                product.price = price
            if image:
                product.image = image
            product.save()
            return UpdateProduct(product=product)
        except Product.DoesNotExist:
            return UpdateProduct(product=None)

class Query(graphene.ObjectType):
    all_products = graphene.List(ProductType)

    def resolve_all_products(self, info, **kwargs):
        return Product.objects.all()

class Mutation(graphene.ObjectType):
    create_product = CreateProduct.Field()
    delete_product = DeleteProduct.Field()
    update_product = UpdateProduct.Field()
