from django.core.paginator import Paginator
from home.models import Product, Category, Brand, Activity
from django.http import JsonResponse
from django.core import serializers
from django.shortcuts import render
import json
from django.db.models import F, ExpressionWrapper, DecimalField
from myapp.models import Cart
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from product.models import ReviewModel
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required


# Create your views here.
# For Carasoul: https://swiperjs.com/get-started#use-swiper-from-cdn


def process_list(lst):
    return [int(item) for item in lst if item != '']


def product(request, id):
    print('Product Id: ', id)
    product = Product.objects.get(pk=int(id))
    description = product.description.split('\n')
    # Get related products from the same category
    related_products = Product.objects.filter(category=product.category).exclude(
        id=id
    )[:3]

    context = {
        'product': product,
        'description': description,
        'related_products': related_products,
        'reviews': ReviewModel.objects.filter(product=product)

    }
# :ReviewModel.objects.
    if request.user.is_authenticated and not ReviewModel.objects.filter(user=request.user).exists():
        context['can_review'] = True

    return render(request, 'product/product.html', context)


def product_list(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    brands = Brand.objects.all()

    # Create a Paginator object
    paginator = Paginator(products, 6)  # Show 5 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Cart
    user = request.user  # User.objects.get(id=request.user.id)
    cart_items = Cart.objects.filter(user=user.pk, isClear=False)
    qty = cart_items.count()

    context = {
        # 'products': products,
        'categories': categories,
        'brands': brands,
        'page_obj': page_obj,
        'cart_quantity': qty
    }
    return render(request, 'menu/menu.html', context)


@csrf_exempt
# @login_required
@require_POST
def filter_products(request):
    if request.method == 'POST':
        json_data = json.loads(request.body)
        min_price = json_data['min_price']
        max_price = json_data['max_price']
        category = json_data['category']
        selected_brands = json_data['brands']
        selected_genders = json_data['genders']
        page_number = json_data.get('page', 1)

        selected_brands = process_list(selected_brands)
        if len(selected_brands) == 0:
            selected_brands = None

        selected_genders = process_list(selected_genders)
        if len(selected_genders) == 0:
            selected_genders = None

        # Start with all products
        products = Product.objects.all()

        products = products.annotate(
            discounted_price=ExpressionWrapper(
                F('price') - (F('price') * F('discount') / 100.0),
                output_field=DecimalField(),
            )
        )
        print('Price Min: ', min_price)
        # Filter by price
        if min_price is not None:
            products = products.filter(discounted_price__gte=min_price)
        if max_price is not None:
            products = products.filter(discounted_price__lte=max_price)
        # products.filter(discounted_price__gte=min_price)
        # Filter by category
        if category != -1:
            products = products.filter(category=category)

        # Filter by brands
        if selected_brands:
            products = products.filter(brand__in=selected_brands)

        # Filter by genders
        if selected_genders:
            products = products.filter(gender__in=selected_genders)

        # Pagination
        # Create a Paginator object
        # Create a Paginator object
        # paginator = Paginator(products, 3)  # Show 5 products per page
        # page_obj = paginator.get_page(page_number)

        # Prepare the data for the JSON response
        # data = serializers.serialize(
        #     'json', page_obj.object_list, fields=('id', 'name', 'price', 'discount', 'image')
        # )
        data = serializers.serialize(
            'json', products, fields=('id', 'name', 'price', 'discount', 'image')
        )
        # Return the JSON response
        return JsonResponse(data, safe=False)


# def product_list(request):
#     products = Product.objects.all()

#     # Apply filters
#     category = request.GET.get('category')
#     if category:
#         products = products.filter(category=category)

#     # Pagination
#     paginator = Paginator(products, 10)  # 10 products per page
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)

#     data = {
#         'products': list(page_obj.object_list.values()),  # Convert QuerySet to list of dictionaries
#         'has_next': page_obj.has_next(),
#         'has_previous': page_obj.has_previous(),
#         'next_page_number': page_obj.next_page_number() if page_obj.has_next() else None,
#         'previous_page_number': page_obj.previous_page_number() if page_obj.has_previous() else None,
#     }
#     return JsonResponse(data)
