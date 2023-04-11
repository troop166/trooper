from django.urls import reverse
from django.utils.html import format_html, format_html_join


def image_preview(image_url):
    """Allow for an image to be displayed in the admin page"""
    return format_html('<img src="{}" width="50%" height="auto" />', image_url)


def change_list(objs):
    urls = format_html_join(
        "\n",
        "<li><a href={}>{}</a></li>",
        (
            (
                reverse(
                    f"admin:{obj._meta.app_label}_{obj._meta.model_name}_change",
                    args=(obj.pk,),
                ),
                str(obj),
            )
            for obj in objs
        ),
    )
    return format_html(
        "\n<ul{}>\n{}\n</ul>\n", " style=margin-left:0;padding-left:0;", urls
    )
