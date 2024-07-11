var cart_data = document.getElementsByClassName('update-cart');

for(i = 0; i < cart_data.length; i++){

    cart_data[i].addEventListener('click', function(){

        var productId = this.dataset.product
        var action = this.dataset.action

        if(user == 'AnonymousUser'){

            updateCookie(productId, action)
            
        }
        else{
            updateCart(productId, action) 
        }
    })
}

function updateCart(productId, action){

    var url = "/update/"

    fetch(url, {

        method: 'POST',
        headers: {'Content-Type': 'application/json', 'X-CSRFToken': csrftoken},
        body: JSON.stringify({'productId': productId, 'action': action})
    })

    .then((response) => {

        return response.json()
    })

    .then((data) => {

        console.log(data);
        location.reload()
    })
}

function updateCookie(productId, action){

    if( action == "add"){

        if(cart[productId] == undefined){

            cart[productId] = {"quantity": 1}
        }

        else{

            cart[productId]["quantity"] += 1
        }
    }

    else{

        cart[productId]["quantity"] -= 1
    }
    console.log("cart", cart, "--")
    document.cookie = "cart=" + JSON.stringify(cart) + ";domaim=;path=/"
    location.reload()

}