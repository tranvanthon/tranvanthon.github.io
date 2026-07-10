from dataclasses import dataclass

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
