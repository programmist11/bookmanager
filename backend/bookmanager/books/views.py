import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Book
from .serializers import BookSerializer

# ---------------------------
# CRUD для книг
# ---------------------------
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

# ---------------------------
# Автозаполнение через Google Books
# ---------------------------
@api_view(['GET'])
def book_autocomplete(request):
    query = request.GET.get('title', '')
    if not query:
        return Response([])

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
                "isbn": isbn_13
            })

        return Response(books)
    except Exception:
        return Response([], status=500)

# ---------------------------
# Выборка книг по библиотеке / стеллажу / полке
# ---------------------------
@api_view(['GET'])
def books_by_root(request, root_id):
    """
    Все книги конкретной библиотеки (root)
    """
    books = Book.objects.filter(section__rack__root_id=root_id)
    serializer = BookSerializer(books, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def books_by_rack(request, rack_id):
    """
    Все книги конкретного стеллажа (rack)
    """
    books = Book.objects.filter(section__rack_id=rack_id)
    serializer = BookSerializer(books, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def books_by_section(request, section_id):
    """
    Все книги конкретной полки (section)
    """
    books = Book.objects.filter(section_id=section_id)
    serializer = BookSerializer(books, many=True)
    return Response(serializer.data)
