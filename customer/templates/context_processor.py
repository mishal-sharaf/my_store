from api.models import Cart

def cart_count(request):
    if request.user.is_authenticated:
        count=Cart.objects.filter(user=request.user).count()
    else:
        count=0
    return {"count":count}