
from django.urls import path
from . import views
urlpatterns = [
    path('',views.index, name='index'),
    path('userLogin/signup/',views.signup, name = 'signup'),
    path('userLogout',views.userLogout, name = 'userLogout'),
    path('userLogin/signin/',views.signin, name = 'signin'),
    path('addToCart/',views.addToCart, name='addToCart'),
    path('cart/',views.cart, name='cart'),
    path('fetchCart/',views.fetchCart, name='fetchCart'),
    path('deleteCart/<id>',views.deleteCart, name='deleteCart'),
    path('updateCart/<id>',views.updateCart, name='updateCart'),
    path('category/',views.category, name='category'),
    path('categoryDisplay/<id>',views.categoryDisplay, name='categoryDisplay'),
    path('details/<id>',views.details, name='details'),
    path('customAdmin/adminLogin/',views.adminLogin, name='adminLogin'),
    path('adminLogout',views.adminLogout, name='adminLogout'),
    path('customAdmin/admin/',views.admin, name='admin'),
    path('customAdmin/addProducts/',views.addProducts, name='addProducts'),
    path('customAdmin/editProduct/<id>',views.editProduct, name='editProduct'),
    path('deleteProduct/<id>',views.deleteProduct, name='deleteProduct'),
    path('customAdmin/addCategory/',views.addCategory, name='addCategory'),
    path('customAdmin/adminCategoryDisplay/<id>',views.adminCategoryDisplay, name='adminCategoryDisplay'),
]