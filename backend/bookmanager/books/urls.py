from django.urls import path
from . import views

urlpatterns = [
    path('', views.book_list_create, name='book_list_create'),
    path('<int:pk>/', views.book_detail, name='book_detail'),
    path('autocomplete/', views.book_autocomplete, name='book_autocomplete'),

    # http://127.0.0.1:8000/book/autocomplete/?title=Идиот 

    
    path('roots/<int:root_id>/books/', views.books_by_root, name='books_by_root'),
    path('racks/<int:rack_id>/books/', views.books_by_rack, name='books_by_rack'),
    path('sections/<int:section_id>/books/', views.books_by_section, name='books_by_section'),
]
