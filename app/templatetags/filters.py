from django import template

register = template.Library()

@register.filter
def get_category_id_by_name(categories, name):
    """Return the category ID by name."""
    category = categories.filter(name=name).first()
    return category.id if category else None