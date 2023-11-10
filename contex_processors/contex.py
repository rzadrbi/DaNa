from product.models import Product


def productPic(request):
    productPic = Product.images.all
    return {'productPic': productPic}
