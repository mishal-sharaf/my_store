from django.urls import path
from customer import views


urlpatterns =[
    path("register",views.SignUpView.as_view(),name="register"),
    path("login",views.SignInView.as_view(),name="signin"),
    path("customer/home",views.HomeView.as_view(),name="user-home"),
    path("products/detail/<int:id>",views.ProductDetailView.as_view(),name="product-detail"),
    path("products/carts/<int:id>/add",views.ProductDetailView.as_view(),name="add-cart"),
    path("cart/all",views.CartListView.as_view(),name="cart-list"),
    path("orders/add/<int:cid>/<int:oid>",views.OrderView.as_view(),name="place-order"),
    path("orders/all",views.MyOrdersView.as_view(),name="my-orders"),
    path("order/<int:id>/remove",views.CanselOrder_View,name="order-cansel"),
    path("customers/accounts/signout",views.Logout_View,name="signout")
]