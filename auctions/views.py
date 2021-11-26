# TODO
#   [X] Add a new list
#   [x] Show actives lists
#   [X] Filter by category
#   [X] Open a list by clicking the title
#   [] Show all watched list for the current user
#   [X] Make a bid for the current for an auction list
#
#


from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.forms.models import modelformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse

from .forms import *
from .models import *
import logging

logger = logging.getLogger(__name__)

# Default Home Page
def index(request):
    return activeAuctionLists(request)


# Login
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {"message": "Invalid username and/or password."})
    else:
        return render(request, "auctions/login.html")


# Log-out
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


# Register
def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {"message": "Passwords must match."})

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {"message": "Username already taken."})
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


# Add a new auction list, if logged
@login_required
def addAuctionList(request):

    # Creación de un nuevo form del modelo Picture.
    # Picture: Clase de la cual se hereda
    # form: Hereda el form 'modificado' de PictureForm que se muestra.
    # extra= # de veces que se muestra el form.
    PictureFormSet = modelformset_factory(Picture, form=PictureForm, extra=4)

    if request.method == "POST":
        form = AuctionListForm(
            request.POST, request.FILES
        )  # Verificación de si la petición es POST y si se envía un archivo
        imageFormSet = PictureFormSet(
            request.POST, request.FILES, queryset=Picture.objects.none()
        )  # queryset: Query de filtración de datos

        if form.is_valid() and imageFormSet.is_valid():
            newAuctionList = form.save(
                commit=False
            )  # commit=False: Guardar datos para modelos desde un form que sean del tipo null=False
            newAuctionList.owner = request.user
            newAuctionList.save()

            for form in imageFormSet.cleaned_data:
                if form:
                    picture = form["picture"]
                    optText = form["optText"]
                    newPicture = Picture(auctionList=newAuctionList, picture=picture, optText=optText)
                    newPicture.save()

            context = {
                "form": AuctionListForm(),
                "imageFormSet": PictureFormSet(queryset=Picture.objects.none()),
                "success": True,
            }
            return redirect("index")
            # return render(request, "auctions/addAuctionList.html", context)
        else:
            context = {"form": AuctionListForm(), "imageFormSet": PictureFormSet(queryset=Picture.objects.none())}
            return render(request, "auctions/addAuctionList.html", context)
    else:
        context = {"form": AuctionListForm(), "imageFormSet": PictureFormSet(queryset=Picture.objects.none())}
        return render(request, "auctions/addAuctionList.html", context)


# Show all active listings
def activeAuctionLists(request):
    filterCategory = request.GET.get("category", None)  # Toma de la categoría de filtro para las listas

    # logger.error(request.GET.get)

    if filterCategory is None:
        auctionLists = AuctionList.objects.filter(isActive=True)  # Todas las listas activas
        auctionLists.items = AuctionList.objects.filter(isActive=True).count()
    else:
        auctionLists = AuctionList.objects.filter(
            isActive=True, category=filterCategory
        )  # Todas las listas activas que sean de la categoría de filtro
        auctionLists.items = AuctionList.objects.filter(isActive=True, category=filterCategory).count()

    categories = Category.objects.all()

    for auctionList in auctionLists:
        auctionList.mainPicture = (
            auctionList.listPictures.first()
        )  # .listPictures: Related name del modelo. Extrae todas las imágenes.

        if request.user in auctionList.interested.all():
            auctionList.isWatched = True
        else:
            auctionList.isWatched = False

    context = {"auctionLists": auctionLists, "categories": categories}
    return render(request, "auctions/index.html", context)


# Show a certain list by ID
def auctionList(request, auctionListId):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))

    auctionList = AuctionList.objects.get(id=auctionListId)

    if request.user in auctionList.interested.all():
        auctionList.isWatched = True
    else:
        auctionList.isWatched = False

    auctionList.watchedBy = auctionList.interested.count()

    context = {
        "auctionList": auctionList,
        "aucListPictures": auctionList.listPictures.all(),
        "bidForm": BidForm(),
        "comments": auctionList.listComments.all(),
        "commentForm": CommentForm(),
    }

    return render(request, "auctions/auctionList.html", context)


# Show watched List
@login_required
def watchedAuctionLists(request):
    auctionLists = request.user.listInterested.all()

    for auctionList in auctionLists:
        auctionList.mainPicture = auctionList.listPictures.first()

        if request.user in auctionList.interested.all():
            auctionList.isWatched = True
        else:
            auctionList.isWatched = False

    auctionLists.items = request.user.listInterested.all().count()
    context = {"auctionLists": auctionLists}
    return render(request, "auctions/watchedAuctionLists.html", context)


@login_required
def changeWatchList(request, auctionListId, currentPage):
    auctionList = AuctionList.objects.get(id=auctionListId)

    if request.user in auctionList.interested.all():
        auctionList.interested.remove(request.user)
    else:
        auctionList.interested.add(request.user)

    if currentPage == "auctionList":
        return HttpResponseRedirect(reverse("auctionList", args=[auctionListId]))
    else:
        return HttpResponseRedirect(reverse(currentPage))


# Make a bid for a non-closed auction
@login_required
def makeBid(request, auctionListId):
    auctionList = AuctionList.objects.get(id=auctionListId)

    offer = float(request.POST["offer"])

    if isValid(auctionList, offer):
        auctionList.currentBid = offer
        bidForm = BidForm(request.POST)
        newBid = bidForm.save(commit=False)
        newBid.auctionList = auctionList
        newBid.user = request.user
        newBid.save()
        auctionList.save()

        return HttpResponseRedirect(reverse("auctionList", args=[auctionListId]))
    else:
        context = {
            "auctionListId": auctionListId,
            "auctionList": auctionList,
            "aucListPictures": auctionList.listPictures.all(),
            "bidForm": BidForm(),
            "commentForm": CommentForm(),
            "failureBid": True,
        }

        return render(request, "auctions/auctionList.html", context)


def isValid(auctionList, offer):
    if offer >= auctionList.startingBid and (auctionList.currentBid is None or offer > auctionList.currentBid):
        return True
    else:
        return False


def closeAuctionList(request, auctionListId):
    auctionList = AuctionList.objects.get(id=auctionListId)

    if request.user == auctionList.owner:

        # logger.error("ERROR:", Bid.objects.filter(auctionList=auctionList))

        if auctionList.currentBid is not None:

            auctionList.isActive = False
            auctionList.buyer = Bid.objects.filter(auctionList=auctionList).last().user
            auctionList.save()

            return HttpResponseRedirect(reverse("auctionList", args=[auctionListId]))

        else:
            context = {
                "auctionList": auctionList,
                "aucListPictures": auctionList.listPictures.all(),
                "failureClose": True,
                "bidForm": BidForm(),
                "commentForm": CommentForm(),
            }

            return render(request, "auctions/auctionList.html", context)


@login_required
def addComment(request, auctionListId):
    auctionList = AuctionList.objects.get(id=auctionListId)

    commentForm = CommentForm(request.POST)

    comment = commentForm.save(commit=False)
    comment.user = request.user
    comment.auctionList = auctionList
    comment.save()

    return HttpResponseRedirect(reverse("auctionList", args=[auctionListId]))
