from django.shortcuts import render, redirect
from .search import scrape, google_books_api_request, api2book
from .models import Book, Author
from django.utils import timezone
from django.db.models import Q

# Create your views here.

def index(request):

    context = get_index_context()

    return render(request, 'books/index.html', context = context)

def get_index_context():
    all_books = Book.objects.all()

    context = {"all_books" : all_books}
    context['tenBooks'] = all_books[:10]

    readBooks = all_books.filter(status="READ")
    wishBooks = all_books.filter(status="WISH")
    currBooks = all_books.filter(status="CURR")
    todoBooks = all_books.filter(status="TODO")
    favorites = all_books.filter(favorite=True)

    # determine how many books are read this year
    current_year = timezone.now().year
    read_this_year = readBooks.filter(modified__year=current_year)
    pagesRead = sum([book.nrPages for book in readBooks])
    pagesReadThisYear = sum([book.nrPages for book in read_this_year])
    context['pagesRead'] = pagesRead
    context['pagesReadThisYear'] = pagesReadThisYear

    # for v in ['var']:
    #     eval(f"contex['{v}'] = v")
    context['readBooks'] = readBooks
    context['wishBooks'] = wishBooks
    context['currBooks'] = currBooks
    context['todoBooks'] = todoBooks
    context['favorites'] = favorites

    # put number of books per category in context
    context['nrReadBooks'] = len(readBooks)
    context['nrWishBooks'] = len(wishBooks)
    context['nrCurrBooks'] = len(currBooks)
    context['nrTodoBooks'] = len(todoBooks)
    context['nrFavorites'] = len(favorites)


    context['nrReadThisYear'] = len(read_this_year)

    context['searchResults'] = []

    return context


def search(request, topk=3):
    """
    This function should return multiple books for the query, and show them
    on the index page, below the search block. The user should be able to click the books to add them to the library: the information is already retrieved. To retrieve the results, the google_books_api_request function is used
    """
    query = request.GET['query']
    results = google_books_api_request(query, topk=topk)

    # the results should be a dictionary with the number of results as a key, and for each result a key with all the information.

    context=get_index_context()

    # if no results are retrieved, set search results to -1
    if results == 1:
        context['searchResults'] = "1"
        return render(request, 'books/index.html', context=context)

    for i in range(1, results['n_results']+1):
        context['searchResults'].append(api2book(results[i]))

    return render(request, 'books/index.html', context=context)


def add(request):
    # scrape the bol.com page
    bol_url = request.GET['url']

    info = scrape(bol_url)

    # url failed
    if info == 1:
        context = {"failure": True, 'bolurl': bol_url}
        return render(request, 'books/search.html', context=context)


    book = Book(**info)
    try:
        book.save()
        info['id'] = book.id
    except:
        info['duplicate'] = True
        info['id'] = Book.objects.get(title=book.title).id


    return render(request, 'books/search.html', context=info)


def detail(request, book_id):
    """Redirects to a page for a specific book"""

    # retrieve the book from the database and pass as context
    b = Book.objects.get(id=book_id)

    context = {'b': b, 'rating_loop': range(1, 6)}

    # context['humanLists'] = [item[1] for item in b.statuschoices]
    # context['machineLists'] = [item[0] for item in b.statuschoices]
    if b.favorite:
        context['favorite'] = True

    context['currList'] = b.status

    return render(request, 'books/detail.html', context=context)


def changeList(request, book_id):
    choice = request.POST['list']

    # change current list in database
    b = Book.objects.get(id=book_id)
    b.status = choice
    b.save()

    return detail(request, book_id)

def changeRating(request, book_id):
    rating = request.POST['rating']

    # change current list in database
    b = Book.objects.get(id=book_id)
    b.rating = rating
    b.save()

    return detail(request, book_id)


def favorite(request, book_id):
    b = Book.objects.get(id=book_id)

    if b.favorite:
        b.favorite = False
    else:
        b.favorite = True
    b.save()

    return detail(request, book_id)

def listview(request, list_id):

    all_books = Book.objects.all()
    context = dict()

    # Favorites list
    if list_id == 5:
        books = all_books.filter(favorite=True)
        name = "Favorites"
    elif list_id ==6:
        books = all_books
        name = "All books"
    else:
        choice_tuple = Book.statuschoices[list_id-1]
        machine_status = choice_tuple[0]
        name = choice_tuple[1]
        books = all_books.filter(status=machine_status)

    context['name'] = name
    context['books'] = books

    return render(request, "books/listview.html", context=context)


def delete(request, book_id):
    b = Book.objects.get(id=book_id)

    b.delete()

    return redirect("/books")


def review(request, book_id):
    b = Book.objects.get(id=book_id)

    b.review = request.POST["review"]
    b.save()

    return detail(request, book_id)


def searchDB(request):
    q = request.GET['query']
    context = dict()
    context['name'] = f"Search results for: {q}"
    context['books'] = Book.objects.all().filter(Q(title__icontains=q) | Q(authors__icontains=q))

    return render(request, "books/listview.html", context=context)











