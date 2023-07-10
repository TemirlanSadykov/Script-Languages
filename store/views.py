from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .forms import SignUpForm, SignInForm, ProductForm, CommentForm
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Product
import requests
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from asgiref.sync import sync_to_async
from django.core.mail.backends.smtp import EmailBackend

def main(request):
    return render(request, 'main.html')

def restricted(request):
    return HttpResponse("Restricted! Sign up as a seller first!")

def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('product-list')
    else:
        form = SignUpForm()
    
    return render(request, 'sign_up.html', {'form': form})

def sign_in(request):
    if request.method == 'POST':
        form = SignInForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('product-list')
            else:
                form.add_error(None, 'Invalid username or password.')
    else:
        form = SignInForm()
    
    return render(request, 'sign_in.html', {'form': form})

def sign_out(request):
    logout(request)
    return redirect('main')

@login_required
def add_product(request):
    if request.user.user_type == 'seller':
        if request.method == 'POST':
            form = ProductForm(request.POST)
            if form.is_valid():
                product = form.save(commit=False)
                product.seller = request.user
                product.save()
                return redirect('product-list')
        else:
            form = ProductForm()
    
        return render(request, 'add_product.html', {'form': form})
    else:
        return redirect('restricted')
    
@login_required
def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})

@login_required
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    comments = product.comments.all()

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.save()
            product.comments.add(comment)
            return redirect('product_detail', product_id=product_id)
    else:
        form = CommentForm()

    return render(request, 'product_detail.html', {'product': product, 'comments': comments, 'comment_form': form})

@login_required
def become_seller(request):
    if request.user.user_type == 'customer':
        request.user.user_type = 'seller'
        request.user.save()
    return redirect('product-list')

@login_required
def view_product(request):
    if request.user.user_type == 'seller':
        products = Product.objects.filter(seller = request.user)
        return render(request, 'view_product.html', {'products': products})
    else:
        return redirect('restricted')
    
@login_required
def edit_product(request, product_id):
    if request.user.user_type == 'seller':
        product = get_object_or_404(Product, id=product_id)
        if request.method == 'POST':
            form = ProductForm(request.POST, instance=product)
            if form.is_valid():
                form.save()
                return redirect('product-list')
        else:
            form = ProductForm(instance=product)
        return render(request, 'edit_product.html', {'form': form})
    else:
        return redirect('restricted')

@login_required    
def purchase_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'purchase_product.html', {'product': product})

async def process_purchase(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        email = request.POST.get('email')
        product = await sync_to_async(get_object_or_404)(Product, id=product_id)
        image_url = product.image_url
        image_response = requests.get(image_url)
        image_content = image_response.content
        
        email_subject = f'Purchase Confirmation: {product.name}'
        email_body = render_to_string('purchase_email.html', {'product': product})
        
        attachment = (f'{product.name}.png', image_content, 'image/png')
        
        await send_email_async(email, email_subject, email_body, attachment)
        
        return render(request, 'purchase_email.html', {'product': product})
    
    return redirect('purchase-product')

async def send_email_async(email, subject, body, attachment=None):
    email_message = EmailMessage(subject=subject, body=body, from_email=settings.DEFAULT_FROM_EMAIL, to=[email])
    if attachment:
        email_message.attach(*attachment)
    backend = EmailBackend()
    await sync_to_async(backend.send_messages)([email_message])