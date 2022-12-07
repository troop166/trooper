from django.utils.html import format_html


def image_preview(image_url):
    """Allow for an image to be displayed in the admin page"""
    return format_html('<img src="{}" width="100%" height="auto" />', image_url)
