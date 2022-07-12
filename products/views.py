from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseBadRequest
from django.conf import settings # new
from django.http.response import JsonResponse # new
from django.views.decorators.csrf import csrf_exempt # new

from products.form import BrandForm, ProductForm,UserForm
from . models import Brand, Cart, Category, Product,MyUser 
import razorpay
# Create your views here.
razorpay_client=razorpay.Client(
auth=(settings.RAZOR_KEY_ID,settings.RAZOR_KEY_SECRET)
)


def purchase(request):
    session_email=request.session['saved_email']
    cart_items=Cart.objects.filter(user_email=session_email)

    total=0
    for items in cart_items:
        total+=items.price
    razorpay_order = razorpay_client.order.create(dict(amount=total,
                                                       currency="INR",
                                                       payment_capture='0'))
 
    # order id of newly created order.
    razorpay_order_id = razorpay_order['id']
    callback_url = 'paymenthandler/'
 
    # we need to pass these details to frontend.
    context = {}
    context['razorpay_order_id'] = razorpay_order_id
    context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
    context['razorpay_amount'] = total
    context['currency'] = "INR"
    context['callback_url'] = callback_url
 
    return render(request, 'products/purchase.html', context=context)
# we need to csrf_exempt this url as
# POST request will be made by Razorpay
# and it won't have the csrf token.
@csrf_exempt
def paymenthandler(request):
 
    # only accept POST request.
    if request.method == "POST":
        try:
           
            # get the required parameters from post request.
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }
 
            # verify the payment signature.
            result = razorpay_client.utility.verify_payment_signature(
                params_dict)
            if result is None:
                amount = 20000  # Rs. 200
                try:
 
                    # capture the payemt
                    razorpay_client.payment.capture(payment_id, amount)
 
                    # render success page on successful caputre of payment
                    return render(request, 'paymentsuccess.html')
                except:
 
                    # if there is an error while capturing payment.
                    return render(request, 'paymentfail.html')
            else:
 
                # if signature verification fails.
                return render(request, 'paymentfail.html')
        except:
 
            # if we don't find the required parameters in POST data
            return HttpResponseBadRequest()
    else:
       # if other than POST request is made.
        return HttpResponseBadRequest()


def Brands(request):
    brand=Brand.objects.all()
    return render(template_name="products/brands.html",request=request,context={"brandlist":brand})
def products(request):
    cart_items=[]
    if(isLoggedIn(request)==True):
        session_email=request.session['saved_email']
        cart_items=Cart.objects.filter(user_email=session_email)
    product=Product.objects.all()
    categories=Category.objects.all()
    
    
    return render(template_name="products/new_product_save.html",
    request=request,context={"productList":product,"cart_size":cart_items.count,"categoryList":categories })



def home(request):
    if request.session.has_key('saved_email'):
        user_email=request.session['saved_email']
        password=request.session['saved_password']
        myUser= MyUser.objects.get(email=user_email)
        if myUser:
            if myUser.password==password:
                return redirect("/products/")

    userForm=UserForm()
    return render(template_name="products/home.html",request=request,context={"form":userForm})



def delete(request):
    product_name=request.GET['item_name']
    Cart.objects.filter(item_name=product_name).delete()
    return redirect('/cart/')
def addToCart(request):
    if(isLoggedIn(request)!=True):
        return redirect("/home") 
    product_name=request.GET['product']
    product_id=request.GET['id']
    product_price=request.GET['price']
    
    try:
        object=Cart.objects.get(product_id=product_id,user_email=request.session['saved_email'])
        object.quanitity += 1
        object.price= int(object.quanitity) * int(product_price)
        object.save()
    except Cart.DoesNotExist:
        c=Cart()
        c.product_id=product_id
        c.item_name=product_name
        c.quanitity=1
        c.user_email=request.session['saved_email']
        c.price=product_price
        c.save()

    return redirect("/")


    

def addBrandName(request):
    newBrand=BrandForm()
    return render(template_name='products/new_Brand.html',request=request,context={'brandform':newBrand})


def addNewProduct(request):
    newProduct=ProductForm()
    return render(template_name='products/new_product.html',request=request,context={'product_form':newProduct})

def save_brand(request):
    newBrand=BrandForm(request.POST,request.FILES)
    if newBrand.is_valid():
        newBrand.save()
        return redirect("/brands/")
    else:
        return redirect("/add_new_brand/")



# new
@csrf_exempt
def stripe_config(request):
    if request.method == 'GET':
        stripe_config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_config, safe=False)

import stripe
@csrf_exempt
def create_checkout_session(request):
    if request.method == 'GET':
        domain_url = 'http://localhost:8000/'
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            # Create new Checkout Session for the order
            # Other optional params include:
            # [billing_address_collection] - to display billing address details on the page
            # [customer] - if you have an existing Stripe Customer ID
            # [payment_intent_data] - capture the payment later
            # [customer_email] - prefill the email input in the form
            # For full details see https://stripe.com/docs/api/checkout/sessions/create

            # ?session_id={CHECKOUT_SESSION_ID} means the redirect will have the session ID set as a query param
            checkout_session = stripe.checkout.Session.create(
                success_url=domain_url + 'success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=domain_url + 'cancelled/',
                payment_method_types=['card'],
                mode='payment',
                line_items=[
                    {
                        'name': 'T-shirt',
                        'quantity': 1,
                        'currency': 'usd',
                        'amount': '2000',
                    }
                ]
            )
            return JsonResponse({'sessionId': checkout_session['id']})
        except Exception as e:
            return JsonResponse({'error': str(e)})

from django.views.generic.base import TemplateView
class SuccessView(TemplateView):
    template_name = 'products/success.html'


class CancelledView(TemplateView):
    template_name = 'products/cancelled.html'


def save_user(request):
    newUser=UserForm(request.POST,request.FILES)
    if newUser.is_valid():
        nu=newUser.save(commit=False)
        try:
            MyUser.objects.get(email=nu.email)
            return HttpResponse("<h2>Email already exists</h2>")
        except MyUser.DoesNotExist:
            nu.save()
            return HttpResponse("<h2>Registration Successfull. </h2 ><a href='/'>Go to Login Page</a>")
    else:
        return HttpResponse("<h2>User data not saved, Register Again</h2>")


def logout(request):
    del request.session['saved_email']
    return redirect("/")

def save_product(request):
    newproduct=ProductForm(request.POST,request.FILES)
    if newproduct.is_valid():
        newproduct.save()
        return redirect("/")
    else:
        return redirect("/add_new_product/")

def validate_user(request):
    user_email=request.POST['email']
    password=request.POST['psw']
    myUser=MyUser.objects.get(email=user_email)
    if myUser:
        if myUser.password==password:
            request.session['saved_email']=user_email
            request.session['saved_password']=password

            return redirect("/")
        else:
            return HttpResponse("<h2>EMail password combination is not correct</h2>")
    else:
        return HttpResponse("<h2>Entered Email doesn't exists</h2>")

def isLoggedIn(request):
    if request.session.has_key('saved_email'):
        return True
    else:
        return False

def category(request):
    type=request.GET["type"]
    product=Product()
    if type=="all":
        product=Product.objects.all()
    else:
        category=Category.objects.get(category_name=type)
        product=Product.objects.filter(product_category=category.id)
    categories=Category.objects.all()
    if(isLoggedIn(request)==True):
        session_email=request.session['saved_email'] 
        cart_items=Cart.objects.filter(user_email=session_email)
        return render(template_name="products/new_product_save.html",
        request=request,context={"productList":product,"cart_size":cart_items.count,"categoryList":categories })
    return render(template_name="products/new_product_save.html",
    request=request,context={"productList":product,"categoryList":categories })

def cart(request):
    if(isLoggedIn(request)!=True):
        return redirect("/") 
    
    session_email=request.session['saved_email']
    cart_items=Cart.objects.filter(user_email=session_email)

    total=0
    for items in cart_items:
        total+=items.price

    razorpay_order = razorpay_client.order.create(dict(amount=total,
                                                       currency="INR",
                                                       payment_capture='0'))
 
    # order id of newly created order.
    razorpay_order_id = razorpay_order['id']
    callback_url = 'paymenthandler/'
 
    # we need to pass these details to frontend.
    context = {}
    context['razorpay_order_id'] = razorpay_order_id
    context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
    context['razorpay_amount'] = total
    context['currency'] = "INR"
    context['callback_url'] = callback_url

    
    context['cart_items'] = cart_items
    
    context['total'] = total
    return render(request,"products/cart.html",context=context)

def cart_plus(request):
    
    product_name=request.GET['item_name']
    object=Cart.objects.get(item_name=product_name,user_email=request.session['saved_email'])
    product_price= object.price/object.quanitity
    object.quanitity += 1
    object.price= int(object.quanitity) * int(product_price)
    object.save()
    return redirect("/cart")

def cart_minus(request):
   product_name=request.GET['item_name']
   object=Cart.objects.get(item_name=product_name,user_email=request.session['saved_email'])
   product_price= object.price/object.quanitity
   object.quanitity -= 1
   object.price= int(object.quanitity) * int(product_price)
   object.save()
   return redirect("/cart")


def searchbar(request):
    search=request.GET["search"]
    Product=Product()
   
    Product=Product.objects.filter(product_name__contains=search)
   
    categories=Category.objects.all()
    session_email=request.session['saved_email']
    cart_items=Cart.objects.filter(user_email=session_email)
    
    return render(template_name="products/new_product_save.html",
    request=request,context={"newproduct":Product,"cart_size":cart_items.count,"categoryList":categories })

def desc(request):
    p_id=request.GET["id"]
    item=Product.objects.get(id=p_id)
    return render(request,"products/description.html",{"desc":item})


    