from django.shortcuts import render
from django.http import HttpResponse
from .models import product,contact,Orders,orderupdate
from math import ceil
import json
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import razorpay


client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))


# Create your views here.
# This section show the product in the home page 
def index(request):
    # products= product.objects.all()
    allProds=[]
    catprods= product.objects.values('category', 'product_id' , 'price')
    cats= {item["category"] for item in catprods}
    for cat in cats:
        prod=product.objects.filter(category=cat)
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allProds.append([prod, range(1, nSlides), nSlides])
    params={'allProds':allProds }
    return render(request,"shop/index.html", params)



 
# search a particular product  function
def searchMatch(query,item):
    ''' return true only if query math the items'''
    if query in item.desc.lower() or query in item.product_name.lower() or query in item.category.lower():
        return True
    else:
        return False

# search logic implemented here
def search(request):
    query=request.GET.get('search')
    allProds=[]
    catprods= product.objects.values('category', 'product_id' , 'price')
    cats= {item["category"] for item in catprods}
    for cat in cats:
        prodtemp=product.objects.filter(category=cat)
        prod=[item for item in prodtemp if searchMatch(query,item)]
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        if len(prod) !=0:
            allProds.append([prod, range(1, nSlides), nSlides])
    params={'allProds':allProds,"msg":""}
    if len(allProds)==0 or len(query)<2:
        return render(request,'shop/notfound.html')
        # params={'msg':"plese make sure to enter relevent search quary"}
    return render(request,"shop/search.html", params)
    # Tfidfvectorizer more advance ml model to search relavent 
    #  universal sentence encoder
    #  sk learn cosine


# This section work only with the about section 
def about(request):
    return render(request,'shop/about.html')


# This is used to conact section the user submit his /her form to contect us 
def contact_view(request):
    if request.method == "POST":
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        desc = request.POST.get('desc', '')
        # Validate phone
        try:
            phone = int(phone)
        except ValueError:
            phone = 0 
        contact_entry = contact(name=name, email=email, phone=phone, desc=desc)
        contact_entry.save()
        # return HttpResponse("Thanks for contacting us!",)
        return render(request, 'shop/thankyou.html')
    return render(request, 'shop/contact.html')


# Track your order where you reached 

def tracker(request):
    if request.method=="POST":
        orderId = request.POST.get('orderId', '')
        email = request.POST.get('email', '')
        try:
            order = Orders.objects.filter(order_id=orderId, email=email)
            if len(order)>0:
                update = orderupdate.objects.filter(order_id=orderId)
                updates = []
                for item in update:
                    updates.append({'text': item.update_desc, 'time': item.timestamp.strftime('%d-%m-%Y / %H:%M')})
                    response = json.dumps({"status":"success", "updates": updates, "itemsJson": order[0].items_json}, default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{"status":"noitem"}')
        except Exception as e:
            return HttpResponse('{"status":"error"}')

    return render(request, 'shop/tracker.html')

# product views 
def productview(request,my_id):
    # featch product using id 
    prod=product.objects.filter(product_id=my_id).first()
    # print(prod)
    return render(request,'shop/productview.html',{'prod':prod})

#Cheek out the product 
def cheekout(request):
    if request.method == "POST":
        items_json = request.POST.get('itemsjson', '')
        name = request.POST.get('name', '')
        amount = request.POST.get('amount', '').strip()
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        address = request.POST.get('address', '') + " " + request.POST.get('address2', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zipcode = request.POST.get('zipcode', '')

        if not amount.isdigit():
            return HttpResponse("Invalid or missing amount", status=400)

        amount = int(amount)

        order = Orders(
            items_json=items_json,
            name=name,
            email=email,
            phone=phone,
            address=address,
            city=city,
            state=state,
            zipcode=zipcode,
            amount=amount
        )
        order.save()

        update = orderupdate(order_id=order.order_id, update_desc="This Order has been placed")
        update.save()


        # Razorpay order create
        razorpay_order = client.order.create(dict(amount=amount * 100,currency='INR',payment_capture='1'))


        context = {
            'razorpay_key_id': settings.RAZORPAY_KEY_ID,
            'amount': amount * 100,
            'order_id': razorpay_order['id'],
            'order': order
        }
        return render(request, 'shop/razorpay_checkout.html',context)

    return render(request, 'shop/cheekout.html')

@csrf_exempt
def handlerequest(request):
    if request.method == "POST":
        try:
            razorpay_payment_id = request.POST.get('razorpay_payment_id')
            razorpay_order_id = request.POST.get('razorpay_order_id')
            razorpay_signature = request.POST.get('razorpay_signature')
            order_id = request.POST.get('order_id')

            # Verify the payment signature
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': razorpay_payment_id,
                'razorpay_signature': razorpay_signature
            }

            client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

            try:
                client.utility.verify_payment_signature(params_dict)

                # Optional: mark your order as paid in DB
                from .models import Orders
                order = Orders.objects.get(order_id=order_id)
                order.payment_id = razorpay_payment_id
                order.paid = True  # You can add a boolean field `paid` in Orders model
                order.save()

                return render(request, 'shop/payment_success.html', {
                    'payment_id': razorpay_payment_id,
                    'order': order
                })

            except razorpay.errors.SignatureVerificationError:
                return HttpResponse("Payment failed: Signature verification failed")

        except Exception as e:
            return HttpResponse(" Error: " + str(e))

    return HttpResponse("Invalid request method")