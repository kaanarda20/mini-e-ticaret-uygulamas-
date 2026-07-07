from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from .models import Product
from django.http import JsonResponse


def product_list(request):
    products = Product.objects.prefetch_related('images', 'variants').all()
    return render(request, 'shop/product_list.html', {'products': products})

@require_POST
def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    cart = request.session.get('cart', {})
    qty = int(request.POST.get('quantity', 1))
    variant_id = request.POST.get('variant_id')
    price = float(product.price)
    variant = None
    if variant_id:
        variant = product.variants.filter(id=variant_id).first()
        if variant:
            price += float(variant.additional_price)

    key = f"{product.id}:{variant.id if variant else ''}"
    cart_item = cart.get(key, {'name': product.name, 'price': str(price), 'quantity': 0, 'variant_id': variant.id if variant else None, 'variant_name': variant.name if variant else None})
    cart_item['quantity'] += qty
    cart[key] = cart_item
    request.session['cart'] = cart
    return redirect('cart')

def cart_view(request):
    cart = request.session.get('cart', {})
    total = sum(float(item['price'])*item['quantity'] for item in cart.values())
    return render(request, 'shop/cart.html', {'cart': cart, 'total': total})


def product_detail(request, pk):
    product = get_object_or_404(Product.objects.prefetch_related('images', 'variants'), pk=pk)
    return render(request, 'shop/product_detail.html', {'product': product})

@require_POST
def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        return JsonResponse({'status': 'error', 'message': 'Cart empty'}, status=400)
    request.session['cart'] = {}
    return JsonResponse({'status': 'success', 'message': 'Payment mocked, order placed'})
