from django.shortcuts import get_object_or_404, render
from category.models import Category
from store.models import Product
from cart.models import CartItem
from cart.views import _cart_session

# Create your views here.


def Store(request, category_slug=None):
    
    categories = None
    products = None
    
    if category_slug is not None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=categories, is_available=True)
        product_count = products.count
    else:
        product_count = Product.objects.all().count
        categories = Category.objects.all()
        products = Product.objects.filter(is_available=True)
    
    context = {
        'product_count': product_count,
        "products": products,
        'category': categories,
    }
    return render(request, 'store/store.html', context)


def Product_detail(request, category_slug, product_slug):
    try:
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_session(request), product = single_product).exists
    except Exception as e:
        raise e
    context = {
        'single_product': single_product,
        'in_cart': in_cart
    }
    return render(request, 'store/product_detail.html', context)
    
     