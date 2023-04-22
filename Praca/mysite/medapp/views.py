from collections import namedtuple
from importlib.metadata import PackageNotFoundError
from itertools import product
from django.contrib.auth import authenticate, forms
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import *
from django.contrib.auth.decorators import login_required
from .models import *
from django.views.generic import CreateView, UpdateView, DeleteView
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            Profile.objects.create(user=new_user)
            messages.success(request, f'Stworzono konto!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'medapp/register.html', {'form': form})

def contact(request):
    if request.method == 'POST':
        contact_form = ContactForm(request.POST)
        if contact_form.is_valid():
            contact_form.save()
            messages.success(request, 'Wysłano widomość!')
            return redirect('medapp:contact')
        else:
            messages.error(request, 'Błąd!')
    else:
        contact_form = ContactForm()
    return render(request,'medapp/contact.html',{'contact_form': contact_form})
    

def home(request):
    return render(request, 'medapp/home.html', {'title': 'Strona Główna'})


def categories(request):
    categories = Category.objects.all()
    return {'categories': categories}


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)

    p = Paginator(products, 12)
    page_number = request.GET.get('page', 1)

    try:
        page_obj = p.get_page(page_number)
    except PageNotAnInteger:
        page_obj = p.page(1)
    except EmptyPage:
        page_obj = p.page(p.num_pages)

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

        p = Paginator(products, 12)
        page_number = request.GET.get('page', 1)

        try:
            page_obj = p.get_page(page_number)
        except PageNotAnInteger:
            page_obj = p.page(1)
        except EmptyPage:
            page_obj = p.page(p.num_pages)
        
    return render(request, 'medapp/products/list.html',{'category': category, 'categories':categories,'products':products, 'page_obj':page_obj})


@login_required
def account(request):
    return render(request, 'medapp/account.html', {'title': 'Profil'})      


@login_required
def my_products(request):
    products = Product.objects.filter(author = request.user.id)
    return render(request, 'medapp/my_products.html',{'products':products})


@login_required
def order_list(request):
    orders = Order.objects.filter(product__author = request.user.id)
    return render(request, 'medapp/orders.html',{'orders':orders})


@login_required
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        order_form = OrderFrom(data=request.POST)
        if order_form.is_valid():
            cd = order_form.cleaned_data
            new_order = order_form.save(commit=False)
            new_order.user = request.user
            new_order.product = product
            order_form.save()
            messages.success(request, 'Zamówienie złożone pomyślnie!')
            return redirect('medapp:product_list')
        else:
            messages.error(request, 'Błąd!')
    else:
        order_form = OrderFrom(instance=request.user)
    return render(request, 'medapp/product_detail.html', {'product': product, 'order_form': order_form})


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    fields = ['category', 'name', 'image', 'description', 'price','available' ,'city', 'quantity']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    template_name ='medapp/product_update.html'
    fields = ['category', 'name', 'image', 'description', 'price' ,'available', 'city', 'quantity']
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        product = self.get_object()
        if self.request.user == product.author:
            return True
        else:
            return False


class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Product
    success_url ='/products/'

    def test_func(self):
        product = self.get_object()
        if self.request.user == product.author:
            return True
        else:
            return False


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile,data=request.POST,files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Edycja zakończona sukcesem!')
        else:
            messages.error(request, 'Błąd!')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request,'medapp/account_edit.html',{'user_form': user_form,'profile_form': profile_form})


@login_required
def profile_detail(request, pk):
    profile = get_object_or_404(Profile, pk=pk)
    products_user = Product.objects.filter(author = profile.user)
    return render(request, 'medapp/profile_detail.html', {'profile': profile, 'products_user': products_user})