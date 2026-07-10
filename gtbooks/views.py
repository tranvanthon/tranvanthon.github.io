from django.http import HttpResponse
from django.shortcuts import render
from store.models import Product, Order
from django.views.generic import ListView


def hello(request):
    if request.headers.get("HX-Request"):
        return render(request, "partials/hello.html")
    return render(request, "core/index.html")


def profile(request):
    return HttpResponse("<h2>Đây là hồ sơ của bạn</h2>")


class DashboardView(ListView):
    model = Product
    template_name = "dashboards/dashboard_admin.html"

    def get_template_names(self):
        if self.request.headers.get("HX-Request"):
            return ["partials/dashboard/base/products.html"]
        return [self.template_name]


class ProductListView(ListView):
    model = Product
    template_name = "dashboards/dashboar.html"
    context_object_name = "products"

    def get_template_names(self):
        if self.request.headers.get("HX-Request"):
            return ["partials/dashboard/base/products.html"]
        return [self.template_name]


class ProductFilterView(ListView):

    model = Product
    template_name = "partials/products/product_table.html"

    def get_queryset(self):

        category = self.request.GET.get("category")

        if category:
            return Product.objects.filter(category_id=category)

        return Product.objects.all()
