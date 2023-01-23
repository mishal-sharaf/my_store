from django.shortcuts import render,redirect
from django.views.generic import CreateView,FormView,TemplateView,ListView,DetailView
from customer.forms import RegistrationForm,SigninForm
from django.urls import reverse_lazy
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from api.models import Products,Cart,Orders
from django.db.models import Sum
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator




def Signin_required(fn):
    def wrapper(request,*args,**kwargs):
        if not request.user.is_authenticated:
            messages.error(request,"invalid session")
            return redirect("signin")
        else:
            return fn(request,*args,**kwargs)
    return wrapper

decs=[Signin_required,never_cache]



class SignUpView(CreateView):
    template_name="signup.html"
    form=RegistrationForm
    success_url=reverse_lazy("signin")
    
    def form_valid(self, form):
        messages.success(self.request,"Registration successfull..!")
        return super().form_valid(form)
    def form_invalid(self, form):
        messages.error(self.request,"Registration failed..!!")
        return super().form_invalid(form)

class SignInView(FormView):
    template_name="cust-login.hyml"
    form_class=SigninForm
    def post(self,request,*args,**kwargs):
        form=SigninForm(request.POST)
        if form.is_valid():
            uname=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
            usr=authenticate(request,username=uname,password=pwd)
            if usr:
                login(request,usr)
                return redirect("user-home")
            else:
                messages.error(request,"invalid credentials")
                return render(request,"cust-login.html",{"form":form})

@method_decorator(decs,name="dispatch")
class HomeView(ListView):
    template_name="cust-index.html"
    context_object_name="products"
    model=Products

@method_decorator(decs,name="dispatch")
class ProductDetailView(DetailView):
    template_name="cust-productdetail.html"
    context_object_name="product"
    pk_url_kwarg="id"
    model=Products

decs
def addtocart(request,*args,**kwargs):
    id=kwargs.get("id")
    product=Products.objects.get(id=id)
    user=request.user
    Cart.objects.create(user=user,product=product)
    messages.success(request,"item hasbeen added to cart")
    return redirect("user-home")


@method_decorator(decs,name="dispatch")
class CartListView(ListView):
    template_name="cart-list.html"
    model=Cart
    context_object_name="cart"

    def get(self,request,*args,**kwargs):
        qs=Cart.objects.filter(user=request.user,status="in-cart")
        total=Cart.objects.filter(user=request.user,status="in-cart").aaggregate(tot=Sum("products__price"))
        return render(request,"cart-list.html",{"carts":qs,"total":total})

    def delete(self,request,*args,**kwargs):
        qs=Cart.objects.get(id=id).delete()

@method_decorator(decs,name="dispatch")
class OrderView(TemplateView):
    template_name="chekout.html"
    def get(self,request,*args,**kwargs):
        pid=kwargs.get("pid")
        qs=Products.objects.get(id=pid)
        return render(request,"checkout.html",{"product":qs,"cid":kwargs.get("cid"),"pid":pid})
    def post(self,request,*args,**kwargs):
        cid=kwargs.get("cid")
        pid=kwargs.get("pid")
        cart=Cart.objects.get(id=id)
        product=Products.objects.get(id=pid)
        user=request.user
        mobile=request.POST.get("mobile")
        address=request.POst.get("address")
        Orders.objects.create(product=product,user=user,address=address,phone=mobile)
        Cart.status="order-placed"
        cart.save()
        messages.success(request,"your order has been placed")
        return redirect("user-home")

@method_decorator(decs,name="dispatch")
class MyOrdersView(ListView):
    model=Orders
    template_name="order-list.html"
    context_object_name="orders"

    def get_queryset(self):
        return Orders.objects.filter(user=self.request.user)

decs
def CanselOrder_View(request,*args,**kwargs):
    id=kwargs.get("id")
    Orders.objects.filter(id=id).update(status="canselled")
    return redirect("user-home")

decs
def Logout_View(request,*args,**kwargs):
    logout(request)
    messages.success(request,"Logged Out")
    return redirect("signin")