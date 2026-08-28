from unittest import TestCase, mock

import python35_test_setup as test_setup
from python35_test_setup import Child, Parent

from django.conf.urls import include, patterns, url
from django.contrib import admin
from django.core.urlresolvers import Resolver404, clear_url_caches, resolve

from adminboost import raw_id_admin, urls


class Python35AdminReloadTests(TestCase):
    def test_inline_registration_refreshes_resolver_cache(self):
        class Inline(raw_id_admin.ImprovedRawIdStackedMixin, admin.StackedInline):
            model = Child
            raw_id_fields = ("related",)

        had_inline_urls = hasattr(admin.site, "_inline_urls")
        original_inline_urls = getattr(admin.site, "_inline_urls", None)
        original_urlpatterns = test_setup.urlpatterns
        try:
            admin.site._inline_urls = {}
            raw_id_admin.reload(urls)
            test_setup.urlpatterns = patterns(
                "",
                url(r"^inline/", include(urls)),
            )
            clear_url_caches()

            with self.assertRaises(Resolver404):
                resolve("/inline/edit-links/related/")

            with mock.patch.object(
                raw_id_admin,
                "clear_url_caches",
                wraps=raw_id_admin.clear_url_caches,
            ) as clear_url_caches_mock:
                Inline(Parent, admin.site)

            clear_url_caches_mock.assert_called_once_with()
            match = resolve("/inline/edit-links/related/")
            self.assertEqual("inline_child_render_edit_links", match.url_name)
        finally:
            if had_inline_urls:
                admin.site._inline_urls = original_inline_urls
            else:
                del admin.site._inline_urls
            raw_id_admin.reload(urls)
            test_setup.urlpatterns = original_urlpatterns
            clear_url_caches()
