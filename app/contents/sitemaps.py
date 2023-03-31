from django.contrib.sitemaps import Sitemap
from .models import Article


class ArticleSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8
    protocol = "http"

    def items(self):
        return Article.objects.actives()

    def lastmod(self, obj):
        return obj.published_at

    def location(self, obj):
        return f"/articles/{obj.slug}/article"
