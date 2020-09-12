from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Customer, Product, Order
from .forms import OrderForm, CreateUserForm
from .filters import OrderFilter


def registerUser(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')

    context = {'form': form}
    return render(request, 'accounts/register.html', context)


def loginUser(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    messages.set_level(request, messages.WARNING)

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.add_message(request,
                                 messages.WARNING,
                                 'Invalid username or password.'
                                 )

    context = {}
    return render(request, 'accounts/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')


@login_required(login_url="login")
def dashboard(request):
    orders = Order.objects.all()
    total = {
        'total': orders.count(),
        'delivered': orders.filter(status='Delivered').count(),
        'pending': orders.filter(status='Pending').count()
    }

    customers = Customer.objects.all()
    c_orders = {}
    for c in customers:
        c_orders[c.id] = [c, c.order_set.all().count()]

    context = {
        'orders': orders,
        'customers': customers,
        'total': total,
        'c_orders': c_orders
    }

    return render(request, 'accounts/dashboard.html', context)


@login_required(login_url="login")
def products(request):
    products = Product.objects.all()

    return render(request, 'accounts/products.html', {'products': products})


def customer(request, pk):
    customer = Customer.objects.get(id=pk)
    orders = customer.order_set.all()
    total_orders = orders.count()

    my_filter = OrderFilter(request.GET, queryset=orders)
    orders = my_filter.qs

    context = {
        'customer': customer,
        'orders': orders,
        'total_orders': total_orders,
        'my_filter': my_filter
    }
    return render(request, 'accounts/customer.html', context)


@login_required(login_url="login")
def createOrder(request, pk):
    customer = Customer.objects.get(id=pk)
    form = OrderForm(initial={'customer': customer})

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form': form}
    return render(request, 'accounts/order_form.html', context)


@login_required(login_url="login")
def updateOrder(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form': form}
    return render(request, 'accounts/order_form.html', context)


@login_required(login_url="login")
def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('/')

    context = {
        'header': "Attention!!",
        'msg': f"Are you sure you want to delete order {order}",
        'btn_class_confirm': "btn-danger",
        'btn_class_cancel': "btn-secondary"
    }
    return render(request, 'accounts/confirmation.html', context)
