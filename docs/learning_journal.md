# Lộ trình học:

Bài 1: Tách dashboard_customer.html thành layout + partial (không dùng HTMX).
Bài 2: Thay onclick="showPage()" bằng HTMX.
Bài 3: Học get_template_names().
Bài 4: Học get_context_data().
Bài 5: Học get_queryset().
Bài 6: CreateView + form_valid().
Bài 7: UpdateView + form_valid().
Bài 8: DeleteView.
Bài 9: Search, filter, pagination bằng HTMX.

## 2026-07-10

- DashboardPageConfig chỉ nên chứa Configuration.
- current_page là State.
- active không nên lưu trong Config.
- View truyền current_page vào context.
- Config có thể có get_context() để giảm coupling.

## "Thầy, mình tiếp tục GTBooks. Mình đã học đến DashboardPageConfig."

## Chỉ mở rộng khi em gõ: "Giải thích sâu".

Nếu em muốn học cực tiết kiệm token

Em chỉ cần dùng các lệnh sau:

"Gọn." → Trả lời ≤ 5 câu.
"Hint." → Chỉ gợi ý, không đáp án.
"Đáp án." → Chỉ đưa đáp án.
"Giải thích sâu." → Phân tích kỹ.
"Tiếp." → Sang bài mới.

# Buổi chiều

- Template là dữ liệu(property) thì:
  - config.template không có ()
- Method (behavior) thì phải có ()
  - config.get_template()
  - config.get_context(request)
  - config.can_access(user)
- get_context() phải luông trả về một dict.

1.  Tái cấu trúc template:
    class DashboarCustomerBaseView: # code
    def get_context_date(self, \*\*kwargs):
    #...code
    context["customer_pages"]=CUSTOMER_PAGES.values()
    context["current_page"]=self.page
    return context
    Mục đích: để tạo slidebar tự động và active khi chọn

2.  thêm:
    @property
    def config(self):
    return CUSTOMER_PAGES[self.kwargs["page"]]

    @property
    def page(self):
    return self.kwargs["page"]

3.  Gọi:

    def get_template_names(self):

        if self.request.htmx:
            return self.config

        return [self.template_name]

    def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)

        context["current_partial"] = self.config.template
        context["current_page"] = self.page
        context["customer_pages"] = CUSTOMER_PAGES.values()
        context.update(self.config.context(self.request))

        return context

4.  Trong template
    {% for config in customer_pages %}
    <div class="nav-link"
              hx-get="{% url 'store:customer_partial' config.page %}"
              hx-target="#page-content"
              hx-swap="innerHTML">
    <i class="{{ config.icon }}"></i> {{ config.title }}
    </div>
    {% endfor %}

# Buổi sáng ngày 10/01/2026

# Bài 1: Active Menu Hiện tại Sidebar:

1. Kiến thức:
   {% for config in customer_pages %}

<div class="nav-link"> <i class="{{ config.icon }}"></i>
{{ config.title }}
</div>
{% endfor %} 
# Chọn 
A. {% if config.page == current_page %} hay 
B. {% if config == current_page %}
chọn: A 
* Giải thích: config là một object, còn config.page là thuộc tính dùng để so sánh.

2.  Chỉnh template:
    <div class="nav-link {% if config.page == current_page %}active{% endif %}"
            hx-get="{% url 'store:customer_partial' config.page %}"
            hx-target="#page-content"
            hx-swap="innerHTML"
            hx-push-url="true">

            <i class="{{ config.icon }}"></i>
            {{ config.title }}

    </div>
    # Như trên thì chỉ mới lấy được link và reload lại mới active.

3.  Cách active trong htmx
    @Server quyết định HTML. HTMX chỉ vận chuyển và thay thế HTML.
    1.  HTMX thực hiện 1 request để lấy dữ liệu:
        Người thiết kế HTMX sẽ cần thêm: html Đoạn này thay ngoài vùng hiện tại.
    2.  hx-swap-oob và hx-select-oob:

        # HTMX sẽ hiểu:

            page-content → thay vào hx-target như bình thường.
            sidebar → à, cái này không thuộc target hiện tại, nhưng vì có hx-swap-oob nên mình cập nhật Sidebar luôn.
            topbar → cập nhật Topbar luôn.

            👉 Chỉ với một request.

        # slow:

            Click Orders
                    │
                    ▼
            1 Request
                    │
                    ▼
            Server render:

            ✓ Sidebar (active mới)

            ✓ Page Content (Orders)

                    │
                    ▼
            HTMX tự cập nhật cả hai vùng.

4.  Kiến thức cần nhớ:
    Bài toán
    │
    ▼
    Sidebar không Active
    │
    ▼
    HTMX chỉ thay #page-content
    │
    ▼
    Muốn cập nhật Sidebar
    │
    ├── 2 Request ❌
    │
    ├── Render cả Dashboard ❌ (tốn HTML)
    │
    └── 1 Request + Update nhiều vùng
    │
    ▼
    hx-swap-oob ✅
    # Config mô tả hệ thống. Context mô tả request.
5.  Tạo thuộc tính url để template gọi rất đẹp code:
    from django.urls import reverse

    # @dataclass

    class DashboardPageConfig:
    page: CustomerPage
    title: str
    icon: str
    template: str
    context: Callable

    # @property

        def url(self):
            return reverse(
                "store:customer_partial",
                kwargs={"page": self.page},
            )

    # Lợi ích khi dùng thuộc tính url không cần phải chỉnh template mà chỉ sửa

# Ngày 13 tháng 7 năm 2026

# Chủ đề: hx-swap-oob

Gợi nhớ khi sang new chat
#core/config.py

from dataclasses import dataclass

from django.urls import reverse

from core.dashboards.pages import CustomerPage

@dataclass

class DashboardPageConfig:

    page: CustomerPage

    title: str

    icon: str

    template: str

    context: callable

    form: object = None

    roles: list[str] | None = None

    def get_context(self, request):

        return self.context(request)

    @property

    def url(self):

        return reverse(

            "store:customer_partial",

            kwargs={"page": self.page},

        )

    def is_active(self, current_page):

        return self.page == current_page

    def active_class(self, current_page):

        return "active" if self.is_active(current_page) else ""

#views.py

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

            return [self.config.template]



        return [self.template_name]



    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)



        pages = []

        customer_pages = CUSTOMER_PAGES.values()

        for config in customer_pages:

            item = copy(config)

            item.active = item.page == self.page

            pages.append(item)



        context["current_partial"] = self.config.template

        context["current_page"] = self.page

        context["customer_pages"] = pages

        context.update(self.config.get_context(self.request))



        return context

#pages.py

from enum import StrEnum

class CustomerPage(StrEnum):

    SIDEBAR = "sidebar"

    OVERVIEW = "overview"

    PRODUCTS = "products"

    ORDERS = "orders"

    WISHLIST = "wishlist"

    ADDRESS = "address"

    COUPONS = "coupons"

    SETTINGS = "settings"

    ACCOUNT = "account"

# customer_pages.py

from core.dashboards.configs import DashboardPageConfig

from core.dashboards.context import (

    account_context,

    address_context,

    coupons_context,

    overview_context,

    product_context,

    settings_context,

    wishlist_context,

)

from core.dashboards.pages import CustomerPage

OVERVIEW = DashboardPageConfig(

    page=CustomerPage.OVERVIEW,

    title="Tổng quan",

    icon="bi bi-speedometer2",

    template="partials/dashboard/overview.html",

    context=overview_context,

)

ACCOUNT = (....

)

PRODUCTS = DashboardPageConfig(

    .....

)

ORDERS = DashboardPageConfig(

......

)

WISHLIST = DashboardPageConfig(

.....

)

ADDRESS = DashboardPageConfig(

.....

)

SETTINGS = DashboardPageConfig(

.....

)

COUPONS = DashboardPageConfig(

    ...

)

CUSTOMER_PAGES = {

..
}

# Bản copy để các active copy nó chịu trách nhiệm riêng:

    from copy import copy

    pages = []

    for config in CUSTOMER_PAGES.values():
        item = copy(config)
        item.active = (item.page == self.page)
        pages.append(item)

    context["customer_pages"] = pages

    Sau đó Template:
     <a
        hx-get="{{ config.url }}"
        class="{% if config.active %}active{% endif %}">

# Không phải HTMX lấy overview sau. mà là:

HTMX không làm việc với template.++> Đúng hơn phải nói: HTMX chỉ nhìn HTML cuối cùng mà Django render ra.

# flow:

1. Browser
   │
   ▼
2. HTMX gửi request
   │
   ▼
3. Django render xong TOÀN BỘ dashboard_customer.html
   │
   ▼
4. current_partial quyết định include overview/orders/...
   │
   ▼
5. Django sinh ra HTML hoàn chỉnh
   │
   ▼
6. HTMX mới dùng hx-select="#page-content"
   │
   ▼
7. HTMX cắt đúng phần #page-content
   │
   ▼
8. HTMX thay vào hx-target="#page-content"
   # Ngày 17 tháng 7 năm 2026

- Muốn hx-swap-oob="true" hoạt động thì phải có request trang sidebar. Cách để nó hoạt động là sử dụng hx-select="#page-content" trong
  if self.request.htmx:
  return [self.template_names]

  # slow:

        Server
            │
            ▼
        dashboard_customer.html
            │
            ▼
        HTML hoàn chỉnh
            │
            ▼
        hx-select
            │
            ▼
        #page-content

  - Lúc này hx-select nó sẽ lấy #page-content trước sau đó mới cho phép hx-target hoạt động.
  - Vì vậy, side cũng được load ngay từ đầu do đó không bị reload lại.

    # hx-select trả lời câu hỏi: "Lấy phần nào trong HTML?"

    # hx-swap-oob trả lời câu hỏi: "Ngoài phần chính, còn cập nhật thêm vùng nào?"
