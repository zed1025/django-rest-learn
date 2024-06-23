from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from news.models import Article
from news.api.serializer import ArticleSerializer

# function based views
@api_view(['GET', 'POST'])
def article_list_create_api_view(request):
    if request.method == 'GET':
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True) # many=True to tell the serializer that more than one object is sent
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = ArticleSerializer(data=request.data) # deserialized data
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_404_NOT_FOUND)
    

@api_view(['GET', 'PUT', 'DELETE'])
def article_detail_api_view(request, value_from_url):
    try:
        article = Article.objects.get(id=value_from_url)
    except Article.DoesNotExist:
        return Response(
            {
                "error" : {
                    "code" : 404,
                    "message" : f"There is no such entry with id={value_from_url}."
                }
            },
            status=status.HTTP_404_NOT_FOUND,
        )
    if request.method == 'GET':
        serializer = ArticleSerializer(article) # no need for many= because only one object
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = ArticleSerializer(instance=article, data=request.data) # instance= is the instance in update() method in serializer.py
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        article.delete()
        return Response(
            {
                "process" : {
                    "code" : 204,
                    "message" : f"Article with  id={value_from_url} DELETED!"
                }
            },
            status=status.HTTP_204_NO_CONTENT
        )


