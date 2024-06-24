from django import views
from django.contrib import admin
from django.urls import path, include
from NepBiz.views import EsewaRequestView, EsewaVerifyView
from myapp.views import contact_view, delete_cart_item, cart_delete, cart_inc, cart_dec, home, add_to_cart, login_view, logout_view, paymentsuccess, signup, cart, go_to_cart, checkout_view, checkout, verify_payment
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path("__debug__/", include("debug_toolbar.urls")),
    path('', include('home.urls')),
    path('', include('search.urls')),
    path('', home, name='home'),
    path('product/', include('product.urls')),
    path('add_to_cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('contact/', contact_view, name='contact'),
    path('login/', login_view, name='login_view'),
    path('logout/', logout_view, name='logout'),
    path('signup/', signup, name='signup'),
    path('cart/', cart, name='cart'),
    path('cart/delete/<int:id>/', cart_delete, name='cart_delete'),
    path('cart/inc/<int:id>/', cart_inc, name='cart_inc'),
    path('cart/dec/<int:id>/', cart_dec, name='cart_dec'),



    path('go_to_cart/', go_to_cart, name='go_to_cart'),
    path('checkout_view/', checkout_view, name='checkout_view'),
    path("esewa-request/", EsewaRequestView.as_view(), name="esewarequest"),
    path("esewa-verify/", EsewaVerifyView.as_view(), name="esewaverify"),
    path('checkout/', checkout, name='checkout'),
    path('verify_payment/', verify_payment, name='verify_payment'),
    path('paymentsuccess/<int:oid>/', paymentsuccess, name='paymentsuccess'),
    path('delete_cart_item/<int:id>/', delete_cart_item, name='delete_cart_item'),




    # path('product/',product),
    # path('order/<int:food_item_id>/',order_now, name='order_now')

]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
