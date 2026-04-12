from django.conf import settings
from django.contrib.sitemaps import Sitemap
from django.http import HttpResponse
from django.urls import reverse


PUBLIC_SITEMAP_ITEMS = [
    {
        "location": "/",
        "changefreq": "weekly",
        "priority": 1.0,
    },
    {
        "location": "/dashboard/onboarding/",
        "changefreq": "monthly",
        "priority": 0.5,
    },
    {
        "location": "/dashboard/ui-showcase/",
        "changefreq": "monthly",
        "priority": 0.3,
    },
]


class StaticViewSitemap(Sitemap):
    def items(self):
        return PUBLIC_SITEMAP_ITEMS

    def location(self, item):
        return item["location"]

    def changefreq(self, item):
        return item["changefreq"]

    def priority(self, item):
        return item["priority"]


def robots_txt(request):
    sitemap_url = request.build_absolute_uri(reverse("sitemap"))

    if settings.DEBUG:
        lines = [
            "User-agent: *",
            "Disallow: /",
            f"Sitemap: {sitemap_url}",
        ]
    else:
        lines = [
            "User-agent: *",
            "Allow: /",
            "Allow: /dashboard/onboarding/",
            "Allow: /dashboard/ui-showcase/",
            "Disallow: /admin/",
            "Disallow: /api/",
            "Disallow: /login/",
            "Disallow: /register/",
            "Disallow: /logout/",
            "Disallow: /password-reset/",
            "Disallow: /school/",
            "Disallow: /thank-you/",
            "Disallow: /dashboard/",
            f"Sitemap: {sitemap_url}",
        ]

    return HttpResponse("\n".join(lines), content_type="text/plain; charset=utf-8")
