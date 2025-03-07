from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from .forms import *
from django.contrib.auth.decorators import login_required
from .models import *
from django.views.generic import CreateView, UpdateView, DeleteView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def register(request):
    """
    Handles the user registration process.

    If the request method is POST, it validates the submitted form data. 
    If the form is valid, a new user is created. 

    Args:
        request: The HTTP request object.

    Returns:
        A rendered response with the registration form or a redirect to the login page 
        if the registration is successful.
    """
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
    """
    Handles the contact form submission.

    If the request method is POST, it validates the submitted form data. 
    If the form is valid, the contact message is saved.

    Args:
        request: The HTTP request object.

    Returns:
        A rendered response with the contact form or a redirect to the contact page 
        if the form submission is successful.
    """
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
    """
    Renders the home page of the application.

    Args:
        request: The HTTP request object.

    Returns:
        A rendered response with the 'home' page template and the context containing 
        the title of the page.
    """
    return render(request, 'medapp/home.html', {'title': 'Strona Główna'})


def categories(request):
    """
    Retrieves all categories from the database.

    Args:
        request: The HTTP request object.

    Returns:
        A dictionary containing all the categories in the 'categories' key.
    """
    categories = Category.objects.all()
    return {'categories': categories}


def product_list(request, category_slug=None):
    """
    Displays a list of available products, optionally filtered by category.

    Args:
        request: The HTTP request object.
        category_slug: An optional slug for filtering products by category.

    Returns:
        A rendered response with the 'product list' template, including the 
        filtered products, categories, and pagination information.
    """
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
    """
    Renders the user's profile page, only for authenticated users.

    Args:
        request: The HTTP request object.

    Returns:
        A rendered response with the 'account' page template.
    """
    return render(request, 'medapp/account.html', {'title': 'Profil'})      


@login_required
def my_products(request):
    """
    Displays the list of products created by the currently logged-in user.

    Args:
        request: The HTTP request object.

    Returns:
        A rendered response with the 'my_products' page template, displaying 
        the user's products.
    """
    products = Product.objects.filter(author = request.user.id)
    return render(request, 'medapp/my_products.html',{'products':products})


@login_required
def order_list(request):
    """
    Displays the list of orders for products created by the currently logged-in user,
    only for authenticated users.

    Args:
        request: The HTTP request object.

    Returns:
        A rendered response with the 'orders' page template, displaying 
        the user's orders.
    """
    orders = Order.objects.filter(product__author = request.user.id)
    return render(request, 'medapp/orders.html',{'orders':orders})


@login_required
def product_detail(request, pk):
    """
    Displays the details of a specific product and handles the order form submission,
    only for authenticated users.

    Args:
        request: The HTTP request object.
        pk: The primary key of the product to be displayed.

    Returns:
        A rendered response with the 'product_detail' page template, 
        displaying the product details and order form.
    """
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
    """
    View for creating a new product.

    Inherits from:
        LoginRequiredMixin: Ensures that only authenticated users can access this view.
        CreateView: Provides the functionality to create a new instance of a model.

    Attributes:
        model: The model associated with the form (Product).
        fields: The fields to be included in the form for creating a product.

    Methods:
        form_valid(form): Customizes the form submission by assigning the current user 
                          as the product's author before saving the product.
    
    Args:
        request: The HTTP request object.
    """
    model = Product
    fields = ['category', 'name', 'image', 'description', 'price','available' ,'city', 'quantity']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    View for updating an existing product.

    Inherits from:
        LoginRequiredMixin: Ensures that only authenticated users can access this view.
        UserPassesTestMixin: Ensures that only the author of the product can update it.
        UpdateView: Provides functionality to update an existing instance of a model.

    Attributes:
        model: The model associated with the form (Product).
        template_name: The template to be used for rendering the product update form.
        fields: The fields to be included in the form for updating a product.

    Methods:
        form_valid(form): Customizes the form submission by assigning the current user 
                          as the product's author before saving the updated product.
        test_func(): Checks if the current user is the author of the product and 
                     grants permission to update it.

    Args:
        request: The HTTP request object.
    """
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
    """
    View for deleting an existing product.

    Inherits from:
        LoginRequiredMixin: Ensures that only authenticated users can access this view.
        UserPassesTestMixin: Ensures that only the author of the product can delete it.
        DeleteView: Provides functionality to delete an existing instance of a model.

    Attributes:
        model: The model associated with the deletion (Product).
        success_url: The URL to redirect to after successfully deleting the product.

    Methods:
        test_func(): Checks if the current user is the author of the product and 
                     grants permission to delete it.

    Args:
        request: The HTTP request object.
    """
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
    """
    View for editing the user's account and profile information,
    only for authenticated users.

    Args:
        request: The HTTP request object, which contains the user's data and the form submissions.

    Returns:
        A rendered HTML page with the edit forms for the user account and profile.
    """
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
    """
    View for displaying the details of a other user profile,
    only for authenticated users.

    Args:
        request: The HTTP request object.
        pk: The primary key of the profile being viewed.

    Returns:
        A rendered HTML page showing the user's profile information and the list of products 
        authored by that user.
    """
    profile = get_object_or_404(Profile, pk=pk)
    products_user = Product.objects.filter(author = profile.user)
    return render(request, 'medapp/profile_detail.html', {'profile': profile, 'products_user': products_user})