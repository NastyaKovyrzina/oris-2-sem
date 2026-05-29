from django.shortcuts import render, get_object_or_404, redirect
from reviews.models import Review
from reviews.forms import ReviewForm
from .models import Product, Category
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

def product_list(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    context = {
        'products': products,
        'categories': categories,
    }
    return render(request, 'catalog/product_list.html', context)

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    reviews = Review.objects.filter(product=product)
    form = ReviewForm()  

    context = {
        'product': product,
        'reviews': reviews,
        'form': form,
    }
    return render(request, 'catalog/product_detail.html', context)

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = request.session.get('cart', {})
    pid = str(product.id)
    cart[pid] = cart.get(pid, 0) + 1
    request.session['cart'] = cart
    request.session.modified = True
    return redirect('catalog:product_detail', product_id=product.id)

def cart_view(request):
    cart = request.session.get('cart', {})
    product_ids = cart.keys()
    products = Product.objects.filter(id__in=product_ids)

    items = []
    total_price = 0
    for product in products:
        qty = cart[str(product.id)]
        line_total = product.price * qty
        total_price += line_total
        items.append({
            'product': product,
            'qty': qty,
            'line_total': line_total,
        })

    return render(request, 'catalog/cart.html', {
        'items': items,
        'total_price': total_price,
    })

def clear_cart(request):
    if 'cart' in request.session:
        del request.session['cart']
        request.session.modified = True
    return redirect('catalog:cart_view')

def toggle_theme(request):
    print(f"Current theme in cookie: {request.COOKIES.get('theme')}")
    current = request.COOKIES.get('theme', 'light')
    new = 'dark' if current == 'light' else 'light'
    resp = HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    resp.set_cookie('theme', new, max_age=60*60*24*30, samesite='Lax')
    print(f"New theme set: {new}")
    return resp

@login_required
def chat_room(request):
    return render(request, 'catalog/chat.html')
