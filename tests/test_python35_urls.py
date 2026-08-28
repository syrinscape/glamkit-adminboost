from unittest import TestCase

import python35_test_setup

from django.conf.urls import url
from django.contrib import admin

from adminboost import raw_id_admin, urls


class Python35UrlTests(TestCase):
    def test_inline_urls_are_materialised_for_django(self):
        pattern = url(r"^example/$", lambda request: None)
        had_inline_urls = hasattr(admin.site, "_inline_urls")
        original_inline_urls = getattr(admin.site, "_inline_urls", None)
        try:
            admin.site._inline_urls = {"example": pattern}

            raw_id_admin.reload(urls)

            self.assertIsInstance(urls.urlpatterns, list)
            self.assertEqual([pattern], urls.urlpatterns)
        finally:
            if had_inline_urls:
                admin.site._inline_urls = original_inline_urls
            else:
                del admin.site._inline_urls
            raw_id_admin.reload(urls)
