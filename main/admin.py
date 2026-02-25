from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.cache import cache
from .models import Product, SiteSettings, Order
import json
import re

# Admin login
@csrf_exempt
def admin_login(request):
    if request.user.is_authenticated:
        return redirect('admin_dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('admin_dashboard')
        else:
            messages.error(request, 'Invalid credentials')
    return render(request, 'admin/login.html')

# Admin logout
def admin_logout(request):
    logout(request)
    return redirect('admin_login')

# Admin dashboard
@login_required
def admin_dashboard(request):
    total_products = Product.objects.count()
    active_products = Product.objects.filter(is_active=True).count()
    total_orders = Order.objects.count()
    pending_orders = Order.objects.filter(status='pending').count()
    
    recent_orders = Order.objects.all()[:5]
    
    context = {
        'total_products': total_products,
        'active_products': active_products,
        'total_orders': total_orders,
        'pending_orders': pending_orders,
        'recent_orders': recent_orders,
    }
    return render(request, 'admin/dashboard.html', context)

# Products management
@login_required
def admin_products(request):
    products = Product.objects.all()
    return render(request, 'admin/products.html', {'products': products})

# Add product
@login_required
def admin_product_add(request):
    if request.method == 'POST':
        # Handle image upload and convert to base64
        image_data = None
        content_type = None
        if request.FILES.get('image'):
            import base64
            img_file = request.FILES.get('image')
            image_data = base64.b64encode(img_file.read()).decode('utf-8')
            content_type = img_file.content_type
        
        product = Product(
            name=request.POST.get('name'),
            category=request.POST.get('category'),
            strain=request.POST.get('strain'),
            thc=request.POST.get('thc'),
            price=request.POST.get('price'),
            icon=request.POST.get('icon'),
            description=request.POST.get('description'),
            is_active=request.POST.get('is_active') == 'on',
            image=image_data,
            image_content_type=content_type
        )
        
        product.save()
        messages.success(request, 'Product added successfully!')
        return redirect('admin_products')
    return render(request, 'admin/product_form.html', {'product': None})

# Edit product
@login_required
def admin_product_edit(request, product_id):
    product = Product.objects.get(id=product_id)
    old_image = product.image
    
    if request.method == 'POST':
        product.name = request.POST.get('name')
        product.category = request.POST.get('category')
        product.strain = request.POST.get('strain')
        product.thc = request.POST.get('thc')
        product.price = request.POST.get('price')
        product.icon = request.POST.get('icon')
        product.description = request.POST.get('description')
        product.is_active = request.POST.get('is_active') == 'on'
        
        # Handle image upload/remove - store as base64 in database
        remove_image = request.POST.get('remove_image') == 'true'
        
        if remove_image:
            product.image = None
            product.image_content_type = None
        elif request.FILES.get('image'):
            import base64
            img_file = request.FILES.get('image')
            product.image = base64.b64encode(img_file.read()).decode('utf-8')
            product.image_content_type = img_file.content_type
        # Keep old image if no new upload and not removing
        
        product.save()
        messages.success(request, 'Product updated successfully!')
        return redirect('admin_products')
    return render(request, 'admin/product_form.html', {'product': product})

# Delete product
@login_required
def admin_product_delete(request, product_id):
    product = Product.objects.get(id=product_id)
    product.delete()
    messages.success(request, 'Product deleted successfully!')
    return redirect('admin_products')

# Orders management
@login_required
def admin_orders(request):
    orders = Order.objects.all()
    return render(request, 'admin/orders.html', {'orders': orders})

# Order detail
@login_required
def admin_order_detail(request, order_id):
    order = Order.objects.get(id=order_id)
    if request.method == 'POST':
        order.status = request.POST.get('status')
        order.notes = request.POST.get('notes')
        order.save()
        messages.success(request, 'Order updated successfully!')
        return redirect('admin_orders')
    return render(request, 'admin/order_detail.html', {'order': order})

# Delete order
@login_required
def admin_order_delete(request, order_id):
    order = Order.objects.get(id=order_id)
    order.delete()
    messages.success(request, 'Order deleted successfully!')
    return redirect('admin_orders')

# Site settings
@login_required
def admin_settings(request):
    settings, created = SiteSettings.objects.get_or_create(id=1)
    if request.method == 'POST':
        settings.site_name = request.POST.get('site_name')
        settings.site_description = request.POST.get('site_description')
        settings.contact_phone = request.POST.get('contact_phone')
        settings.contact_email = request.POST.get('contact_email')
        settings.contact_address = request.POST.get('contact_address')
        settings.whatsapp_number = request.POST.get('whatsapp_number')
        settings.operating_hours = request.POST.get('operating_hours')
        settings.about_title = request.POST.get('about_title')
        settings.about_content = request.POST.get('about_content')
        settings.hero_title = request.POST.get('hero_title')
        settings.hero_subtitle = request.POST.get('hero_subtitle')
        # Bank account details
        settings.bank_name = request.POST.get('bank_name')
        settings.account_number = request.POST.get('account_number')
        settings.account_type = request.POST.get('account_type')
        settings.branch_code = request.POST.get('branch_code')
        settings.account_holder = request.POST.get('account_holder')
        settings.payment_reference = request.POST.get('payment_reference')
        settings.save()
        messages.success(request, 'Settings saved successfully!')
        return redirect('admin_settings')
    return render(request, 'admin/settings.html', {'settings': settings})

# API for products (for frontend)
def api_products(request):
    products = Product.objects.filter(is_active=True)
    data = [{
        'id': p.id,
        'name': p.name,
        'category': p.category,
        'strain': p.strain,
        'thc': p.thc,
        'price': str(p.price),
        'icon': p.icon,
        'image': p.image_url,  # Returns data URL for database-stored images
        'description': p.description
    } for p in products]
    return JsonResponse(data, safe=False)

# API for site settings
def api_settings(request):
    settings, created = SiteSettings.objects.get_or_create(id=1)
    data = {
        'site_name': settings.site_name,
        'site_description': settings.site_description,
        'contact_phone': settings.contact_phone,
        'contact_email': settings.contact_email,
        'contact_address': settings.contact_address,
        'whatsapp_number': settings.whatsapp_number,
        'operating_hours': settings.operating_hours,
        'about_title': settings.about_title,
        'about_content': settings.about_content,
        'hero_title': settings.hero_title,
        'hero_subtitle': settings.hero_subtitle,
        'bank_name': settings.bank_name,
        'account_number': settings.account_number,
        'account_type': settings.account_type,
        'branch_code': settings.branch_code,
        'account_holder': settings.account_holder,
        'payment_reference': settings.payment_reference,
    }
    return JsonResponse(data)

# Create superuser command for first time setup
def create_admin():
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@queueblaze.co.za', 'admin123')
        print('Admin user created: admin / admin123')

# Save order from checkout
@csrf_exempt
def save_order(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            # Debug: print the received data
            print("Received order data:", data)
            
            # Extract customer data
            customer = data.get('customer', {})
            
            # Extract address data
            address = data.get('address', {}) or {}
            
            # Convert items to JSON string
            items_json = json.dumps(data.get('items', []))
            
            order = Order(
                first_name=customer.get('first_name', ''),
                last_name=customer.get('last_name', ''),
                customer_email=customer.get('email', ''),
                customer_phone=customer.get('phone', ''),
                
                delivery_type=data.get('delivery_type', 'delivery'),
                shipping_option=data.get('shipping_option') or 'standard',
                
                address_street=address.get('street', ''),
                address_suburb=address.get('suburb', ''),
                address_city=address.get('city', ''),
                address_province=address.get('province', ''),
                address_postal_code=address.get('postal_code', ''),
                
                payment_method=data.get('payment_method', 'eft'),
                
                items_json=items_json,
                subtotal=data.get('subtotal', 0),
                shipping=data.get('shipping', 0),
                total_amount=data.get('total', 0),
                
                notes=data.get('notes', ''),
                status='pending'
            )
            order.save()
            return JsonResponse({'success': True, 'order_id': order.id})
        except json.JSONDecodeError as e:
            print("JSON Decode Error:", str(e))
            return JsonResponse({'success': False, 'error': 'Invalid JSON: ' + str(e)}, status=400)
        except Exception as e:
            print("Order Save Error:", str(e))
            import traceback
            traceback.print_exc()
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
    return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)

# Save contact inquiry with rate limiting and spam protection
@csrf_exempt
def save_inquiry(request):
    if request.method == 'POST':
        try:
            # Get client IP for rate limiting
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ip = x_forwarded_for.split(',')[0]
            else:
                ip = request.META.get('REMOTE_ADDR', 'unknown')
            
            # Rate limiting: Max 3 submissions per hour per IP
            rate_limit_key = f'rate_limit_inquiry_{ip}'
            submissions = cache.get(rate_limit_key, 0)
            
            if submissions >= 3:
                return JsonResponse({
                    'success': False, 
                    'error': 'Too many requests. Please try again later.'
                }, status=429)
            
            data = json.loads(request.body)
            
            # Validate required fields
            name = data.get('name', '').strip()
            email = data.get('email', '').strip()
            
            if not name or not email:
                return JsonResponse({
                    'success': False, 
                    'error': 'Name and email are required.'
                }, status=400)
            
            # Validate email format
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            
            if not re.match(email_pattern, email):
                return JsonResponse({
                    'success': False, 
                    'error': 'Invalid email format.'
                }, status=400)
            
            # Validate name length (prevent spam)
            if len(name) > 100:
                return JsonResponse({
                    'success': False, 
                    'error': 'Name too long.'
                }, status=400)
            
            # Get other fields with limits
            phone = data.get('phone', '')[:20]
            subject = data.get('subject', 'General')[:100]
            message = data.get('message', '')[:2000]
            
            # Honeypot check (hidden field - should be empty)
            honeypot = data.get('website', '')
            if honeypot:
                # Don't reveal we caught them, just silently succeed
                return JsonResponse({'success': True})
            
            # Create order with inquiry details
            order = Order(
                first_name=name.split()[0] if name else '',
                last_name=' '.join(name.split()[1:]) if name and len(name.split()) > 1 else '',
                customer_email=email,
                customer_phone=phone,
                delivery_type='pickup',
                payment_method='eft',
                items_json='[]',
                subtotal=0,
                shipping=0,
                total_amount=0,
                notes=f"Contact Inquiry - Subject: {subject}\n\nMessage: {message}",
                status='pending'
            )
            order.save()
            
            # Increment rate limit counter
            cache.set(rate_limit_key, submissions + 1, 3600)
            
            return JsonResponse({'success': True})
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
    return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)

