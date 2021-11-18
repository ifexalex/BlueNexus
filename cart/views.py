from django.shortcuts import get_object_or_404, redirect, render
from cart.models import CartItem, Cart
from django.utils.formats import number_format
from django.contrib.auth.decorators import login_required
from store.models import Product

# Create your views here.


def _cart_session(request):
    cart = request.session.session_key
    
    if not cart:
        cart = request.session.create()
    return cart



def add_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    
    try:
        cart = Cart.objects.get(cart_id=_cart_session(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id=_cart_session(request)
        )
    cart.save()
    
        
    try:
        
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(product= product, user = request.user)
        else: 
            cart_item = CartItem.objects.get(product= product, cart = cart)
        cart_item.quantity+=1
        cart_item.save()
    except CartItem.DoesNotExist:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.create(
            product=product,
            quantity=1,
            user=request.user,
            cart = cart
        )
        else:
            cart_item = CartItem.objects.create(
                product=product,
                quantity=1,
                cart = cart
            )
        
        cart_item.save()
        
    return redirect('cart')


def CartPage(request, total = 0, quantity = 0, cart_items = None):
    
    vat = 0
    grand_total = 0
    try:
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user= request.user, is_active = True)
        cart = Cart.objects.get(cart_id=_cart_session(request))
        cart_items = CartItem.objects.filter(cart = cart, is_active = True)
        
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity+= cart_item.quantity
            
        vat = (2* total)/100
        grand_total = (vat + total)
    except:
        pass
    
    context = {
        'total': number_format(total, force_grouping = True),
        'quantity': quantity,
        'cart_items': cart_items,
        'vat': vat,
        'grand_total': number_format(grand_total, force_grouping = True),
    }
    return render(request, 'store/cart.html', context)


def remove_cart_item(request, product_id, cart_item_id):
    
    
    try: 
        product = get_object_or_404(Product, id=product_id)
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(product = product, user= request.user, id=cart_item_id)
            
        else:
            cart = Cart.objects.get(cart_id=_cart_session(request))
            cart_item = CartItem.objects.get(product = product, cart= cart)
    
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
    
        else:  
            cart_item.delete()
    except:
        pass
        
    return redirect('cart')



def remove_cart(request, product_id,cart_item_id):
    
    product = get_object_or_404(Product, id=product_id)
    if request.user.is_authenticated:
            cart_item = CartItem.objects.get(product = product, user= request.user, id=cart_item_id)
    else:
        cart = Cart.objects.get(cart_id=_cart_session(request))
        cart_item = CartItem.objects.get(product = product, cart= cart, id=cart_item_id)
    
    cart_item.delete()
    return redirect('cart')

@login_required(login_url='login')
def checkout_cart(request,total = 0, quantity = 0, cart_items = None):
    vat = 0
    grand_total = 0
    
    try:
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user= request.user, is_active = True)
        cart = Cart.objects.get(cart_id=_cart_session(request))
        cart_items = CartItem.objects.filter(cart = cart, is_active = True)
        
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity+= cart_item.quantity
            
        vat = (2* total)/100
        grand_total = (vat + total)
    except:
        pass
    
    context = {
        'total': number_format(total, force_grouping = True),
        'quantity': quantity,
        'cart_items': cart_items,
        'vat': vat,
        'grand_total': number_format(grand_total, force_grouping = True),
    }
    
    return render(request, 'store/checkout.html', context)
    