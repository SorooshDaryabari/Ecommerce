from django.http import HttpResponse
from blog.serializers import PostSearchSerializer
from products.serializers import ProductSearchSerializer
from search.documents import ProductDocument, PostDocument
from elasticsearch_dsl import Q
from rest_framework.views import APIView
from rest_framework.pagination import LimitOffsetPagination


class SearchProduct(APIView, LimitOffsetPagination):
    product_serializer = ProductSearchSerializer
    search_document = ProductDocument

    def get(self, request, query=None):
        try:
            q = Q(
                "multi_match",
                query=query,
                fields=[
                    "title",
                    "slug",
                    "category.name",
                    "brand.name",
                ],
                fuzziness="auto",
            ) & Q(
                should=[
                    Q("match", is_default=True),
                ],
                minimum_should_match=1,
            )
            search = self.search_document.search().query(q)
            response = search.execute()

            results = self.paginate_queryset(response, request, view=self)
            serializer = self.product_serializer(results, many=True)
            return self.get_paginated_response(serializer.data)

        except Exception as e:
            return HttpResponse(e, status=500)


class SearchPost(APIView, LimitOffsetPagination):
    post_serializer = PostSearchSerializer
    search_document = PostDocument

    def get(self, request, query=None):
        try:
            q = Q(
                "multi_match",
                query=query,
                fields=[
                    "title",
                    "slug",
                    "category.name",
                ],
                fuzziness="auto",
            ) & Q(
                should=[
                    Q("match", is_default=True),
                ],
                minimum_should_match=1,
            )
            search = self.search_document.search().query(q)
            response = search.execute()
            results = self.paginate_queryset(response, request, view=self)
            serializer = self.post_serializer(results, many=True)
            return self.get_paginated_response(serializer.data)

        except Exception as e:
            return HttpResponse(e, status=500)
