from django.shortcuts import render, get_object_or_404
from .models import Category, Product, ProductImage
from cart.forms import CartAddProductForm

# Create your views here.
def index(request):
    categories = Category.objects.all()
    return render(request, 'shop/index.html', {'categories': categories})


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.all()
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    cart_product_form = CartAddProductForm()

    return render(request, 'shop/product_list.html',
                    {'category': category,
                    'categories': categories,
                    'products': products,
                    'cart_product_form': cart_product_form})


def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    pictures = ProductImage.objects.filter(product=product.id)

    cart_product_form = CartAddProductForm()

    return render(request,'shop/product_detail.html',
                    {'product': product,
                    'pictures':pictures,
                    'cart_product_form': cart_product_form})
