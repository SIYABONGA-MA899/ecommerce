from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from .models import Product, Order, Customer, OrderItem, ShippingAddress
from datetime import datetime
import json
from .utils import cookieCart, guestUser
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

# Create your views here.

def SignUp(request):

    if request.method == "POST":

        name = request.POST['name']
        surname = request.POST['surname']
        username = request.POST['username']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if pass1 != pass2:

            return redirect('signup')
        
        if Customer.objects.filter(name = username):

            return redirect('signup')
        
        if Customer.objects.filter(email = email):

            return redirect('signup')

        obj1 = User.objects.create_user(username = username, email= email, password= pass1)
        obj1.first_name = name
        obj1.last_name = surname
        obj1.save()
        obj = Customer.objects.create(user = obj1, name = name, email = email)
        obj.save()

        return redirect('login')

    return render(request, "Frontend/signup.html")

def signIn(request):

    if request.method == "POST":

        username = request.POST['username']
        password = request.POST['password']

        user1 = authenticate(username = username, password = password)
        print("user1 authenticated")
        user = Customer.objects.filter(name = username)

        if user1 is not None:

            login(request, user1)
            return redirect('home')

        else:

            print("ayingenanga")

    return render(request, "Frontend/login.html")

def Home(request):

    if request.user.is_authenticated:
        customer = request.user.customer
        order, create = Order.objects.get_or_create(customer = customer, complete = False)
        print(order.cartTotal, "cart total")
        items = order.orderitem_set.all()

        context = {"order": order, "items": items}

    else:

        context = {}
        data = cookieCart(request)

        context["items"] = data['items']
        context["order"] = data['order']

    return render(request, "Frontend/home.html", context)

def Men(request):

    objs = Product.objects.filter(kind = "trouser")

    context = {"objs": objs}

    if request.user.is_authenticated:
        customer = request.user.customer
        order, create = Order.objects.get_or_create(customer = customer, complete = False)
        print(order.cartTotal, "cart total")
        items = order.orderitem_set.all()

        context = {"order": order, "items": items}

    else:

        #context = {}
        data = cookieCart(request)

        context["items"] = data['items']
        context["order"] = data['order']

    return render(request, "Frontend/men.html", context)

def Women(request):

    objs = Product.objects.filter(kind = "dress")

    context = {"objs": objs}

    if request.user.is_authenticated:
        customer = request.user.customer
        order, create = Order.objects.get_or_create(customer = customer, complete = False)
        print(order.cartTotal, "cart total")
        items = order.orderitem_set.all()

        context = {"order": order, "items": items}

    else:

        #context = {}
        data = cookieCart(request)

        context["items"] = data['items']
        context["order"] = data['order']

    return render(request, "Frontend/women.html", context)

def Kids(request):

    objs = Product.objects.filter(kind = "kids")

    context = {"objs": objs}

    return render(request, "Frontend/kids.html", context)

def Shoes(request):

    objs = Product.objects.filter(kind = "shoes")

    context = {'objs': objs}

    return render(request, "Frontend/shoes.html", context)

def Jewellery(request):

    objs = Product.objects.filter(kind = "jewellery")

    context = {"objs": objs}

    return render(request, "Frontend/jewellery.html", context)

def Underwear(request):

    objs = Product.objects.filter(kind = "underwear")

    context = {"objs": objs}

    return render(request, "Frontend/underwear.html", context)

def Cart(request):

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer = customer, complete = False)
        items = order.orderitem_set.all()

        context = {"items": items, "order": order}

    else:

        try:

            cart = json.loads(request.COOKIES["cart"])

        except:

            cart = {}
            
        context = {"order": {"number_of_items": 0, "cartTotal": 0}}
        items = []

        for i in cart.keys():

            context["order"]["number_of_items"] += cart[i]["quantity"]
            context["order"]["cartTotal"] += Product.objects.get(id = i).price * cart[i]["quantity"]

            item = {
                "product": {
                "id": Product.objects.get(id = i).id,
                "name": Product.objects.get(id = i).name,
                "price": Product.objects.get(id = i).price,
                "imageURL": Product.objects.get(id = i).imageURL
                },
                "quantity": cart[i]["quantity"],
                "itemTotal": Product.objects.get(id = i).price * cart[i]["quantity"]
            }

            items.append(item)

        context["items"] = items

        print(context["items"])
                                                 
    return render(request, "Frontend/cart.html", context)


def Checkout(request):

    if request.user.is_authenticated:
        customer = request.user.customer
        order, create = Order.objects.get_or_create(customer = customer, complete = False)
        print(order.cartTotal, "cart total")
        items = order.orderitem_set.all()

        context = {"order": order, "items": items}

    else:

        context = {}
        data = cookieCart(request)

        context["items"] = data['items']
        context["order"] = data['order']

    return render(request, "Frontend/checkout.html", context)

def updateCart(request):

    customer = request.user.customer
    data = json.loads(request.body)
    action = data['action']
    productId = data['productId']

    #customer, create = Customer.objects.get_or_create(user=request.user)
    product = Product.objects.get(id = productId)
    order, created = Order.objects.get_or_create(customer = customer, complete = False)
    
    orderitem, created = OrderItem.objects.get_or_create(order = order, product = product)

    if action == "add":

        orderitem.quantity = orderitem.quantity + 1
        print("siya ADD ngoku")

    elif action == "subtract":

        orderitem.quantity -=1
        print("siya SUBTRACT ngoku")

    orderitem.save()

    if orderitem.quantity <= 0:

        orderitem.delete()

    print(orderitem.order, orderitem.product, orderitem.quantity)

    return JsonResponse('data from the frontend ifikile', safe = False)

def processOrder(request):

    data = json.loads(request.body)
    transaction_id = datetime.now().timestamp()

    if request.user.is_authenticated:

        customer = request.user.customer
        order, create = Order.objects.get_or_create(customer = customer, complete = False)

    else:

        customer, order = guestUser(request, data)

    order.transaction_id = transaction_id
    total = float(data['userData']['total'])
            
    if total == order.cartTotal:

        order.complete = True
        order.save()

    if order.complete == True:

        address = data['shippingData']['address']
        country = data['shippingData']['country']
        city = data['shippingData']['city']
        zipcode = data['shippingData']['zipcode']

        ShippingAddress.objects.create(order = order, customer = customer, address = address, country = country, city = city, zipcode = zipcode)

    print("shipping done")

    return JsonResponse('processing is done..', safe = False)
