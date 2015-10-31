from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import Http404
from django.utils.translation import get_language
from django.views.generic import TemplateView

from blog import settings as blog_settings
from blog.models import Post, Tag


class IndexView(TemplateView):
    template_name = 'blog/index.jinja2'

    def get(self, request, page_number=1, *args, **kwargs):
        posts_list = Post.objects.order_by('-created_at').filter(language_code=get_language())
        paginator = Paginator(posts_list, blog_settings.POSTS_PAGE_SIZE)

        try:
            posts = paginator.page(page_number)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)

        return self.render_to_response({
            'posts': posts
        })


class PostView(TemplateView):
    template_name = 'blog/post.jinja2'

    def get(self, request, slug=None, *args, **kwargs):
        try:
            post = Post.objects.get(post_meta=slug, language_code=get_language())
        except Post.DoesNotExist:
            # TODO: use default language instead
            raise Http404

        # TODO: optimization needed
        tags = Tag.objects.filter(language_code=get_language(), tag_meta__in=post.tags.all())
        tags = dict(tags.values_list('pk', 'title'))

        return self.render_to_response({
            'post': post,
            'tags': tags,
        })
