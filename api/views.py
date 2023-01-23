from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from api.models import Products,Cart,Reviews
from api.serializers import ProductSeriealizers,ProductModelSeriealizers,UserSerializers,CartsSerializer,ReviewSerializer
from rest_framework import viewsets
from rest_framework.decorators import action
from django.contrib.auth.models import User
from rest_framework import authentication,permissions

class ProductView(APIView):
    def get(self,request,*args,**kwargs):
        qs=Products.objects.all()
        serializer=ProductSeriealizers(qs,many=True)
        return Response(data=serializer.data)

    def post(self,request,*args,**kwargs):
        serializer=ProductSeriealizers(data=request.data)
        if serializer.is_valid():
            Products.objects.create(**serializer.validated_data)
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)

class ProductDetailsView(APIView):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("id")
        qs=Products.objects.get(id=id)
        serializer=ProductSeriealizers(qs,many=False)
        return Response(data=serializer.data)

    def put(self,request,*args,**kwargs):
        id=kwargs.get("id")
        Products.objects.filter(id=id).update(**request.data)
        qs=Products.objects.get(id=id)
        serializer=ProductSeriealizers(qs,many=False)
        return Response(data=serializer.data)
    def delete(self,request,*args,**kwargs):
        id=kwargs.get("id")
        Products.objects.filter(id=id).delete()
        return Response(data="product deleted")

# viewset

class ProductViewsetView(viewsets.ModelViewSet):
    # def list(self,request,*args,**kwargs):
    #     qs=Products.objects.all()
    #     serializer=ProductModelSeriealizers(qs,many=True)
    #     return Response(serializer.data)
    # def create(self,request,*args,**kwargs):
    #     serializer=ProductModelSeriealizers(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.validated_data)
    #     else:
    #         return Response(serializer.errors)
    # def retrieve(self,request,*args,**kwargs):
    #     id=kwargs.get("pk")
    #     qs=Products.objects.get(id=id)
    #     seriealizer=ProductModelSeriealizers(qs,many=False)
    #     return Response(data=seriealizer.data)
    # def update(self,request,*args,**kwargs):
    #     id=kwargs.get("pk")
    #     obj=Products.objects.get(id=id)
    #     serializer=ProductModelSeriealizers(data=request.data,instance=obj)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(data=serializer.data)
    #     else:
    #         return Response(serializer.errors)
    # def destroy(self,request,*args,**kwargs):
    #     id=kwargs.get("pk")
    #     Products.objects.get(id=id).delete()
    #     return Response('deleted')
    serializer_class = ProductModelSeriealizers
    queryset = Products.objects.all()
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    @action(methods=["GET"],detail=False)
    def categories(self,request,*args,**kwargs):
        res=Products.objects.value_list("category",flat=True).distinct()
        return Response(data=res)

    @action(methods=["POST"],detail=True)
    def addcart(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        item=Products.objects.get(id=id)
        usr=request.user
        usr.cart_set.create(product=item)
        return  Response(data="added")
    @action(methods=["POST"],detail=True)
    def addreview(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        item=Products.objects.get(id=id)
        usr=request.user
        serializer=ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(product=item,user=usr)
            return Response(data=serializer.data)
        else:
            return  Response(serializer.errors)
        # usr.reviews_set.create(product=item)
        # return  Response(data="review added")
    @action(["GET"],detail=True)
    def view_review(self,request,*args,**kwargs):
        # id=kwargs.get(id="pk")
        product=self.get_object()
        qs=product.viewreview_set.all()
        serializer=ReviewSerializer(qs,many=True)
        return Response(data=serializer.data)

class CartView(viewsets.ModelViewSet):
    serializer_class = CartsSerializer
    queryset = Cart.objects.all()
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def list(self,request,*args,**kwargs):
        qs=request.user.cart_set.all()
        serializer=CartsSerializer(qs,many=True)
        return Response(data=serializer.data)

class DeleteReviewView(viewsets.ViewSet):
    def delete(self,request,*args,**kwargs):
        id=kwargs.get(id="pk")
        obj=Products.objects.filter(id=id).delete()
        return Response(data='deleted')
class Userview(viewsets.ModelViewSet):
    serializer_class = UserSerializers
    queryset = User.objects.all()






    # def create(self,request,*args,**kwargs):
    #     serializer=UserSerializers(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(data=serializer.data)
    #     else:
    #         return Response(data=serializer.errors)
    #