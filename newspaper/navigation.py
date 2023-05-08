from .models import *


def navigation(request):
    categories = Category.objects.all()[:5]
    tags = Tag.objects.all()[:10]
    scrolling_post = Post.objects.filter(
        status='active', published_at__isnull=False).order_by('-published_at', '-views_count')[:5]

    return {"categories": categories, "tags": tags, "scrolling_post": scrolling_post}
