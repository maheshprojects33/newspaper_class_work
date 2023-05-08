from django.shortcuts import render, redirect
from django.views.generic import ListView, TemplateView, View, DetailView

from django.http import JsonResponse

from .models import *
from newspaper.forms import *


from datetime import timedelta
from django.utils import timezone
from django.contrib import messages


# Create your views here.

class Home(ListView):
    model = Post
    template_name = 'aznews/home/home.html'
    queryset = Post.objects.filter(
        status__isnull=False).order_by('-published_at')
    context_object_name = 'posts'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["trending_posts"] = Post.objects.filter(
            status='active', published_at__isnull=False).order_by('-published_at', '-views_count')

        context["trending_post"] = Post.objects.filter(
            status='active', published_at__isnull=False).order_by('-views_count').first()

        context["featured_posts"] = Post.objects.filter(
            status='active', published_at__isnull=False).order_by('-views_count')[2:5]

        one_week_ago = timezone.now() - timedelta(days=7)
        context['weekly_top_posts'] = Post.objects.filter(
            status='active', published_at__isnull=False, published_at__gte=one_week_ago).order_by("-published_at")[:7]

        context['recent_posts'] = Post.objects.filter(
            status='active', published_at__isnull=False, published_at__gte=one_week_ago).order_by("-published_at")[1:6]

        return context


class AboutView(TemplateView):
    template_name = "aznews/about.html"


class ContactView(View):
    template_name = "aznews/contact.html"

    def get(self, request, *args, **kwargs):

        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Query Received will contact you soon")
            return render(request, self.template_name)
        else:
            messages.error(request, "Something went wrong")
            return render(request, self.template_name, {"form": form})

class PostListView(ListView):
    model = Post
    template_name = 'aznews/list/list.html'
    context_object_name = 'posts'
    queryset = Post.objects.filter(status="active", published_at__isnull=False).order_by("-published_at")
    paginate_by = 2

class PostByCategoryView(ListView):
    model = Post
    template_name = "aznews/list/list.html"
    context_object_name = 'posts'
    paginate_by = 2

    def get_queryset(self):
        query = super().get_queryset()
        query = query.filter(
            status="active",
            published_at__isnull=False,
            category=self.kwargs["cat_id"]
        ).order_by("-published_at")
        return query

class PostDetailView(DetailView):
    model = Post
    template_name = 'aznews/detail/detail.html'
    context_object_name = 'posts'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        obj = self.get_object()
        obj.views_count += 1
        obj.save()

        context["previous_post"] = {
            Post.objects.filter(
            status = 'active', published_at__isnull = False, id__lt=obj.id
            )
            .order_by("-id")
            .first()
        }
        context["next_post"] = {
            Post.objects.filter(status='active',
                                published_at__isnull=False,
                                id__lt=obj.id)
                                .order_by("id")
                                .first()
        }
        return context



class NewsletterView(View):
    def post(self, request, *args, **kwargs):
        is_ajax = request.headers.get("x-requested-with")
        if is_ajax == "XMLHttpRequest":
            form = NewsletterForm(request.POST)
            if form.is_valid():
                form.save()
                return JsonResponse(
                    {
                        "success": True,
                        "message": "Successfully submitted to our newsletter."
                    },
                    status=201,
                )
            else:
                return JsonResponse(
                    {
                        "success": False,
                        "message": "Email is not valid"
                    },
                    status=400
                )
        else:
            return JsonResponse(
                {
                    "success": False,
                    "message": "Cannot process. Must be an AJAX request"
                },
                status=400
            )
        

class CommentView(View):
    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        post_id = request.POST['post']
        if form.is_valid():
            form.save()
            return redirect("post-detail", post_id)
        else:
            post = Post.objects.get(pk=post_id)
            return render(self.template_name, {"post":post, "form":form})
        
from django.db.models import Q
class PostSearchView(View):
    
    template_name = 'aznews/detail/detail.html'

    def get(self, request, *args, **kwargs):
        query = request.GET.get("query")
        post_list = Post.objects.filter(
            (Q(status='active') & Q(published_at__isnull=False))
            & (Q(title_icontains=query) | Q(content_icontains=query)),
            )
        page = request.GET.get("page", 1)
        paginator = paginator(post_list, 1)
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)

        return render(self.request, "detail.html")