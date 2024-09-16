from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User,house,listing,Comment,Bid


def index(request):
    if request.method=="GET":
        home=house.objects.all()
        activelisting=listing.objects.filter(isactive=True)
        name=request.user
        return render(request, "auctions/index.html",{
          "home":home,
         "category":activelisting,
        })

def catji(request):
    if request.method=="POST":
        home=house.objects.all()
        housefromform=request.POST['houe']
        ho=house.objects.get(type=housefromform)
        activelisting=listing.objects.filter(isactive=True, house=ho)
        name=request.user
        return render(request, "auctions/index.html",{
          "home":home,
         "category":activelisting,
        })

def watch(request, id):
    object=listing.objects.get(pk=id)
    objectwatch=request.user in object.watchlist.all()
    name=request.user
    cateory=listing.objects.filter(watchlist=name)
    isowner= request.user.username==object.owner.username
    n=len(cateory)
    com=Comment.objects.filter(list=object)
    return render(request,"auctions/watch.html",{
        "object":object,
        "objectwatch":objectwatch,
        "n":n,
        "com":com,
        "isowner":isowner,
    })


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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def create(request): 
  if request.method=='GET':
    allcategory=house.objects.all()
    owner=User.objects.all()
    name=request.user
    cateory=listing.objects.filter(watchlist=name)
    n=len(cateory)
    return render(request, "auctions/create.html",{
       "category":allcategory,
       "person":owner,
       "n":n
    })
  else:
      title=request.POST["title"]
      discription=request.POST["discription"]
      imageurl=request.POST["imageurl"]
      price=request.POST["price"] 
      home=request.POST["house"]
      person=request.user
      ho=house.objects.get(type=home)
      currentUser=request.user

      bid=Bid(bid=float(price), user=currentUser)
      bid.save()
      new=listing(
          title=title,
          discription=discription,
          imageurl=imageurl,
          price=bid,
          owner=person,
          house=ho
      )
      new.save()
      return HttpResponseRedirect(reverse(index))

def addBid(request, id):
    newBid=float(request.POST["newBid"])
    object=listing.objects.get(pk=id)
    isowner= request.user.username==object.owner.username
    if newBid>object.price.bid:
        updatebid=Bid(user=request.user, bid=newBid)
        updatebid.save()
        object.price=updatebid
        object.save()
        return render(request, "auctions/watch.html",{
            "object":object,
            "message":"New Bid had been placed",
            "update":True,
            "isowner":isowner,

        })
    else:
        return render(request, "auctions/watch.html",{
            "object":object,
            "message":"Bid must be larger than previous",
            "update":False,
            "isowner":isowner,
        })

def watchlist(request):
    name=request.user
    category=listing.objects.filter(watchlist=name)
    n=len(category)
    return render(request,"auctions/watchlist.html",{
        "category":category,
       "n":n,

    })

def Cont(request):
    name=request.user
    cateory=listing.objects.filter(watchlist=name)
    n=len(cateory)
    return render(request,"auctions/layout.html",{
        "n":n,
    })
   
    
def removewatch(request, id):
    listingdata= listing.objects.get(pk=id)
    currentuser=request.user
    listingdata.watchlist.remove(currentuser)
    return HttpResponseRedirect(reverse("watch",args=(id, )))

def addwatch(request,id):
    listingdata= listing.objects.get(pk=id)
    currentuser=request.user
    listingdata.watchlist.add(currentuser)
    return HttpResponseRedirect(reverse("watch",args=(id, )))

def comment(request, id):
  if request.method=="POST":
    object=listing.objects.get(pk=id)
    currentuser=request.user
    comy=request.POST["coment"]
    coy=Comment(
        author=currentuser,
        list=object,
        comment=comy,
    )
    coy.save()
    return HttpResponseRedirect(reverse("watch",args=(id, )))

def closeAuction(request, id):
    object=listing.objects.get(pk=id)
    object.isactive=False
    object.save()
    name=request.user
    cateory=listing.objects.filter(watchlist=name)
    isowner= request.user.username==object.owner.username
    n=len(cateory)
    com=Comment.objects.filter(list=object)
    return render(request,"auctions/watch.html",{
        "object":object,
        "n":n,
        "com":com,
        "update":True,
       "isowner":isowner,
        "message":"Congratulation you auction isclosed",
    })







      
 
