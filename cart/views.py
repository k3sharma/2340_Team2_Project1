from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from django.utils.timezone import now
from dashboard.models import Movie, Order, OrderItem
from .utils import calculate_cart_total

def index(request):
    cart_total = 0
    movies_in_cart = []
    cart = request.session.get('cart', {})
    movie_ids = list(cart.keys())
    if (movie_ids != []):
        movies_in_cart = Movie.objects.filter(id__in=movie_ids)
        cart_total = calculate_cart_total(cart,
            movies_in_cart)
    template_data = {}
    template_data['title'] = 'Cart'
    template_data['movies_in_cart'] = movies_in_cart
    template_data['cart_total'] = cart_total
    return render(request, 'cart/index.html',
        {'template_data': template_data})

def add(request, id):
    get_object_or_404(Movie, id=id)
    cart = request.session.get('cart', {})
    cart[id] = request.POST['quantity']
    request.session['cart'] = cart
    return redirect('cart.index')

def add_to_cart(request, id):
    get_object_or_404(Movie, id=id)
    cart = request.session.get('cart', {})
    cart[id] = request.POST['quantity']
    request.session['cart'] = cart
    return redirect('cart.index')

def clear(request):
    request.session['cart'] = {}
    return redirect('cart.index')

def remove(request, id):
    cart = request.session.get('cart', {})
    if id in cart:
        del cart[id]
    request.session['cart'] = cart
    return redirect('cart.index')

@login_required
def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        return redirect('cart.index')

    movie_ids = list(cart.keys())
    movies_in_cart = Movie.objects.filter(id__in=movie_ids)

    order = Order.objects.create(user=request.user, date=now())
    print(cart)
    for movie in movies_in_cart:
        quantity = cart[str(movie.id)]
        OrderItem.objects.create(order=order, movie=movie, quantity=quantity)

    request.session['cart'] = {}

    return redirect('cart.orders')

@login_required
def orders(request):
    user_orders = Order.objects.filter(user=request.user).order_by('-date')
    return render(request, 'cart/orders.html', {'orders': user_orders})