from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_view
from .forms import LoginForm, MyPasswordChangeForm, MyPasswordResetForm, MySetPasswordForm
from django.urls import include


urlpatterns = [
    path("", views.home),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path("category/<slug:value>", views.CategoryView.as_view(), name="category"),
    path("category-title/<value>",
         views.CategoryTitleView.as_view(), name="category_title"),
    path("product-detail/<int:pk>",
         views.ProductDetailView.as_view(), name="product_detail"),
    path("profile/", views.ProfileView.as_view(), name="profile"),
    path("address/", views.address, name="address"),
    path("update-address/<int:pk>",
         views.UpdateAddressView.as_view(), name="update_address"),
    
    path("search/", views.search, name="search"),
    path("wishlist/", views.show_wishlist, name="wishlist"),

    path("add-to-cart/", views.add_to_cart, name="add_to_cart"),
    path("cart/", views.show_cart, name="show_cart"),
    path("checkout/", views.CheckoutView.as_view(), name="checkout"),
    path('paymentdone/', views.payment_done, name='paymentdone'),
    path("orders/", views.orders, name="orders"),


    path("pluscart/", views.plus_cart),
    path("minuscart/", views.minus_cart),
    path("removecart/", views.remove_cart),

    path("addwishlist/", views.add_wishlist),
    path("removewishlist/", views.remove_wishlist),

    # authentication

    path("registration/", views.CustomerRegistrationView.as_view(),
         name="customer_registration"),
    path("accounts/login/", auth_view.LoginView.as_view(template_name="store/login.html",
         authentication_form=LoginForm), name="login"),
    path("password-change/", auth_view.PasswordChangeView.as_view(template_name="store/password_change.html",
         form_class=MyPasswordChangeForm, success_url="/password-change-done"), name="password_change"),
    path("password-change-done/", auth_view.PasswordChangeDoneView.as_view(template_name="store/password_change_done.html"),
         name="password_change_done"),
    path("logout/", auth_view.LogoutView.as_view(next_page="login"), name="logout"),

    path("password-reset/", auth_view.PasswordResetView.as_view(template_name="store/password_reset.html",
         form_class=MyPasswordResetForm), name="password_reset"),
    path("password-reset/done/", auth_view.PasswordResetDoneView.as_view(template_name="store/password_reset_done.html"),
         name="password_reset_done"),
    path("password-reset-confirm/<uidb64>/<token>/", auth_view.PasswordResetConfirmView.as_view(template_name="store/password_reset_confirm.html",
                                                                                                form_class=MySetPasswordForm), name="password_reset_confirm"),
    path("password-reset-complete/", auth_view.PasswordResetCompleteView.as_view(template_name="store/password_reset_complete.html"),
         name="password_reset_complete"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
