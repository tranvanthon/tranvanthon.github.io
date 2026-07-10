from django.contrib.sites.shortcuts import get_current_site


# Lấy site_domain và site_name
def site_info(request):
    current_site = get_current_site(request)
    return {
        "site_name": current_site.name,
        "site_domain": current_site.domain,
    }


def nav_categories(request):
    from store.models import Category

    return {
        "nav_categories": Category.active.filter(parent__isnull=True)
        .prefetch_related("children")
        .order_by("display_order", "name")
    }
