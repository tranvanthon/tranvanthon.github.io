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
