from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import get_object_or_404, render
from .models import Product, Category, Brand

# Create your views here.

def get_sidebar_context(selected_category=None, selected_brand=None):
    return {
        'categories': Category.objects.all()[:4],
        'brands': Brand.objects.all()[:11],
        'selected_category': selected_category,
        'selected_brand': selected_brand,
    }


def home(request):
    latestproducts = Product.objects.all().order_by('-created_at')[:6]
    featuredproducts = Product.objects.filter(featured=True)[:6]
    context = {
        'latestproducts': latestproducts,
        'featuredproducts': featuredproducts,
    }
    context.update(get_sidebar_context())
    return render(request, 'products/home.html', context)


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    context = {
        'product': product,
    }
    context.update(get_sidebar_context())
    return render(request, 'products/detail.html', context)


def product_list(request, list_type):
    if list_type == 'latest':
        products = Product.objects.all().order_by('-created_at')
        title = 'Latest Products'
    elif list_type == 'featured':
        products = Product.objects.filter(featured=True).order_by('-created_at')
        title = 'Featured Products'
    else:
        raise Http404('Product list not found')

    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'products': page_obj.object_list,
        'page_obj': page_obj,
        'paginator': paginator,
        'title': title,
    }
    context.update(get_sidebar_context())
    return render(request, 'products/product_list.html', context)


def filter_products(request, filter_type, slug):
    if filter_type == 'category':
        selected_category = get_object_or_404(Category, slug=slug)
        products = Product.objects.filter(category=selected_category).order_by('-created_at')
        title = f'{selected_category.name} Products'
        selected_brand = None
    elif filter_type == 'brand':
        selected_brand = get_object_or_404(Brand, slug=slug)
        products = Product.objects.filter(brand=selected_brand).order_by('-created_at')
        title = f'{selected_brand.name} Products'
        selected_category = None
    else:
        raise Http404('Filter not found')

    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'products': page_obj.object_list,
        'page_obj': page_obj,
        'paginator': paginator,
        'title': title,
        'selected_category': selected_category,
        'selected_brand': selected_brand,
    }
    context.update(get_sidebar_context(selected_category, selected_brand))
    return render(request, 'products/product_list.html', context)
