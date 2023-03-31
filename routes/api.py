from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from app.contents.sitemaps import ArticleSitemap

sitemaps = {"articles": ArticleSitemap}

schema_view = get_schema_view(
    openapi.Info(
        title="Blog ThiagoDomingos API",
        default_version="v1",
        description="ThiagoDomingos@",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@thiagodomingos.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path("", include("app.accounts.urls")),
    path("", include("app.contents.urls")),
    path("", include("app.comments.urls")),
    path("docs/", schema_view.with_ui("swagger"), name="schema-swagger-ui"),
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ),
]

if settings.DEBUG:  # Dev only
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
