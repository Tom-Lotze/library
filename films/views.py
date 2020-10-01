from django.shortcuts import render, redirect
from django.utils import timezone
from .models import Film, Genre, Actor
from .scrape import scrape_imdb


# Create your views here.


def index(request):

    all_films = Film.objects.all()

    nrFilms = len(all_films)
    watchList = all_films.filter(status="TODO")
    seenFilms = all_films.filter(status="SEEN")

    context = dict()

    context["all_films"] =  all_films
    context["seenFilms"] = seenFilms
    context["watchList"] = watchList

    context['tenFilms'] = all_films[:10]
    context["nrFilms"] = nrFilms
    context['nrSeen'] = len(seenFilms)
    context["seenThisYear"] = len(seenFilms.filter(modified__year = timezone.now().year))
    context['genres'] = Genre.objects.all()


    context['hoursSeen'] = round(sum([f.duration.seconds for f in seenFilms])/3600, 1)
    context['hoursSeenYear'] = round(sum([f.duration.seconds for f in seenFilms if f.modified.year==timezone.now().year])/3600, 1)


    return render(request, 'films/index.html', context=context)



def search(request):
    imdb_url = request.GET['url']

    info = scrape_imdb(imdb_url)

    if info == 1:
        context = {'failure': True, 'imdburl': imdb_url}
        return render(request, 'films/search.html', context=context)


    return render(request, 'films/search.html', context=info)



def favorite(request, film_id):
    f = Film.objects.get(id=film_id)

    if f.favorite:
        f.favorite = False
    else:
        f.favorite = True
    f.save()

    return detail(request, film_id)


def detail(request, film_id):

    f = Film.objects.get(id=film_id)
    context = {'f': f, 'rating_loop': range(1, 6)}

    if f.favorite:
        context['favorite'] = True

    context['currList'] = f.status

    return render(request, 'films/detail.html', context=context)

def genre(request, genre_id):
    context = dict()


    genre = Genre.objects.get(id=genre_id)
    context['name'] = genre.genre
    context['films'] = genre.film_set.all()


    return render(request, 'films/genre.html', context=context)

def actor(request, actor_id):
    actor = Actor.objects.get(id=actor_id)
    context = dict()
    context['name'] = actor.name
    context['films'] = actor.film_set.all()
    context['url'] = actor.url


    return render(request, 'films/actor.html', context=context)


def delete(request, film_id):
    f = Film.objects.get(id=film_id)

    f.delete()

    return redirect("/films")


def changeStatus(request, film_id):
    choice = request.POST['list']

    # change current list in database
    f = Film.objects.get(id=film_id)
    f.status = choice
    f.save()

    return detail(request, film_id)


def changeRating(request, film_id):
    rating = request.POST['rating']

    # change current list in database
    f = Film.objects.get(id=film_id)
    f.ownRating = rating
    f.save()

    return detail(request, film_id)


def listview(request, list_id):
    context = dict()

    context['listview'] = True
    all_films = Film.objects.all()
    # all
    if list_id == 0:
        context['name'] = "All Films"
        context['films'] = all_films
    # watchlist
    elif list_id == 1:
        context['name'] = "Watchlist"
        context['films'] = all_films.filter(status="TODO")
    # seen
    elif list_id == 2:
        context['name'] = "Seen Films"
        context['films'] = all_films.filter(status="SEEN")



    return render(request, 'films/genre.html', context = context)




def review(request, film_id):
    f = Film.objects.get(id=film_id)

    f.review = request.POST["review"]
    f.save()

    return detail(request, film_id)


def searchDB(request):
    q = request.GET['title']

    results = Film.objects.all().filter(title__icontains=q)
    context = dict()
    context['results'] = results
    context['query'] = q

    return render(request, 'films/results.html', context=context)



