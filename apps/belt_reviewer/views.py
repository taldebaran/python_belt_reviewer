from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from models import *
# Create your views here.
def index(request):
    return render(request, 'belt_reviewer/index.html')

def login(request):
    result = User.objects.validateLogin(request)

    if result[0] == False:
        print_messages(request, result[1])
        return redirect(reverse('index'))

    return log_user_in(request, result[1])

def register(request):
    result = User.objects.validateReg(request)

    if result[0] == False:
        print_messages(request, result[1])
        return redirect(reverse('index'))

    return log_user_in(request, result[1])

def books(request):
    if not 'user' in request.session:
        return redirect(reverse('index'))
    context = {
        'recent_books': Review.objects.all().order_by('-created_at')[:3]
    }

    return render(request, 'belt_reviewer/books.html', context)

def new_book(request):
    context = {
        'authors': Author.objects.all()
    }
    return render(request, 'belt_reviewer/new_book.html', context)

def show_book(request, id):
    book = Book.objects.get(id=id)
    context = {
        'book': book,
        'reviews': Review.objects.filter(book=book)
    }
    return render(request, 'belt_reviewer/show_book.html', context)

def del_review(request, id):
    review = Review.objects.get(id=id)
    book = review.book
    review.delete()
    return redirect(reverse('show_book',  kwargs={'id': book.id}))

def create_book_review(request):
    if request.method == 'POST':
        author = request.POST['author']

        if request.POST['custom_author'] != '':
            author = Author.objects.create(name=request.POST['custom_author']).id

        book = Book.objects.create(title=request.POST['title'], \
                                   author_id=author)

        review = Review.objects.create(book=book, \
                                       rating=request.POST['rating'], \
                                       text=request.POST['review'], \
                                       user_id=request.session['user']['id'])
    return redirect(reverse('books'))

def print_messages(request, message_list):
    for message in message_list:
        messages.add_message(request, messages.INFO, message)

def log_user_in(request, user):
    request.session['user'] = {
        'id' : user.id,
        'first_name' : user.first_name,
        'last_name' : user.last_name,
        'email' : user.email,
    }
    return redirect(reverse('books'))

def logout(request):
    request.session.pop('user')
    return redirect(reverse('index'))
