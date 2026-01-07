from decimal import Decimal
from django.db import models
from django.contrib.auth.models import User 
from django.conf import settings
from django.db import models
# Create your models here.
class Product(models.Model):
    image = models.ImageField(upload_to='product_images/', blank=True, null=True, default='img/no-image.png')
    productName = models.CharField(max_length=191)
    description = models.TextField()
    price = models.DecimalField(max_digits= 10, decimal_places=2)
    stock = models.DecimalField(max_digits=6, decimal_places=2, default=0)   
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.productName
    
class Order(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Processing', 'Processing'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=5, decimal_places=2, default=1.00) 
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - {self.product.productName} ({self.user.username})"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to="avatars/", default="avatars/default.jpg")
    birthdate = models.DateField(null=True, blank=True)
    contact_no = models.CharField(max_length=20, null=True, blank=True)
    address = models.CharField(max_length=190, null=True, blank=True)

    def __str__(self):
        return str(self.user)
    
    # ✅ Get delivery address automatically from user's profile
    @property
    def delivery_address(self):
        try:
            return self.user.userprofile.address
        except UserProfile.DoesNotExist:
            return "No address provided"
    

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')  # Prevent duplicates

    def __str__(self):
        return f"{self.user.username} → {self.product.name}"
    

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    session_key = models.CharField(max_length=250, null=True, blank=True)

    def __str__(self):
        return f"Cart ({self.user.username if self.user else 'Guest'})"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("1.0"))

    def subtotal(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.product.productName} - {self.quantity}"


class SaveForLater(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.product.productName} saved by {self.user.username}"
    
class Transaction(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('COD', 'Cash on Delivery'),
        ('EWALLET', 'E-Wallet'),
    ]

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
        ('Failed', 'Failed'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    reference = models.CharField(max_length=100, blank=True, null=True)  # optional e-wallet ID

    def __str__(self):
        return f"{self.user.username} - {self.payment_method} - {self.status}"


class Notification(models.Model):
    NOTIF_TYPES = [
        ('order', 'Order'),
        ('system', 'System'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # null means admin notification
    message = models.TextField()
    url = models.CharField(max_length=255, blank=True, null=True)
    notif_type = models.CharField(max_length=50, choices=NOTIF_TYPES, default='system')
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.message[:50]} ({'Admin' if self.user is None else self.user.username})"