from django.conf import settings


if not settings.configured:
    settings.configure(
        DATABASES={
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
                "NAME": ":memory:",
            },
        },
        INSTALLED_APPS=(
            "django.contrib.auth",
            "django.contrib.contenttypes",
            "django.contrib.admin",
            "adminboost",
        ),
        MIDDLEWARE_CLASSES=(),
        ROOT_URLCONF=__name__,
        SECRET_KEY="python35-tests",
        STATIC_URL="/static/",
        TEMPLATE_DIRS=(),
    )

import django


django.setup()

from django.db import models


urlpatterns = []


class Related(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        app_label = "adminboost_tests"

    def __str__(self):
        return self.name


class Parent(models.Model):
    related_many = models.ManyToManyField(Related)

    class Meta:
        app_label = "adminboost_tests"


class Child(models.Model):
    parent = models.ForeignKey(Parent)
    related = models.ForeignKey(Related)

    class Meta:
        app_label = "adminboost_tests"
