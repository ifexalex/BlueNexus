from django.http import response
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from cart.models import Cart, CartItem
from .forms import OrderForm
import datetime
from .models import Order, Payment, OrderProduct
import json
from store.models import Product
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from decouple import config
from paystackapi.paystack import Paystack
import decimal
# Create your views here.


paystack_secretkey = config('PAYSTACK_SECRET_KEY')
paystack = Paystack(secret_key=paystack_secretkey)


def place_order(request, total=0, quantity=0,):
    current_user = request.user

    # If the cart count is less than or equal to 0, then redirect back to shop
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('store')

    grand_total = 0
    vat = 0
    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity
    vat = (2 * total)/100
    grand_total = total + vat

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            # Store all the billing information inside Order table
            data = Order()
            data.user = current_user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone = form.cleaned_data['phone']
            data.email = form.cleaned_data['email']
            data.address_line_1 = form.cleaned_data['address_line_1']
            data.address_line_2 = form.cleaned_data['address_line_2']
            data.country = form.cleaned_data['country']
            data.state = form.cleaned_data['state']
            data.city = form.cleaned_data['city']
            data.order_note = form.cleaned_data['order_note']
            data.order_total = grand_total
            data.vat = vat
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            # Generate order number
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr,mt,dt)
            current_date = d.strftime("%Y%m%d") #20210305
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()

            order = Order.objects.get(user=current_user, is_ordered=False, order_number=order_number)
            context = {
                'order': order,
                'cart_items': cart_items,
                'total': total,
                'tax': vat,
                'grand_total': grand_total,
            }
            return render(request, 'orders/payment.html' , context)
    else:
        return redirect('checkout')
    
    

def payment(request,total=0, quantity=0, cart_id=None):
    current_user = request.user
    order = Order.objects.filter(user=current_user).first()
    order_count = Order.objects.filter(user=current_user).count()
    
   
    cart_items = CartItem.objects.filter(user=current_user)
    grand_total = 0
    vat = 0
    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity
        cart_id = cart_item.cart   
    vat = (2 * total)/100
    grand_total = total + vat
    
    
        
    if current_user.is_eligible is True and order_count >1: 
        current_user.credit_balance  = current_user.credit_balance - order.order_total
        current_user.save()
        
        cart = CartItem.objects.filter(user=current_user)
        cart.delete()
        
        paymentObj = Payment.objects.create(
        user=current_user,
        payment_id = cart_id,
        payment_method = 'Paystack',
        amount_paid = str(grand_total),
        status = 'Pending',
        )
        
        
        order = Order.objects.update(
        payment=paymentObj.id,
        status = 'Accepted',
        )
    
        cart = Cart.objects.filter(cart_id=paymentObj.payment_id)
        cart.delete()
    
        payment = Payment.objects.filter(user= current_user)
        payment.update(status='Paid')
        context = {
        'order': order,
        }
        return redirect('order_complete')
    else:
        #initialize paystack Gateway
        initialize_transaction = paystack.transaction.initialize(
        email= current_user.email,
        amount=int(grand_total)*100,
        currency='NGN',
        )
    

        paymentObj = Payment.objects.create(
            user=current_user,
            payment_id = cart_item.cart.cart_id,
            payment_method = 'Paystack',
            amount_paid = str(grand_total),
            status = 'Pending',
        )
    
    
        order = Order.objects.update(
            payment=paymentObj.id,
            status = 'Accepted',
        )
    
        cart = Cart.objects.filter(cart_id=paymentObj.payment_id)
        cart.delete()
    
    return HttpResponseRedirect(initialize_transaction['data']['authorization_url'])



def order_complete(request):
    
    current_user = request.user
    order = Order.objects.filter(user=current_user).first()
    order_count = Order.objects.filter(user=current_user).count()
    cart = CartItem.objects.filter(user=current_user)
    cart.delete()
    
    payment = Payment.objects.filter(user= current_user)
    payment.update(status='Paid')
    
    
    if current_user.is_eligible is False:
    
        current_user.is_eligible =True
        current_user.save()

    
    context = {
        'order': order,
    }
    
    return render(request, 'orders/order_complete.html', context)
    
    