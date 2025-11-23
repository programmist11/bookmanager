import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Book
from .serializers import BookSerializer


@api_view(['GET', 'POST'])
def book_list_create(request):
    if request.method == 'GET':
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def book_detail(request, pk):
    try:
        book = Book.objects.get(pk=pk)
    except Book.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = BookSerializer(book)
        return Response(serializer.data)

    if request.method == 'PUT':
        serializer = BookSerializer(book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def book_autocomplete(request):
    query = request.GET.get('title', '')
    if not query:
        return Response([])

    # Запрос к Google Books
    url = "https://www.googleapis.com/books/v1/volumes"
    params = {
        "q": f"intitle:{query}",
        "langRestrict": "ru",
        "maxResults": 15
    }

    try:
        r = requests.get(url, params=params)
        data = r.json()

        books = []
        for item in data.get("items", []):
            volume = item.get("volumeInfo", {})

            # Достаем ISBN-13
            isbn_13 = next(
                (id_info['identifier'] for id_info in volume.get("industryIdentifiers", [])
                 if id_info.get('type') == "ISBN_13"),
                None
            )

            books.append({
                "title": volume.get("title"),
                "author": ", ".join(volume.get("authors", [])),
                "year": volume.get("publishedDate", "")[:4],
                "genre": ", ".join(volume.get("categories", [])),
                "description": volume.get("description", ""),
                "cover": volume.get("imageLinks", {}).get("thumbnail", ""),
                "pages": volume.get("pageCount"),
                "isbn": isbn_13  # только ISBN-13
            })

        return Response(books)

    except Exception as e:
        return Response([], status=500)
