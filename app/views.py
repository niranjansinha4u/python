from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views import View
from .models import Customer, Product, Cart, OrderPlaced
from .forms import CustomerRegistrationForm, CustomerProfileForm
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class ProductView(View):
    def get(self, request):
        mobile = Product.objects.filter(category='M')[:7] 
        laptop = Product.objects.filter(category='L') 
        gold_ring = Product.objects.filter(category='GR') 
        diamond_ring = Product.objects.filter(category='DR') 
        return render(request, 'app/home.html', {'mobile':mobile,'laptop':laptop,'gold_ring':gold_ring,'diamond_ring':diamond_ring})
        
class ProductDetail(View):
    def get(self,request,pk):
        product_id = Product.objects.filter(pk=pk)
        gotocart = False
        if request.user.is_authenticated:
            for product_idd in product_id:
                gotocart = Cart.objects.filter(Q(product=product_idd) & Q(user=request.user)).exists()
        return render(request, 'app/productdetail.html', {'product_details':product_id, 'gotocart':gotocart})


def mobile(request, data=None):
    if data == None:
        mobiles = Product.objects.filter(category='M').order_by('discounted_price')
        # category = Product.objects.get(category='M')

    elif data == 'Samsung' or data == 'Apple':
        mobiles = Product.objects.filter(category='M').filter(brand=data).order_by('discounted_price')
    elif data == 'Below-10k':
        mobiles = Product.objects.filter(category='M').filter(discounted_price__lt=10000).order_by('discounted_price')
    elif data == 'Below-20k':
        mobiles = Product.objects.filter(category='M').filter(discounted_price__lt=20000).order_by('discounted_price')
    elif data == 'Below-50k':
        mobiles = Product.objects.filter(category='M').filter(discounted_price__lt=50000).order_by('discounted_price')
    elif data == 'Above-10k':
        mobiles = Product.objects.filter(category='M').filter(discounted_price__gt=10000).order_by('discounted_price')
    elif data == 'Above-20k':
        mobiles = Product.objects.filter(category='M').filter(discounted_price__gt=20000).order_by('discounted_price')
    elif data == 'Above-50k':
        mobiles = Product.objects.filter(category='M').filter(discounted_price__gt=50000).order_by('discounted_price')
    
    return render(request, 'app/mobile.html', {'mobiles':mobiles})

def laptop(request, data=None):
    if data == None:
        laptops = Product.objects.filter(category='L').order_by('discounted_price')
    elif data == 'MacBook' or data == 'HP':
        laptops = Product.objects.filter(category='L').filter(brand=data).order_by('discounted_price')
    elif data == 'Below-10k':
        laptops = Product.objects.filter(category='L').filter(discounted_price__lt=10000).order_by('discounted_price')
    elif data == 'Below-20k':
        laptops = Product.objects.filter(category='L').filter(discounted_price__lt=20000).order_by('discounted_price')
    elif data == 'Below-50k':
        laptops = Product.objects.filter(category='L').filter(discounted_price__lt=50000).order_by('discounted_price')
    elif data == 'Above-10k':
        laptops = Product.objects.filter(category='L').filter(discounted_price__gt=10000).order_by('discounted_price')
    elif data == 'Above-20k':
        laptops = Product.objects.filter(category='L').filter(discounted_price__gt=20000).order_by('discounted_price')
    elif data == 'Above-50k':
        laptops = Product.objects.filter(category='L').filter(discounted_price__gt=50000).order_by('discounted_price')
    
    return render(request, 'app/laptop.html', {'laptops':laptops})

@login_required
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    Cart(user=user, product=product ).save()
    return redirect('/cart')

# def countCartItem(request):
#    global cartItems
#    if request.user.is_authenticated:
#        user = request.user
#        cartItems = len(Cart.objects.filter(user=user))
       
#        data={
#          'cartItems': cartItems  
#        }       
#        return HttpResponse(data)
@login_required
def show_cart(request):
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user=user)        
        amount = 0.0
        shipping_amount = 99.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == user]
        cartItems = 0
        
        if cart_product:
            # request.session['cartItems'] = cartItems 
            cartItems = len(cart_product)       
            for p in cart_product:
                tempAmt = (p.quantity*p.product.discounted_price)
                amount+= tempAmt
                total_amount = amount+shipping_amount
        
            cartData={
                'carts':cart,
                'cartDt':cart_product,
                'sAmt':shipping_amount,
                'pAmt':amount,
                'pTotalAmt':total_amount,
                'totalItems':cartItems
            }            
            return render(request, 'app/addtocart.html', cartData)
        else:
            return render(request, 'app/empty.html')
    # else:
    #     return render(request, 'app/login.html')

@login_required
def buy_now(request):
 return render(request, 'app/addtocart.html')

# def change_password(request):
#     return render(request, 'app/passwordchange.html')

class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        return render(request, 'app/customerregistration.html',{'form':form})
    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request, "User Created Sucessfully.")
            form.save()
        return render(request, 'app/customerregistration.html',{'form':form})
    
@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    def get(self, request):
        form = CustomerProfileForm()       
        return render(request, 'app/profile.html', {'form':form, 'active':'btn-primary'})
    
    def post(self, request):
        form = CustomerProfileForm(request.POST or None)
        if form.is_valid():
            current_user = request.user
            name = form.cleaned_data['name']
            phone = form.cleaned_data['phone']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']
            profile_reg = Customer(user=current_user, name=name, phone=phone, locality=locality, city=city, state=state, zipcode=zipcode)
            profile_reg.save()
            messages.success(request, "User Profile Updated Successfully.")            
        return render(request, 'app/profile.html', {'form':form, 'active':'btn-primary'})
            
@login_required
def address(request):
    add = Customer.objects.filter(user=request.user)
    return render(request, 'app/address.html', {'addr':add, 'active':'btn-primary'})

@login_required
def checkout(request):
    address = Customer.objects.filter(user=request.user)
    cart_items = Cart.objects.filter(user=request.user)
    amount = 0.0
    shipping_amount = 99.0
    total_amount = 0.0
    cart_product = [p for p in Cart.objects.all() if p.user == request.user]
    cartItems = 0
    if cart_product:
        # request.session['cartItems'] = cartItems 
        cartItems = len(cart_product)       
        for p in cart_product:
            tempAmt = (p.quantity*p.product.discounted_price)
            amount+= tempAmt
            total_amount = amount+shipping_amount
    return render(request, 'app/checkout.html', {'cart_items':cart_items, 'address':address, 'amount':amount, 'totalamount':total_amount,'totalItems':cartItems})

@login_required
def orders(request):
    op = OrderPlaced.objects.filter(user=request.user)
    return render(request, 'app/orders.html', {'order_placed':op})

@login_required
def payment_done(request):
    cust_id = request.GET.get('custid')
    customer = Customer.objects.get(id=cust_id)
    cart_items = Cart.objects.filter(user=request.user)
    for cart in cart_items:
        OrderPlaced(user=request.user, customer=customer, product=cart.product, quantity=cart.quantity).save()
        cart.delete()
    return redirect("/orders")

def plus_cart(request):
    if request.method == 'GET':
        product_id = request.GET['product_id']
        # print(product_id)
        cartObj = Cart.objects.get(Q(product=product_id) & Q(user=request.user))
        cartObj.quantity+=1
        cartObj.save()
        amount = 0.0
        shipping_amount = 99.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        cartItems = 0
        if cart_product:
            # request.session['cartItems'] = cartItems 
            cartItems = len(cart_product)       
            for p in cart_product:
                tempAmt = (p.quantity*p.product.discounted_price)
                amount+= tempAmt
                total_amount = amount+shipping_amount
        
            cartData={
                'quantity':cartObj.quantity,
                'amount':amount,
                'totalamount':total_amount
            }
        return JsonResponse(cartData)

def minus_cart(request):
    if request.method == 'GET':
        product_id = request.GET['product_id']
        # print(product_id)
        cartObj = Cart.objects.get(Q(product=product_id) & Q(user=request.user))
        cartObj.quantity-=1
        cartObj.save()
        amount = 0.0
        shipping_amount = 99.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        cartItems = 0
        if cart_product:
            # request.session['cartItems'] = cartItems 
            cartItems = len(cart_product)       
            for p in cart_product:
                tempAmt = (p.quantity*p.product.discounted_price)
                amount+= tempAmt
                total_amount = amount+shipping_amount
        
            cartData={
                'quantity':cartObj.quantity,
                'amount':amount,
                'totalamount':total_amount
            }
        return JsonResponse(cartData)
def remove_cart(request):
    if request.method == 'GET':
        product_id = request.GET['product_id']
        # print(product_id)
        cartObj = Cart.objects.get(Q(product=product_id) & Q(user=request.user))
        cartObj.delete()
        amount = 0.0
        shipping_amount = 99.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        cartItems = 0
        # request.session['cartItems'] = cartItems 
        cartItems = len(cart_product)       
        for p in cart_product:
            tempAmt = (p.quantity*p.product.discounted_price)
            amount+= tempAmt
            total_amount = amount+shipping_amount
    
        cartData={
            'amount':amount,
            'totalamount':total_amount,
            'cartItems':cartItems
        }
    return JsonResponse(cartData)        