from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login$', views.login, name='login'),
    url(r'^register$', views.register, name='register'),
    url(r'^books$', views.books, name='books'),
    url(r'^books/(?P<id>\d+)$', views.show_book, name='show_book'),
    url(r'^review/del/(?P<id>\d+)$', views.del_review, name='del_review'),
    url(r'^books/add$', views.new_book, name='new_book'),
    url(r'^create_book_review$', views.create_book_review, name='create_book_review'),
    url(r'^logout$', views.logout, name='logout'),
]
