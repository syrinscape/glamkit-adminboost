from decimal import Decimal
from unittest import TestCase, mock

from python35_test_setup import Parent, Related

from django.contrib import admin


class Python35TextTests(TestCase):
    def test_preview_widget_renders_text_from_bytes(self):
        from adminboost import preview

        class File(object):
            name = b"caf\xc3\xa9.jpg"

        class Image(object):
            file = File()

        class Thumbnail(object):
            url = "/thumb/caf%C3%A9.jpg"

        class Form(object):
            preview_instance_required = False

            def get_images(self, instance):
                return [Image()]

            def get_preview_help_text(self, instance):
                return "Price: %s" % Decimal("12.99")

        widget = preview.ImagePreviewWidget(form=Form())
        with mock.patch.object(preview, "Thumbnailer", File), mock.patch.object(
            preview,
            "get_thumbnailer",
        ) as get_thumbnailer, mock.patch.object(
            preview.default_storage,
            "url",
            return_value="/media/caf%C3%A9.jpg",
        ) as storage_url:
            get_thumbnailer.return_value.get_thumbnail.return_value = Thumbnail()

            output = widget.render("preview", None)

        storage_url.assert_called_once_with("caf\xe9.jpg")
        self.assertIsInstance(output, str)
        self.assertIn("/media/caf%C3%A9.jpg", output)
        self.assertIn("Price: 12.99", output)

    def test_raw_id_widget_renders_related_object_text(self):
        from adminboost import widgets

        db_field = Parent._meta.get_field("related_many")
        widget = widgets.VerboseManyToManyRawIdWidget(db_field, admin.site)
        related = Related(pk=7, name="Cr\xe8me")
        manager = mock.Mock()
        manager.using.return_value.get.return_value = related
        with mock.patch.object(
            widget.rel.to,
            "_default_manager",
            manager,
        ), mock.patch.object(
            widgets,
            "render_edit_link",
            side_effect=lambda obj, field: str(obj),
        ), mock.patch.object(
            widgets,
            "render_edit_links",
            side_effect=lambda model, links, field: "|".join(links),
        ):
            output = widget.label_for_value("7,, 8")

        self.assertEqual("Cr\xe8me|Cr\xe8me", output)
        self.assertEqual(2, manager.using.return_value.get.call_count)
