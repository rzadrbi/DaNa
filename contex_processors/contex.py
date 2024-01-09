from product.models import Product, Category
from cart.models import shipping_cost


def productPic(request):
    productPic = Product.images.all
    return {'productPic': productPic}

def CatSearch(request):
    Cat = Category.objects.filter(parent__categories=False)
    return {'CatList': Cat}

def shipping_costs(request):
    shipping_costs = shipping_costs.objects.all()
    return {'shipping_costs': shipping_costs}