from django import template

register = template.Library()


@register.filter(name="add_css")
def add_css(field, css):
    """Adds a CSS class to the tag."""
    return field.as_widget(attrs={"class": css})


