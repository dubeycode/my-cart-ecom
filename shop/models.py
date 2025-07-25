from django.db import models
from django.utils.timezone import now
# Create your models here.
class product(models.Model):
    product_id=models.AutoField(primary_key=True)
    product_name=models.CharField(max_length=50)
    category=models.CharField(max_length=50,default="")
    subcategory=models.CharField(max_length=50,default="")
    price=models.IntegerField(default=0)
    desc=models.CharField(max_length=600)
    pub_date=models.DateField()
    image=models.ImageField(upload_to="shop/imges",default="")
    
    def __str__(self):
        return self.product_name
    

# contact models 

class contact(models.Model):
    msg_id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=50)
    email=models.CharField(max_length=40,default="")
    phone=models.IntegerField(default=0)
    desc=models.CharField(max_length=1000,default="")

    def __str__(self):
        return self.name
    
# order items models 
class Orders(models.Model):
    order_id=models.AutoField(primary_key=True)
    items_json=models.CharField(max_length=50000)
    amount=models.IntegerField(default=0)
    name=models.CharField(max_length=100)
    email=models.CharField(max_length=100,default="")
    address=models.CharField(max_length=100)
    city=models.CharField(max_length=100)
    state=models.CharField(max_length=100)
    zipcode=models.CharField(default=0)
    phone=models.CharField(max_length=6,default=00)
    payment_id = models.CharField(max_length=100, blank=True, null=True)
    paid = models.BooleanField(default=False)




# order update models  
class orderupdate(models.Model):
    update_id=models.AutoField(primary_key=True)
    order_id=models.IntegerField(default="")
    update_desc=models.CharField(max_length=5000)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return self.update_desc[0:7] + "...."

    
