import json
from .models import *

def cookieCart(request):

    try:

        cart = json.loads(request.COOKIES['cart'])

    except:

            cart = {}

    order = {"cartTotal":0, "number_of_items":0}
    items = []

    try:

        for i in cart:

            product = Product.objects.get(id  = i)

            total = product.price * cart[i]["quantity"]
            order["cartTotal"] += total 
            order["number_of_items"] += cart[i]["quantity"] 

            item = {
                    "product": {"name": product.name, "imageURL": product.imageURL, "price": product.price, "sex": product.sex, "kind": product.kind},
                    "quantity": cart[i]["quantity"],
                    "itemTotal": product.price * cart[i]["quantity"]
                }

            total += product.price * cart[i]["quantity"]

            items.append(item)

    except:

        pass

    return({'items': items, 'order': order})



def guestUser(request, data):
     
    cookieData = cookieCart(request)
    items = cookieData['items']

    email = data['userData']['email']
    name = data['userData']['name']

    customer, created = Customer.objects.get_or_create(email = email)

    customer.name = name
    customer.save()

    order = Order.objects.create(customer = customer, complete = False)

    for item in items:
        
        product = Product.objects.create(
            name = item['product']['name'],
            image = item['product']['imageURL'], 
            price = item['product']['price'],
            sex = item['product']['sex'],
            kind  = item['product']['kind']
        )

        orderitem = OrderItem.objects.create(order = order, product = product, quantity = item['quantity'])

    return (customer, order)

