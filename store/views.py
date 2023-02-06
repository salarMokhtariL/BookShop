from django.shortcuts import render, redirect
from django.http import JsonResponse
import json
import datetime
from django.views.decorators.csrf import csrf_exempt
from .models import *
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.forms import UserCreationForm
from .forms import CreatUserForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout


def register_page(request):
    form = CreatUserForm()

    if request.method == 'POST':
        form = CreatUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for' + user)
            return redirect('login')

    context = {'form': form}
    return render(request, 'store/Register.html', context)


def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('store')
        else:
            messages.info(request, 'Username or password is incorrect')
            return render(request, 'store/Login.html')

    context = {}
    return render(request, 'store/Login.html', context)


def logout_page(request):
    logout(request)
    return redirect('login')


@csrf_exempt
def store(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer,
                                                     complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_item

    else:
        items = []
        order = {'get_cart_item': 0, 'get_cart_total': 0, 'shipping': False}
        cartItems = order['get_cart_item']

    product = Product.objects.all()
    cate = Category.objects.all()
    context = {'items': items, 'product': product, 'cartItems': cartItems,
               'cate': cate}
    return render(request, 'store/Store.html', context)


@csrf_exempt
def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer,
                                                     complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_item
    else:
        items = []
        order = {'get_cart_item': 0, 'get_cart_total': 0, 'shipping': False}
        cartItems = order['get_cart_item']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/Cart.html', context)


@csrf_exempt
def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer,
                                                     complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_item

    else:
        items = []
        order = {'get_cart_item': 0, 'get_cart_total': 0, 'shipping': False}
        cartItems = order['get_cart_item']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/Checkout.html', context)


@csrf_exempt
def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action:', action)
    print('Product:', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)


from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        total = data['form']['total']
        order.transaction_id = transaction_id

        if total == order.get_cart_total:
            order.complete = True
        order.save()

        if order.shipping == True:
            ShippingAddress.objects.create(
                customer=customer,
                order=order,
                address=data['shipping']['address'],
                city=data['shipping']['city'],
                state=data['shipping']['state'],
                zipcode=data['shipping']['zipcode'],
            )
    else:
        print('User is not logged in')

    return JsonResponse('Payment submitted..', safe=False)


def team_views(request):
    team = Team.objects.all()
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer,
                                                     complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_item

    else:
        items = []
        order = {'get_cart_item': 0, 'get_cart_total': 0, 'shipping': False}
        cartItems = order['get_cart_item']

    context = {'cartItems': cartItems, 'team': team}

    return render(request, 'store/team.html', context)


def author_views(request):
    author = Author.objects.all()
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer,
                                                     complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_item

    else:
        items = []
        order = {'get_cart_item': 0, 'get_cart_total': 0, 'shipping': False}
        cartItems = order['get_cart_item']

    context = {'cartItems': cartItems, 'author': author}

    return render(request, 'store/author.html', context)


def product_detail(request, slug):
    author = Author.objects.all()
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer,
                                                     complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_item

    else:
        items = []
        order = {'get_cart_item': 0, 'get_cart_total': 0, 'shipping': False}
        cartItems = order['get_cart_item']

    products = Product.objects.all()
    product = get_object_or_404(Product, slug=slug, in_stock=True)
    categories = Category.objects.all()
    context = {'cartItems': cartItems, 'author': author, 'product': product,
               'order': order, 'categories': categories,
               'items': items, 'products': products}

    return render(request, 'store/detail.html', context)


def categories(request):
    return {
        'categories': Category.objects.all()
    }


def category_list(request, category_slug=None):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer,
                                                     complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_item

    else:
        items = []
        order = {'get_cart_item': 0, 'get_cart_total': 0, 'shipping': False}
        cartItems = order['get_cart_item']

    category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(cate=category)
    context = {'cartItems': cartItems, 'category': category,
               'order': order, 'categories': categories,
               'items': items, 'products': products}
    return render(request, 'store/Cat.html', context)


def language_list(request, language_slug=None):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer,
                                                     complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_item

    else:
        items = []
        order = {'get_cart_item': 0, 'get_cart_total': 0, 'shipping': False}
        cartItems = order['get_cart_item']

    language = get_object_or_404(Language, slug=language_slug)
    products = Product.objects.filter(language=language)
    context = {'cartItems': cartItems,
               'order': order, 'categories': categories,
               'items': items, 'language': language, 'products': products}
    return render(request, 'store/Language.html', context)


def sort_page(request):

    context = {}
    return render(request, 'store/Sort.html', context)
