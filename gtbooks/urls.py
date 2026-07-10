from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from gtbooks import views

urlpatterns = [
    path("hello/", views.hello, name="hello"),
    path("profile/", views.profile, name="profile"),
    path("product_list/", views.ProductListView.as_view(), name="product_list"),
    path("products/filter/", views.ProductFilterView.as_view(), name="product_filter"),
    path(
        "profiles/",
        include(
            "profiles.urls",
        ),
    ),
    path("", include("store.urls")),
    path("profiles/", include("allauth.urls")),
    path("admin/", admin.site.urls),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
