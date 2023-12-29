from product.models import Product, Category


def productPic(request):
    productPic = Product.images.all
    return {'productPic': productPic}

def CatSearch(request):
    Cat = Category.objects.filter(parent__categories=False)
    return {'CatList': Cat}
