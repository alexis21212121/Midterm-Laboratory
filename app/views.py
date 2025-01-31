from django.shortcuts import render, redirect
from django.views.generic import CreateView, DetailView, TemplateView, ListView
from django.urls import reverse_lazy
from .forms import UserRegistrationForm
from .models import UserProfile
from django.contrib.auth.models import User
from .models import UserProfile, Product, Cart
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView, DeleteView
from django import forms
from django.contrib.auth import update_session_auth_hash
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Category, Cart
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from decimal import Decimal
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .models import Order, OrderItem
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.mixins import UserPassesTestMixin
from .forms import ProductForm



class HomePageView(TemplateView):
    template_name = 'app/home.html'

class ProfileView(TemplateView):
    template_name = 'app/profile_view.html'

class AboutPageView(TemplateView):
    template_name = 'app/about.html'

class ForgotPassPageView(TemplateView):
    template_name = 'app/forgotpass.html'

class ContactPageView(TemplateView):
    template_name = 'app/contact.html'


class ProductListView(ListView):
    model = Product
    template_name = 'app/menu.html'
    context_object_name = 'products'

class UserRegistrationView(CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'app/signup.html'
    success_url = reverse_lazy('home')  

    def form_valid(self, form):
        """Override form_valid to log the user in after successful registration."""
        user = form.save() 

        login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
        messages.success(self.request, "Registration successful!")
        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        """Redirect to home if the user is already logged in."""
        if request.user.is_authenticated:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)


class ProductDetailView(DetailView):
    model = Product
    template_name = 'app/product_detail.html'
    context_object_name = 'product'


class SignInPageView(View):
    def get(self, request):
        """Render the sign-in page on GET request."""
        return render(request, 'app/signin.html')

    def post(self, request):
        """Handle the login logic on POST request."""
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)  
            messages.success(request, f"Welcome, {user.username}!")

            # Redirect to the admin dashboard if user is an admin
            if user.is_staff or user.is_superuser:
                return redirect('admin_dashboard')  # Customize this URL to your admin page

            return redirect('home')  # Regular user redirection
        else:
            messages.error(request, "Invalid email or password.")
            return render(request, 'app/signin.html')


class ChangePasswordForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter new password'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm new password'}))

    class Meta:
        model = User
        fields = ['password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")

        return cleaned_data



class ChangePasswordView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ChangePasswordForm  
    template_name = 'app/change_password.html'

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])  
        user.save()

       
        update_session_auth_hash(self.request, user)

        messages.success(self.request, "Your password has been successfully changed.")
        
  
        return redirect('home')

    def get_success_url(self):
        return reverse_lazy('home')



class DeleteAccountView(LoginRequiredMixin, DeleteView):
    model = User
    template_name = 'app/delete_account.html'
    success_url = reverse_lazy('home')

    def get_object(self, queryset=None):
        return self.request.user


def filter_products(request):
    category_id = request.GET.get('category_id')
    if category_id:
        products = Product.objects.filter(categories__id=category_id)  # Products in the selected category
    else:
        products = Product.objects.none()  # No products if no category is provided

    data = [
        {
            'id': product.id,
            'name': product.name,
            'price': f'{product.price:.2f}',
        }
        for product in products
    ]
    return JsonResponse({'products': data})

@login_required
def add_to_cart(request):
    if request.method == "POST":
        product_id = request.POST.get("product_id")
        quantity = int(request.POST.get("quantity", 1))
        product = get_object_or_404(Product, id=product_id)

        cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)
        if not created:
            cart_item.quantity += quantity  # Increase quantity if item exists
        cart_item.save()

        total_items = Cart.objects.filter(user=request.user).count()  # Count total cart items

        return JsonResponse({
            "success": True,
            "message": f"{product.name} added to cart!",
            "product_name": product.name,  # 🔹 New: Return product name
            "total_items": total_items
        })

    return JsonResponse({"success": False, "error": "Invalid request"}, status=400)

@login_required
def cart_view(request):
    user = request.user
    cart_items = Cart.objects.filter(user=user)
    total_price = sum(item.total_price for item in cart_items)  # ✅ Remove parentheses

    # Ensure the total price is added to context
    context = {
        'cart_items': cart_items,
        'total_price': total_price
    }
    return render(request, 'app/cart.html', context)
    

def update_cart(request):
    if request.method == "POST":
        item_id = request.POST.get("item_id")
        quantity = int(request.POST.get("quantity", 1))
        cart_item = get_object_or_404(Cart, id=item_id, user=request.user)

        # ✅ Ensure quantity is always at least 1
        cart_item.quantity = max(1, quantity)
        cart_item.save()

        # ✅ Fix: Use total_price as a property (no parentheses)
        item_total = cart_item.total_price  # ✅ Fix here
        total_price = sum(item.total_price for item in Cart.objects.filter(user=request.user))  # ✅ Fix here

        return JsonResponse({
            "success": True,
            "item_total": f"{item_total:.2f}",
            "new_total": f"{total_price:.2f}"
        })

    return JsonResponse({"success": False, "error": "Invalid request"}, status=400)

@require_POST  # ✅ Ensures only POST requests are allowed
def remove_from_cart(request):
    if request.method == "POST":
        item_id = request.POST.get("item_id")
        try:
            cart_item = Cart.objects.get(id=item_id, user=request.user)
            cart_item.delete()
            
            # ✅ Recalculate the total price
            cart_items = Cart.objects.filter(user=request.user)
            new_total = sum(item.total_price for item in cart_items)

            return JsonResponse({"success": True, "new_total": new_total})
        except Cart.DoesNotExist:
            return JsonResponse({"success": False, "error": "Item not found."})
    
    return JsonResponse({"success": False, "error": "Invalid request."})

def menu_view(request):
    from .models import Category  # Move import here
    categories = Category.objects.prefetch_related('products').all()
    return render(request, 'app/menu.html', {'categories': categories})

@login_required
def place_order(request):
    if request.method == "POST":
        user = request.user
        cart_items = Cart.objects.filter(user=user)

        if not cart_items.exists():
            return JsonResponse({"success": False, "error": "Your cart is empty."})

        # ✅ Create a new order
        order = Order.objects.create(user=user)

        # ✅ Move cart items to OrderItem
        for cart_item in cart_items:
            OrderItem.objects.create(
                order=order,  
                product=cart_item.product,
                quantity=cart_item.quantity,
                price=cart_item.product.price
            )

        # ✅ Clear the cart after order is placed
        cart_items.delete()

        return JsonResponse({"success": True, "order_id": order.id})

    return JsonResponse({"success": False, "error": "Invalid request"}, status=400)

@login_required
def order_tracking(request):
    orders = Order.objects.filter(user=request.user).order_by('-date')

    # Compute the total price for each order and each item
    for order in orders:
        total_price = 0
        for item in order.order_items.all():
            item.total_price = item.quantity * item.price  # Calculate item total price
            total_price += item.total_price
        order.total_price = total_price  # Add the total order price

    context = {
        'orders': orders
    }
    return render(request, 'app/order_tracking.html', context)

@login_required
@require_POST
def cancel_order(request):
    order_id = request.POST.get("order_id")
    
    try:
        order = Order.objects.get(id=order_id, user=request.user)
        # Ensure order is in "pending" state before cancellation
        if order.status.lower() == "pending":
            order.delete()
            return JsonResponse({"success": True})
        else:
            return JsonResponse({"success": False, "error": "Order cannot be canceled."})
    
    except Order.DoesNotExist:
        return JsonResponse({"success": False, "error": "Order not found."})

    return JsonResponse({"success": False, "error": "Invalid request."}, status=400)

@staff_member_required
def update_order_status(request, order_id):
    order = Order.objects.get(id=order_id)
    if request.method == "POST":
        new_status = request.POST.get("status")
        order.status = new_status
        order.save()
        return redirect("admin_orders")  # Redirect to an admin orders list page

    return render(request, "admin/update_order_status.html", {"order": order})

class AdminDashboardView(UserPassesTestMixin, TemplateView):
    template_name = 'app/admin_dashboard.html'

    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Fetch all products and add them to the context
        context['products'] = Product.objects.all()
        return context

class AddProductView(View):
    def get(self, request):
        form = ProductForm()
        return render(request, 'app/add_product.html', {'form': form})

    def post(self, request):
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Product added successfully!")
            return redirect('admin_dashboard')  # Redirect to admin dashboard or products list
        return render(request, 'app/add_product.html', {'form': form})

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'image', 'price', 'stock', 'categories']

@login_required
@staff_member_required
def manage_orders(request):
    users_with_orders = User.objects.prefetch_related('orders').all()
    return render(request, 'app/manage_orders.html', {'users_with_orders': users_with_orders})

@login_required
@staff_member_required
def update_order_status(request, user_id):
    user_orders = Order.objects.filter(user_id=user_id)
    
    if request.method == 'POST':
        new_status = request.POST.get('status')
        user_orders.update(status=new_status)  # Update all orders of the user
        messages.success(request, f"All orders of {user_orders.first().user.username} updated to {new_status}!")
        return redirect('manage_orders')

    return render(request, 'app/update_order_status.html', {'user_orders': user_orders})

@login_required
@staff_member_required
def remove_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    print(f"Deleting order {order.id}")  # Debugging line
    order.delete()
    return JsonResponse({'success': True, 'order_id': order_id})

class EditProductView(View):
    def get(self, request, pk=None):
        # If a product is selected, fetch it
        if pk:
            selected_product = get_object_or_404(Product, pk=pk)
            form = ProductForm(instance=selected_product)
        else:
            selected_product = None
            form = ProductForm()

        # Pass all products and the selected product to the context
        context = {
            'products': Product.objects.all(),
            'selected_product': selected_product,
            'form': form,
        }
        return render(request, 'app/edit_product.html', context)

    def post(self, request, pk):
        # Handle the form submission for editing a product
        product = get_object_or_404(Product, pk=pk)
        form = ProductForm(request.POST, request.FILES, instance=product)

        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')  # Redirect back to the dashboard after saving

        return render(request, 'app/edit_product.html', {'form': form, 'product': product})

def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == "POST":
        product.delete()
        messages.success(request, "Product deleted successfully.")
        return redirect('admin_dashboard')  # Redirect to the dashboard or another relevant page

    return redirect('edit_product', pk=pk)

