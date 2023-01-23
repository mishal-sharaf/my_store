from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator,MaxValueValidator


class Products(models.Model):
    name=models.CharField(max_length=200)
    price=models.PositiveIntegerField
    description=models.CharField(max_length=200)
    category=models.CharField(max_length=200)
    image=models.ImageField(null=True,upload_to="images")
    @property
    def avg_rating(self):
        ratings=self.reviews_set.all().value_list(rating,flat=True)
        if ratings:
            return sum(ratings)/len(ratings)
        else:
            return 0
    @property
    def review_count(self, request, *args, **kwargs):
        ratings = self.reviews_get.all().values_list("rating", flat=True)
        if ratings:
            return len(ratings)
        else:
            return 0
    def __str__(self):
        return self.name

class Cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Products,on_delete=models.CASCADE)
    date=models.DateTimeField(auto_now_add=True)
    options=(
        ("order-placed","order-placed"),
        ("in-cart","in-cart"),
        ("canselled","canselled")
    )
    status=models.CharField(max_length=200,choices=options,default="in-cart")

class Reviews(models.Model):
    product=models.ForeignKey(Products,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    rating=models.PositiveIntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)])
    comment=models.CharField(max_length=200)

    def __str__(self):
        return self.comment

class Orders(models.Model):
    product=models.ForeignKey(Products,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    options=(
        ("order-placed","order-placed"),
        ("despatched","despatched"),
        ("in-transmit","in-transmit"),
        ("canselled","canselled")
    )
    status=models.CharField(max_length=200,choices=options,default="order-placed")
    date=models.DateField(auto_now_add=True)
    address=models.CharField(max_length=200)
    phone=models.CharField(max_length=12)

# orm queries
# price lessthan 2500
# qs=Products.object.filter(price__lt=2500)

# to print specific rows
# qs=Products.objects.values_list('category'))

# to prind data avoiding duplicate
# qs=Products.objects.value_list('category').distinct()prmor




