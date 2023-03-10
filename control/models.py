from django.db import models
from wagtail.models import Page, Orderable
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.snippets.models import register_snippet
from modelcluster.fields import ParentalKey

from wagtail.contrib.modeladmin.options import (
    ModelAdmin, ModelAdminGroup, modeladmin_register
)

from modelcluster.models import ClusterableModel

class GriperIndexPage(Page):

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

        context["griper_commands"] = Griper.objects.all()

        return context

class GriperCommands(Orderable):

    page = ParentalKey("control.Griper", related_name="commands")
    joint = models.CharField(
        max_length=255,
        choices=[
            ("M1", "M1"),
            ("M2", "M2"),
            ("M3", "M3"),
            ("M4", "M4"),
            ("M5", "M5"),
            ("M6", "M6"),
        ]
    )
    value_degrees = models.IntegerField()

    panels = [
        FieldPanel("joint"),
        FieldPanel("value_degrees"),
    ]

    def get_js_string(self):
        sign = "+" if self.value_degrees >= 0 else "-"
        value = abs(self.value_degrees)
        n = 3 - len(str(value))
        l = ["0"]*n
        print(f"{self.joint}_{sign}{''.join(l)}{value}")
        return f"{self.joint}_{sign}{''.join(l)}{value}"


class Griper(Page):
    content_panels = Page.content_panels + [
    MultiFieldPanel(
        [InlinePanel("commands", label="commands")],
        heading="Griper Commands",
        ),
    ]



class Home(Page):
    intro = models.CharField(max_length=255)

    content_panels = Page.content_panels + [
        FieldPanel("intro"),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["instructions"] = Instructions.objects.all()
        return context


class Instructions(Page):
    name = models.CharField(max_length=127)

    content_panels = Page.content_panels + [
        FieldPanel("name"),
        MultiFieldPanel(
            [InlinePanel("componenets_settings", label="Instruction")],
            heading="Instructions",
        ),
    ]


class ComponentSettings(Orderable):
    page = ParentalKey("control.Instructions", related_name="componenets_settings")
    componenet = models.ForeignKey(
        "control.Componenets",
        blank=True,
        on_delete=models.CASCADE,
    )

    panels = [
        FieldPanel("componenet")
    ]


@register_snippet
class Componenets(ClusterableModel):
    choices = [
        ("SERVO", "SERVO"),
        ("LED", "LED")
    ]
    name = models.CharField(max_length=255)
    choice = models.CharField(max_length=20, choices=choices)
    degrees = models.IntegerField(help_text="Only for servo", null=True, blank=True)
    status = models.BooleanField(default=False, help_text="only for LED")

    panels = [
        FieldPanel("name"),
        FieldPanel("choice"),
        FieldPanel("degrees"),
        FieldPanel("status"),
    ]

    def __str__(self, *args, **kwargs):
        return self.name

    def __repr__(self, *args, **kwargs):
        return self.name

    def get_js_string(self):
        if self.choice == "SERVO":
            return f"servo-{self.degrees}"

        elif self.choice == "LED":
            return f"led-{1 if self.status else 0}"
