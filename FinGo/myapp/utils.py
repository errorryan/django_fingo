from .models import Cart

def get_cart(request):
    # Logged-in user
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        return cart

    # Guest user → use session
    if not request.session.session_key:
        request.session.create()

    cart, created = Cart.objects.get_or_create(session_key=request.session.session_key)
    return cart
