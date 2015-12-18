from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from . models import Product, Order
from . forms import BuyShirtForm


def index(request):
    products = Product.objects.all()

    # Let's paginate
    paginator = Paginator(products, 10)
    page = request.GET.get('page')

    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    context_dict = {
        'page_title': "Products",
        'page_sub_title': "",
        'products': products,
        'navbar': "products"
    }

    return render(request, 'shop/products/index.html', context_dict)


def detail(request, product_id):
    if request.method == 'POST':
        # Check if user is logged in before processing POST
        if not request.user.is_authenticated():
            messages.error(request, "Only logged in users may purchase products.")
            return redirect('shop:detail', product_id)

        # Bind the submitted form
        form = BuyShirtForm(request.POST)

        if form.is_valid():
            # Fetch the Product
            product = get_object_or_404(Product, pk=product_id)

            # Create a purchase order for the product
            new_order = Order(
                customer=request.user,
                product=product,
                size=form.cleaned_data.get('size'),
                price=product.current_price
            )

            # Save it
            new_order.save()

            messages.success(
                request,
                "Thanks for shopping with us {0}! Your product has been purchased.".format(request.user.first_name)
            )
            return redirect('shop:index')
    else:
        form = BuyShirtForm()

    context_dict = {
        'page_title': "Viewing Product" + product_id,
        'product': Product.objects.get(pk=product_id),
        'navbar': "products",
        'form': form
    }

    return render(request, 'shop/products/detail.html', context_dict)