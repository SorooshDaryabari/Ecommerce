from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from products.models import Product
from blog.models import Post


@registry.register_document
class ProductDocument(Document):
    category = fields.ObjectField(
        properties={
            "name": fields.TextField(),
        }
    )
    brand = fields.ObjectField(
        properties={
            "name": fields.TextField(),
        }
    )

    class Index:
        name = "products"
        settings = {
            "number_of_shards": 1,
            "number_of_replicas": 0,
        }

    class Django:
        model = Product
        fields = (
            "title",
            "slug",
            "regular_price",
            "discount_price",
            "short_description",
        )


@registry.register_document
class PostDocument(Document):
    category = fields.ObjectField(
        properties={
            "name": fields.TextField(),
        }
    )

    class Index:
        name = "posts"
        settings = {
            "number_of_shards": 1,
            "number_of_replicas": 0,
        }

    class Django:
        model = Post
        fields = (
            "title",
            "short_description",
        )
