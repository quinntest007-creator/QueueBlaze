from django.db import models
import os

# Create your models here.

class Product(models.Model):
    CATEGORY_CHOICES = [
        ('flower', 'Flowers'),
        ('edibles', 'Edibles'),
        ('concentrates', 'Concentrates'),
        ('accessories', 'Accessories'),
    ]
    
    STRAIN_CHOICES = [
        ('sativa', 'Sativa'),
        ('indica', 'Indica'),
        ('hybrid', 'Hybrid'),
        ('all', 'All'),
    ]
    
    # Icon choices for products
    ICON_CHOICES = [
        ('🌿', '🌿 Leaf'),
        ('🍁', '🍁 Maple'),
        ('🌸', '🌸 Flower'),
        ('🍀', '🍀 Clover'),
        ('🎋', '🎋 Bamboo'),
        ('🌺', '🌺 Hibiscus'),
        ('🍄', '🍄 Mushroom'),
        ('🌵', '🌵 Cactus'),
        ('🎄', '🎄 Christmas Tree'),
        ('🌲', '🌲 Evergreen'),
        ('🍃', '🍃 Herb'),
        ('☘️', '☘️ Shamrock'),
        ('🌱', '🌱 Seedling'),
        ('🌿', '🌿 Herb'),
        ('🍪', '🍪 Cookie'),
        ('🍬', '🍬 Candy'),
        ('🍫', '🍫 Chocolate'),
        ('🍩', '🍩 Donut'),
        ('🍦', '🍦 Ice Cream'),
        ('🧁', '🧁 Cupcake'),
        ('🍮', '🍮 Pudding'),
        ('🍭', '🍭 Lollipop'),
        ('💧', '💧 Drop'),
        ('🧪', '🧪 Test Tube'),
        ('💎', '💎 Diamond'),
        ('🔮', '🔮 Crystal Ball'),
        ('⚗️', '⚗️ Alembic'),
        ('🧴', '🧴 Lotion'),
        ('💊', '💊 Pill'),
        ('🏺', '🏺 Amphora'),
        ('🫙', '🫙 Jar'),
        ('📦', '📦 Box'),
        ('🛍️', '🛍️ Shopping Bag'),
        ('⚙️', '⚙️ Gear'),
        ('🔧', '🔧 Wrench'),
        ('🛠️', '🛠️ Tools'),
        ('🔥', '🔥 Fire'),
        ('💨', '💨 Smoke'),
        ('⚡', '⚡ Bolt'),
        ('🔋', '🔋 Battery'),
    ]
    
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='flower')
    strain = models.CharField(max_length=20, choices=STRAIN_CHOICES, default='hybrid')
    thc = models.CharField(max_length=50, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    icon = models.CharField(max_length=10, choices=ICON_CHOICES, default='🌿')
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name
    
    def delete(self, *args, **kwargs):
        # Delete the image file when product is deleted
        if self.image:
            if os.path.isfile(self.image.path):
                os.remove(self.image.path)
        super().delete(*args, **kwargs)


class SiteSettings(models.Model):
    site_name = models.CharField(max_length=200, default='QueueBlaze')
    site_description = models.TextField(blank=True)
    contact_phone = models.CharField(max_length=50, blank=True)
    contact_email = models.EmailField(blank=True)
    contact_address = models.TextField(blank=True)
    whatsapp_number = models.CharField(max_length=50, blank=True)
    operating_hours = models.CharField(max_length=200, blank=True)
    about_title = models.CharField(max_length=200, blank=True)
    about_content = models.TextField(blank=True)
    hero_title = models.CharField(max_length=200, blank=True)
    hero_subtitle = models.TextField(blank=True)
    
    # Bank Account Details for EFT
    bank_name = models.CharField(max_length=100, blank=True)
    account_number = models.CharField(max_length=50, blank=True)
    account_type = models.CharField(max_length=50, blank=True)
    branch_code = models.CharField(max_length=20, blank=True)
    account_holder = models.CharField(max_length=100, blank=True)
    payment_reference = models.CharField(max_length=100, blank=True)
    
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = 'Site Settings'
        verbose_name_plural = 'Site Settings'
    
    def __str__(self):
        return self.site_name


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    
    DELIVERY_TYPE_CHOICES = [
        ('delivery', 'Delivery'),
        ('pickup', 'Pickup'),
    ]
    
    PAYMENT_METHOD_CHOICES = [
        ('eft', 'EFT/Bank Transfer'),
        ('cash', 'Cash on Delivery'),
        ('stripe', 'Credit Card'),
    ]
    
    # Customer Info
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    customer_email = models.EmailField()
    customer_phone = models.CharField(max_length=50)
    
    # Delivery
    delivery_type = models.CharField(max_length=20, choices=DELIVERY_TYPE_CHOICES, default='delivery')
    shipping_option = models.CharField(max_length=50, blank=True)
    
    # Address
    address_street = models.CharField(max_length=255, blank=True)
    address_suburb = models.CharField(max_length=100, blank=True)
    address_city = models.CharField(max_length=100, blank=True)
    address_province = models.CharField(max_length=100, blank=True)
    address_postal_code = models.CharField(max_length=10, blank=True)
    
    # Payment
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, default='eft')
    
    # Order Details
    items_json = models.TextField()  # JSON string of items
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    shipping = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Order #{self.id} - {self.first_name} {self.last_name}"
