from django.shortcuts import render, redirect
from django.views import View
from django.http import JsonResponse
from urllib import request
from django.db.models import Q, Count
from django.contrib import messages
from . models import Product, Customer, Cart, OrderPlace, Payment, Wishlist
from . forms import CustomerRegistrationForm, CustomerProfileForm
from django.conf import settings
import razorpay
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


# Create your views here.

def home(request):
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    return render(request, 'store/home.html', locals())

def about(request):
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    return render(request, 'store/about.html', locals())

def contact(request):
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    return render(request, 'store/contact.html', locals())


class CategoryView(View):
    def get(self, request, value):
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))
            
        order_by = request.GET.get('order_by')
        if order_by == 'title':
            product = Product.objects.filter(category=value).order_by('title')
        elif order_by == 'price':
            product = Product.objects.filter(category=value).order_by('selling_price')
        else:
            product = Product.objects.filter(category=value)

        if request.GET.get('order_direction') == 'desc':
            product = product.reverse()
        
        # product = Product.objects.filter(category=value)
        title = Product.objects.filter(category=value).values("title")
        return render(request, 'store/category.html', locals())


class CategoryTitleView(View):
    def get(self, request, value):
        product = Product.objects.filter(title=value)
        title = Product.objects.filter(
            category=product[0].category).values("title")
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))
        return render(request, 'store/category.html', locals())


class ProductDetailView(View):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        wishlist = Wishlist.objects.filter(Q(product=product) & Q(user=request.user.id))
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))
        return render(request, 'store/product_detail.html', locals())


class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))            
        return render(request, 'store/customer_registration.html', locals())

    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration Successful")
        else:
            messages.warning(request, "Registration Failed")
        return render(request, 'store/customer_registration.html', locals())


@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    def get(self, request):
        form = CustomerProfileForm()
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))
        return render(request, 'store/profile.html', locals())

    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            city = form.cleaned_data['city']
            address = form.cleaned_data['address']
            mobile = form.cleaned_data['mobile']
            reg = Customer(user=user, name=name, city=city,
                           address=address, mobile=mobile)
            reg.save()
            messages.success(request, "Profile Saved Successfully")
        else:
            messages.warning(request, "Profile Failed")
        return render(request, 'store/profile.html', locals())


@login_required
def address(request):
    add = Customer.objects.filter(user=request.user)
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    return render(request, 'store/address.html', locals())


@method_decorator(login_required, name='dispatch')
class UpdateAddressView(View):
    def get(self, request, pk):
        add = Customer.objects.get(pk=pk)
        form = CustomerProfileForm(instance=add)
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))
        return render(request, 'store/update_address.html', locals())

    def post(self, request, pk):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            add = Customer.objects.get(pk=pk)
            add.name = form.cleaned_data['name']
            add.city = form.cleaned_data['city']
            add.address = form.cleaned_data['address']
            add.mobile = form.cleaned_data['mobile']
            add.save()
            messages.success(request, "Profile Updated Successfully")
        else:
            messages.warning(request, "Profile Update Failed")

        return redirect("address")


@login_required
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get("product_id")
    product = Product.objects.get(id=product_id)
    Cart(user=user, product=product).save()
    return redirect("/cart")

@login_required
def show_cart(request):
    user = request.user
    cart = Cart.objects.filter(user=user)
    amount = 0
    for c in cart:
        value = c.quantity * c.product.selling_price
        amount = amount + value
    totalamount = amount
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    return render(request, 'store/add_to_cart.html', locals())

def show_wishlist(request):
    user = request.user
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    product = Wishlist.objects.filter(user=user)
    return render(request, 'store/wishlist.html', locals())


@method_decorator(login_required, name='dispatch')
class CheckoutView(View):
    def get(self, request):
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))
        user = request.user
        add = Customer.objects.filter(user=user)
        cart_items = Cart.objects.filter(user=user)
        amount = 0
        for c in cart_items:
            value = c.quantity * c.product.selling_price
            amount = amount + value
        totalamount = amount
        payamount = int(totalamount * 100)
        client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
        data = {"amount": payamount, "currency": "USD", "receipt": "order_rcptid_12"}
        payment_response = client.order.create(data=data)
        # print(payment_response)
        order_id = payment_response['id']
        order_status = payment_response['status']
        if order_status == 'created':
            payment = Payment(user=user, amount=totalamount,
                              order_id=order_id, payment_status=order_status)
            payment.save()
        return render(request, 'store/checkout.html', locals())


@login_required
def payment_done(request):
    order_id = request.GET.get('order_id')
    payment_id = request.GET.get('payment_id')
    cust_id = request.GET.get('cust_id')
    # print (f"order={order_id}, pay={payment_id}, cust={cust_id}")
    user = request.user
    customer = Customer.objects.get(id=cust_id)
    payment = Payment.objects.get(order_id=order_id)
    payment.paid = True
    payment.payment_id = payment_id
    payment.save()
    cart = Cart.objects.filter(user=user)
    # print(cart)
    for c in cart:
        # print(c)
        OrderPlace(user=user, customer=customer, product=c.product, quantity=c.quantity, payment_mode=payment).save()
        c.delete()
    return redirect("orders")

@login_required
def orders(request):
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    order_place = OrderPlace.objects.filter(user=request.user)
    return render(request, 'store/orders.html', locals())

def plus_cart(request):
    if request.method == "GET":
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity += 1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.selling_price
            amount = amount + value
        totalamount = amount
        data = {
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': totalamount
        }
        return JsonResponse(data)

def minus_cart(request):
    if request.method == "GET":
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity -= 1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.selling_price
            amount = amount + value
        totalamount = amount
        data = {
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': totalamount
        }
        return JsonResponse(data)


def remove_cart(request):
    if request.method == "GET":
        prod_id = request.GET['prod_id']
        c = Cart.objects.filter(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.selling_price
            amount = amount + value
        totalamount = amount
        data = {
            'amount': amount,
            'totalamount': totalamount
        }
        return JsonResponse(data)


def add_wishlist(request):
    if request.method == "GET":
        prod_id = request.GET['prod_id']
        product = Product.objects.get(id=prod_id)
        user = request.user
        Wishlist(user=user, product=product).save()
        data = {
            'message': 'Product Added Successfully'
        }
        return JsonResponse(data)

def remove_wishlist(request):
    if request.method == "GET":
        prod_id = request.GET['prod_id']
        product = Product.objects.get(id=prod_id)
        user = request.user
        Wishlist.objects.filter(user=user, product=product).delete()
        data = {
            'message': 'Product Removed Successfully'
        }
        return JsonResponse(data)

def search(request):
    query = request.GET['search']
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    product = Product.objects.filter(Q(title__icontains=query))
    return render(request, 'store/search.html', locals())
