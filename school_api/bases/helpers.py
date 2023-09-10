from django.utils import text
from safedelete.queryset import SafeDeleteQueryset


def create_slug(name, model):
    slug = clean_slug = text.slugify(name)
    exists = True
    i = 0
    while exists:
        if i > 0:
            slug = clean_slug + "-" + str(i)
        queryset = model.objects.filter(slug=slug)
        if isinstance(queryset, SafeDeleteQueryset):
            queryset = queryset.all(force_visibility=True)
        exists = queryset.exists()
        i += 1

    return slug
