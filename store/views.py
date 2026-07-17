from copy import copy
import unicodedata

from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from collections import OrderedDict
from django.core.paginator import Paginator
from django.contrib.messages.views import SuccessMessageMixin
from core.dashboards.configs import DashboardPageConfig
from core.dashboards.customer_pages import CUSTOMER_PAGES
from core.dashboards.pages import CustomerPage
from store.forms import CategoryUpdateForm, ProductUpdateForm
from tools.required_role import RoleRequiredMixin

from django.urls import reverse, reverse_lazy
from django.views.generic import (
    DeleteView,
    DetailView,
    CreateView,
    ListView,
    UpdateView,
    View,
    TemplateView,
)
from django.db.models import Count, DecimalField, ExpressionWrapper, F, Q, Sum, Min, Max

from store.models import Banner, Brand, Category, Product, ProductImage

from tools.breadcrumb_utils import get_breadcrumb
from tools.utils import get_or_create_cart
from django.contrib.auth.decorators import login_required
from core.dashboards.templates import CUSTOMER_PARTIALS
from core.dashboards.context import CUSTOMER_CONTEXTS


# Dashboard
class DashboardBaseView(RoleRequiredMixin, TemplateView):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "categories": Category.active.all().order_by("display_order", "name"),
                "brands": Brand.objects.all(),
                "form": ProductUpdateForm(),
                "total_products_count": Product.objects.count(),
                "total_categories_count": Category.objects.count(),
                "products": Product.active.filter(create_by=self.request.user),
            }
        )
        return context


# baseview cho từng roles


class DashboardAdminBaseView(DashboardBaseView):
    template_name = "dashboards/dashboard_admin.html"
    allowed_roles = ["admin"]


class DashboardStaffBaseView(DashboardBaseView):
    template_name = "dashboards/dashboard_staff.html"
    allowed_roles = ["admin", "staff"]


class DashboardCustomerView(View):
    def get(self, request):
        return redirect("store:customer_overview")


class DashboardCustomerBaseView(DashboardBaseView):
    template_name = "dashboards/dashboard_customer.html"

    allowed_roles = ["admin", "staff", "customer"]

    page = None

    @property
    def config(self):
        return CUSTOMER_PAGES[self.kwargs["page"]]

    @property
    def page(self):
        return self.kwargs["page"]

    def get_template_names(self):

        if self.request.htmx:
            return [self.template_name]

        return [self.template_name]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pages = []

        for config in CUSTOMER_PAGES.values():
            item = copy(config)
            item.active = item.page == self.page
            pages.append(item)

        context["current_partial"] = self.config.template
        context["current_page"] = self.page
        context["customer_pages"] = pages
        context.update(self.config.get_context(self.request))

        return context


# Dashboard customer


class DashboardCustomerPageView(DashboardCustomerBaseView):
    pass


class DashboardCustomerOverviewView(DashboardCustomerBaseView):
    page = CustomerPage.OVERVIEW


class DashboardCustomerOrdersView(DashboardCustomerBaseView):
    page = CustomerPage.ORDERS


class DashboardCustomerProductsView(DashboardCustomerBaseView):
    page = CustomerPage.PRODUCTS


class DashboardCustomerWishlistView(DashboardCustomerBaseView):
    page = CustomerPage.WISHLIST


class DashboardCustomerCouponsView(DashboardCustomerBaseView):
    page = CustomerPage.COUPONS


class DashboardCustomerAddressView(DashboardCustomerBaseView):
    page = CustomerPage.ADDRESS


class DashboardCustomerSettingsView(DashboardCustomerBaseView):
    page = CustomerPage.SETTINGS


class DashboardCustomerAccountView(DashboardCustomerBaseView):
    page = CustomerPage.ACCOUNT


class DashboardStaffView(DashboardBaseView):
    template_name = "dashboards/dashboard_staff.html"
    allowed_roles = ["admin", "staff"]


class DashboardAdminView(DashboardBaseView):
    template_name = "dashboards/dashboard_admin.html"
    allowed_roles = ["admin"]


# setmain


@login_required
def set_main_image(request, pk):
    img = get_object_or_404(ProductImage, pk=pk)
    product = img.product
    ProductImage.objects.filter(product=product).update(is_main=False)
    img.is_main = True
    img.save(update_fields=["is_main"])
    return redirect("store:product_detail", slug=product.slug)


# Search
def normalize_search_text(value):
    value = unicodedata.normalize("NFD", value or "")
    value = "".join(char for char in value if unicodedata.category(char) != "Mn")
    return value.replace("đ", "d").replace("Đ", "D").casefold()


def product_matches_search(product, normalized_query):
    normalized_name = normalize_search_text(product.name)
    normalized_brand = normalize_search_text(
        product.brand.name if product.brand else ""
    )
    normalized_category = normalize_search_text(
        product.category.name if product.category else ""
    )
    searchable_text = " ".join([normalized_name, normalized_brand, normalized_category])
    words = searchable_text.split()

    if normalized_name.startswith(normalized_query):
        return 0
    if any(word.startswith(normalized_query) for word in words):
        return 1
    if normalized_query in searchable_text:
        return 2
    return None


def search(request):
    query = request.GET.get("query", "").strip()
    if request.headers.get("HX-Request") and not query:
        return HttpResponse("")

    products = (
        Product.active.filter(is_sold=False)
        .select_related("brand", "category")
        .prefetch_related("images")
    )
    if query:
        normalized_query = normalize_search_text(query)
        matched_products = []

        for product in products:
            rank = product_matches_search(product, normalized_query)
            if rank is not None:
                matched_products.append((rank, product.name.casefold(), product))

        products = [
            product
            for _, _, product in sorted(matched_products, key=lambda item: item[:2])
        ]
    context = {"products": products, "query": query}
    if request.headers.get("HX-Request"):
        return render(request, "partials/filter/search_results.html", context)
    return render(request, "core/search.html", context)


# Brand
class BrandCreateView(SuccessMessageMixin, RoleRequiredMixin, CreateView):
    model = Brand
    fields = ["name"]
    template_name = "store/brands/brand_form.html"
    success_message = "Đã tạo thương hiệu thành công: %(name)s"
    success_url = reverse_lazy("store:brand_create")
    allowed_roles = [
        "admin",
    ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Tạo thương hiệu"
        return context


# Products
class ProductCreateView(RoleRequiredMixin, SuccessMessageMixin, CreateView):
    model = Product
    form_class = ProductUpdateForm
    template_name = "partials/dashboard/base/product_form.html"
    success_message = "Đã tạo sản phẩm thành công: %(name)s"
    allowed_roles = ["admin", "staff"]

    def get_success_url(self):
        if self.request.user.is_superuser or self.request.user.role == "admin":
            return reverse("admin_dashboard")
        if self.request.user.role == "staff":
            return reverse("staff_dashboard")
        return reverse("store:home")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Thêm sản phẩm mới"
        if self.request.headers.get("HX-Request"):
            context["htmx_active"] = True
        return context

    def form_valid(self, form):
        form.instance.create_by = self.request.user
        response = super().form_valid(form)

        images = self.request.FILES.getlist("images")
        for index, img in enumerate(images):
            ProductImage.objects.create(
                product=self.object, order=index, image=img, is_main=(index == 0)
            )

        if self.request.headers.get("HX-Request"):
            return render(
                self.request,
                "partials/dashboard/base/product_form.html",
                {
                    "form": self.get_form_class()(),
                    "htmx_success": self.get_success_message(form.cleaned_data),
                    "htmx_active": True,
                },
            )

        return response

    def form_invalid(self, form):
        if self.request.headers.get("HX-Request"):
            return render(
                self.request,
                "partials/dashboard/base/product_form.html",
                {"form": form, "htmx_active": True},
                status=422,
            )

        return super().form_invalid(form)


class ProductDeleteView(RoleRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Product
    allowed_roles = ["admin", "staff"]

    def get_success_url(self):
        if self.request.user.is_superuser:
            return reverse("store:admin_dashboard")
        if self.request.user.is_staff:
            return reverse("store:staff_dashboard")

    def get_queryset(self):
        if self.request.user.role == "admin":
            return self.model.objects.all()
        return self.model.objects.filter(create_by=self.request.user)


class ProductUpdateView(RoleRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Product
    form_class = ProductUpdateForm
    slug_field = "slug"
    success_message = "Update product successfully!"
    template_name = "store/products/product_update_form.html"

    def get_success_url(self):
        return (
            reverse("admin_dashboard")
            if self.request.user.is_superuser
            else reverse("store:home")
        )

    def form_valid(self, form):

        response = super().form_valid(form)

        images = self.request.FILES.getlist("images")

        last_order = ProductImage.objects.filter(product=self.object).count()

        for index, img in enumerate(images):
            ProductImage.objects.create(
                product=self.object, image=img, order=last_order + index
            )

        return response

    def form_invalid(self, form):

        print("FORM INVALID")
        print(form.errors)
        print(form.non_field_errors())

        return super().form_invalid(form)


# Cart detail
def cart_detail(request):

    order = get_or_create_cart(request)

    context = {
        "order": order,
        "cart_items": order.items.all(),
        "total_amount": order.total_amount,
    }

    return render(
        request,
        "store/carts/cart_detail.html",
        context,
    )


def add_to_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    order = get_or_create_cart(request)
    order.add_product(product, quantity=1)

    if request.headers.get("HX-Request"):
        cart_items = list(order.items.all())
        cart_items_count = sum(item.quantity for item in order.items.all())
        return render(
            request,
            "partials/carts/cart_update.html",
            {
                "cart_items_count": cart_items_count,
                "cart_item": cart_items,
            },
        )

    return redirect(request.META.get("HTTP_REFERER", "/"))


class ProductDetailView(DetailView):
    model = Product
    slug_field = "slug"
    template_name = "store/products/product_detail.html"

    def get_queryset(self):
        return Product.objects.select_related(
            "category",
            "brand",
        ).prefetch_related(
            "images",
            "variants",
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        product = self.object
        variant_id = self.request.GET.get("variant")

        selected_variant = (
            product.variants.filter(id=variant_id).first() or product.variants.first()
        )

        context.update(
            {
                "selected_variant": selected_variant,
                "related_products": Product.active.filter(
                    category=product.category
                ).exclude(id=product.id)[:4],
                "featured_products": Product.active.filter(is_featured=True)[:4],
                "categories": Category.active.filter(
                    parent__isnull=True
                ).prefetch_related("children"),
            }
        )

        return context


# Category


class CategoryPermanentDeleteView(RoleRequiredMixin, View):

    def post(self, request, slug):

        category = get_object_or_404(Category.objects, slug=slug, is_active=False)

        category.hard_delete()

        messages.success(request, "Deleted permanently")

        return redirect("store:category_trash")


class CategoryTrashView(RoleRequiredMixin, ListView):

    model = Category

    template_name = "store/categories/trash.html"

    context_object_name = "categories"

    def get_queryset(self):

        return Category.objects.filter(is_active=False)


class CategoryDeleteView(SuccessMessageMixin, RoleRequiredMixin, DeleteView):
    model = Category
    allowed_roles = [
        "admin",
    ]

    def get_success_url(self):
        return reverse("admin_dashboard")

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        # 1. Kiểm tra điều kiện ngay tại View
        if self.object.category_products.filter(is_active=True).exists():
            messages.error(
                request,
                f"Không thể xóa danh mục '{self.object.name}' vì vẫn còn sản phẩm đang hoạt động bên trong!",
            )
            return HttpResponseRedirect(self.get_success_url())

        # 2. Nếu không vướng sản phẩm nào, tiến hành soft delete
        self.object.delete()
        return HttpResponseRedirect(self.get_success_url())


class CategoryRestoreView(RoleRequiredMixin, View):
    def post(self, request, slug):
        category = get_object_or_404(Category.objects, slug=slug, is_active=False)
        category.restore()

        messages.success(request, "Restore success")
        return redirect("store:category_trash")


class CategoryCreateView(RoleRequiredMixin, SuccessMessageMixin, CreateView):
    model = Category
    fields = ["name", "parent", "image", "icon_code"]
    success_message = "Create category successfully!"
    allowed_roles = ["admin", "staff"]

    def get_success_url(self):
        return (
            reverse("store:admin_dashboard")
            if self.request.user.is_superuser
            else reverse("store:staff_dashboard")
        )


class CategoryUpdateView(RoleRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Category
    form_class = CategoryUpdateForm
    success_message = "Category updated successfully!"
    template_name = "store/categories/category_update_form.html"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_success_url(self):
        return (
            reverse("admin_dashboard")
            if self.request.user.is_superuser
            else reverse("staff_dashboard")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "title": "Update category",
            }
        )
        return context


class CategoryDetailView(DetailView):
    model = Category
    context_object_name = "category"
    template_name = "store/categories/category_detail.html"

    def get_object(self):
        return get_object_or_404(Category.active, slug=self.kwargs["slug"])

    def get(self, request, *args, **kwargs):
        category = self.get_object()
        breadcrumb_items = OrderedDict()
        ancestors = []
        current = category
        while current:
            ancestors.insert(0, current)
            current = current.parent
        for cat in ancestors:
            breadcrumb_items[cat.name] = reverse(
                "store:category_detail", kwargs={"slug": cat.slug}
            )
        request.custom_breadcrumb = breadcrumb_items
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.object

        brand = self.request.GET.get("brand")
        min_p = self.request.GET.get("min_price")
        max_p = self.request.GET.get("max_price")
        sort = self.request.GET.get("sort")

        products = category.get_products_queryset(
            brand=brand, min_price=min_p, max_price=max_p, sort=sort
        )
        paginator = Paginator(products, 12)
        page_obj = paginator.get_page(self.request.GET.get("page"))

        price_range = category.get_products_queryset().aggregate(
            min_price=Min("price"),
            max_price=Max("price"),
        )
        context.update(
            {
                "breadcrumb": get_breadcrumb(category=category),
                "grouped_products": category.get_grouped_products(
                    brand=brand, min_price=min_p, max_price=max_p, sort=sort
                ),
                "page_obj": page_obj,
                "products": page_obj,
                "brands": Brand.objects.all(),
                "categories": Category.active.filter(
                    parent__isnull=True
                ).prefetch_related("children"),
                "custom_breadcrumb": getattr(self.request, "custom_breadcrumb", {}),
                "min_category_price": price_range["min_price"] or 0,
                "max_category_price": price_range["max_price"] or 0,
            }
        )
        return context


class HomeView(ListView):
    model = Product
    template_name = "core/index.html"

    def get_queryset(self):
        return Product.active.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        featured_categories = (
            Category.active.filter(category_products__isnull=False)
            .annotate(product_count=Count("category_products"))
            .order_by("-product_count")[:8]
        )
        best_sellers = [
            p
            for p in Product.active.all().prefetch_related("images")
            if p.is_bestseller
        ][:8]
        context.update(
            {
                "banners": Banner.objects.filter(is_active=True).order_by("order")[:5],
                "latest_products": Product.active.order_by(
                    "-created_at"
                ).prefetch_related("images")[:8],
                "best_sellers": best_sellers,
                "featured_categories": featured_categories,
            }
        )
        return context
