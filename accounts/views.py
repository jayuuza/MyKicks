from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout


from .forms import UserRegistrationForm
from shop.models import Order


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(data=request.POST)

        if user_form.is_valid():
            # Create a new user object
            User.objects.create_user(
                user_form.cleaned_data['email'],
                user_form.cleaned_data['email'],
                user_form.cleaned_data['password1'],
                first_name=user_form.cleaned_data['first_name'],
                last_name=user_form.cleaned_data['last_name'],
            )

            # Add a success message in the middleware
            messages.success(request, "Registration successful.")

            return redirect('shop:index')
    else:
        user_form = UserRegistrationForm()

    return render(request, 'accounts/register.html', dict(user_form=user_form))


def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # If remember me hasn't been checked then expire the session
        if not request.POST.get('remember_me'):
            request.session.set_expiry(0)

        user = authenticate(username=email, password=password)

        if user:
            login(request, user)
            messages.success(request, "Welcome, {0}!".format(user.first_name))
        else:
            messages.error(request, "Invalid login credentials.")
        return redirect('shop:index')
    else:
        return redirect('shop:index')


@login_required
def user_logout(request):
    logout(request)
    messages.warning(request, "You've been logged out.")
    return redirect('shop:index')


@login_required
def user_history(request):
    orders = Order.objects.filter(customer=request.user.pk)

    # Let's paginate
    paginator = Paginator(orders, 10)
    page = request.GET.get('page')

    try:
        orders = paginator.page(page)
    except PageNotAnInteger:
        orders = paginator.page(1)
    except EmptyPage:
        orders = paginator.page(paginator.num_pages)

    context_dict = {
        'page_title': "Order History",
        'orders': orders,
        'navbar': "my_account"
    }

    return render(request, 'accounts/history.html', context_dict)