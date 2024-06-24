import uuid
from .models import Cart
from django.shortcuts import redirect
from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import login_required
# Import this decorator if it's not already imported.
from django.contrib.auth.decorators import login_required
from .models import Order
from django.shortcuts import get_object_or_404, render, redirect
import json
from django.http import Http404, HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Cart, contact
from home.models import FeatureProduct, Product
from django.contrib.auth.models import User
from .forms import CheckoutForm
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            # Redirect to a success page
            messages.success(request, 'Login Successful')

            return redirect('home')

        else:
            messages.error(request, 'username & password may be invalid')
            return redirect('login_view')

    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('home')


def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        # Attempt to create a new user
        if User.objects.filter(username=username).exists():
            error_message = 'Username is already taken. Please choose a different username.'
            return render(request, 'signup.html', {'error_message': error_message})

        else:
            user = User.objects.create_user(
                username=username, email=email, password=password)
            user.save()
            messages.success(
                request, "your account has been created successfully")

            # Redirect or perform additional actions for successful signup
            return redirect('login_view')

    # Display an error message when the username is already taken
    else:
        return render(request, 'signup.html')


def home(request):
    # feature_products = FeatureProduct.objects.all().prefetch_related('product')
    feature_products = FeatureProduct.objects.all().prefetch_related('product')

    context = {
        'feature_products': feature_products
    }

    if request.user.is_authenticated:
        user_id = request.user.id
        # products =

        # qty = len(list(products))
        qty = Cart.objects.filter(
            user=user_id, isClear=False).count()
        # print('QTY: ', qty, '   ', type(qty))
        context['cart_quantity'] = qty

    return render(request, 'home.html', context)


def contact_view(request):
    if request.method == "POST":
        name = request.POST['name']
        phone = request.POST['phone']
        email = request.POST['email']
        subject = request.POST['message']

        contact.objects.create(name=name, phone=phone,
                               email=email, subject=subject)

        messages.success(request, 'Sent Message Successful')
        return redirect("home")

     #########
    context = {}

    if request.user.is_authenticated:
        user_id = request.user.id
        products = Cart.objects.filter(user=user_id, isClear=False)

        qty = len(list(products))
        context['cart_quantity'] = str(qty)
    #######

    return render(request, 'contact.html', context)


# def menu(request):
#     return render(request, 'menu.html')


def cart(request):
    user = User.objects.get(id=request.user.id)
    cart_items = Cart.objects.filter(user=user, isClear=False)

    total_price = 0
    for item in cart_items:
        total_price += item.product.discountedPrice() * item.qunatity

    #################
    qty = cart_items.count()
    # print('QTY: ', qty, '   ', type(qty))
    context = {
        "cart_items": cart_items,
        'cart_quantity': qty,
        'total_price': total_price
    }

    if request.user.is_authenticated:
        user_id = request.user.id
        products = Cart.objects.filter(user=user_id, isClear=False)

        qty = len(list(products))
        context['cart_quantity'] = str(qty)
    ####################
    return render(request, 'cart.html', context)


def cart_delete(request, id):
    cart_item = Cart.objects.get(id=id)
    cart_item.clear_cart()
    return redirect('cart')


def cart_inc(request, id):
    cart_item = Cart.objects.get(id=id)
    cart_item.increment()
    return redirect('cart')


def cart_dec(request, id):
    cart_item = Cart.objects.get(id=id)
    cart_item.decrement()
    return redirect('cart')


all_cart_items = []


def go_to_cart(request):
    global all_cart_items
    if request.method == 'POST':
        # Get the JSON data from the request body
        data = json.loads(request.body)
        print(data)

        # Process the JSON data
        cart_items = Product.objects.filter(id__in=data['products'])
        all_cart_items = cart_items

        print(cart_items)
        # Return the JSON response
        return render(request, 'cart.html',)
    else:
        cart_items = all_cart_items
        all_cart_items = []
    # return render(request, 'cart.html', {'cart_items':[{'name':'One'},{'name':'Two'}]} )
    return render(request, 'cart.html', {'cart_items': cart_items})
    # store order information(checkout form)


def checkout_view(request):
    # fetching total amount
    user = User.objects.get(id=request.user.id)
    cart_items = Cart.objects.filter(user=user, isClear=False)
    products = [item.product.price for item in cart_items]
    total_amount = sum(products)
    url = "https://uat.esewa.com.np/epay/transrec"
    data = {
        'amt': total_amount,
        'scd': 'EPAYTEST',
        # user.id is initial use oredr id for specific order
        'rid': "refid"+str(user.id),
        'pid': uuid.uuid4()
    }

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            print('validdddddddddd')
            return render(request, 'esewarequest.html', {'total_amount': total_amount})
    form = CheckoutForm()
    context = {'form': form, 'dynamic_total_amount': total_amount}

    if request.user.is_authenticated:
        user_id = request.user.id
        products = Cart.objects.filter(user=user_id, isClear=False)
        qty = len(list(products))
        context['cart_quantity'] = str(qty)
    return render(request, 'checkout.html', context)

# Checkout ................................


@login_required
def checkout(request):
    if request.method == 'POST':
        print('Post req')
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            option = form.cleaned_data

            # Set the user for the order
            order.ordered_by = request.user

            cart_items = Cart.objects.filter(user=request.user, isClear=False)
            products = [item.product.price for item in cart_items]
            total_amount = sum(products)
            order.save()
            oid = order.pk
            print('Order Saved')
            print(total_amount)
            uid = uuid.uuid4()
            print(uid)

            return render(request, 'esewarequest.html', {'uid': uid, 'total': total_amount, 'oid': oid, 'order': order})
        else:
            print('Form is Invalid')

    form = CheckoutForm()
    return render(request, 'checkout.html', {'form': form})


# Views for cart


@login_required(login_url='/login')
def add_to_cart(request, product_id):
    if request.user.is_authenticated:
        user_id = request.user.id
        # Add item to cart
        if product_id > 0:
            user = User.objects.get(id=user_id)
            product = Product.objects.get(id=product_id)
            try:
                cart_item = Cart.objects.get(
                    user=user, isClear=False, product=product)
                print('Added product id', cart_item)
                print(cart_item)
            except Cart.DoesNotExist:
                cart_item = Cart.objects.create(
                    user=user, product=product, qunatity=1)
                print('Product added, : ', cart_item)
            return redirect('home')


# @csrf_exempt
def verify_payment(self, request):
    url = "https://uat.esewa.com.np/epay/transrec"
    q = request.GET.get('q')
    print(request.GET)
    d = {
        'q': request.GET.get('q'),
        'amt': request.GET.get('amt'),
        'scd': 'EPAYTEST',
        'rid':  request.GET.get('refId'),
        'pid': request.GET.get('oid'),
    }
    resp = request.post(url, d)
    print("status code=====", resp.status_code)
    if resp.status_code == 200:
        # print(resp.text)
        return HttpResponse("Payment Successful")
    else:
        raise Http404()


# views.py


def paymentsuccess(request, oid):
    if request.user.is_authenticated:
        try:
            order = Order.objects.get(id=oid)
            cart_items = Cart.objects.filter(user=request.user, isClear=False)

            # cart_items.bulk_update(fields=[isClear])
            total_cost = 0
            for cart in cart_items:
                total_cost += cart.total_price()

        except Order.DoesNotExist:
            return HttpResponse('Order not found')

        context = {
            'order': order,
            'cart_items': cart_items,
            'total_cost': total_cost
        }
        Cart.objects.filter(user=request.user).update(isClear=True)
        return render(request, 'paymentsuccess.html', context)
    else:
        return HttpResponse('User not authenticated')


# views.py
# cart/views.py


def delete_cart_item(request, id):
    items = Cart.objects.get(id=id)
    print(items)
    items.delete()
    # Replace 'cart' with the appropriate URL name
    return render(request, 'cart.html', {'items': items})
