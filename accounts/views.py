from django.shortcuts import render, redirect
from .models import Customer, Product, Order
from .forms import OrderForm


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


def products(request):
    products = Product.objects.all()

    return render(request, 'accounts/products.html', {'products': products})


def customer(request, pk):
    customer = Customer.objects.get(id=pk)
    orders = customer.order_set.all()
    total_orders = orders.count()

    context = {
        'customer': customer,
        'orders': orders,
        'total_orders': total_orders
    }
    return render(request, 'accounts/customer.html', context)


def createOrder(request):
    form = OrderForm()
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form': form}
    return render(request, 'accounts/order_form.html', context)


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


def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('/')

    context = {
        # 'order': order,
        'header': "Attention!!",
        'msg': f"Are you sure you want to delete order {order}",
        'btn_class_confirm': "btn-danger",
        'btn_class_cancel': "btn-secondary"
    }
    return render(request, 'accounts/confirmation.html', context)
