from django.urls import path
from .views import SignUp, signIn, Home, Men, Women, Kids, Shoes, Jewellery, Underwear, Cart, updateCart, Checkout, processOrder

urlpatterns = [
    path("signup/", SignUp, name = "signup"),
    path("login/", signIn, name="login"),
    path("", Home, name= "home"),
    path("men/", Men, name= "men"),
    path("women/", Women, name= "women"),
    path("kids/", Kids, name= "kids"),
    path("shoes/", Shoes, name= "shoes"),
    path("jewellery/", Jewellery, name= "jewellery"),
    path("underwear/", Underwear, name= "underwear"),
    path("cart/", Cart, name = "cart"),
    path("update/", updateCart, name = "update"),
    path("checkout/", Checkout, name = "checkout"),
    path("process_order/", processOrder, name = "process_order")
]