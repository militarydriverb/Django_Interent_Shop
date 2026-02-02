
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from blog.models import Blog


class BlogListView(ListView):
    model = Blog

    def get_queryset(self):
        return Blog.objects.filter(is_published=True)


class BlogDetailView(DetailView):
    model = Blog

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.views_count += 1
        obj.save()
        return obj


class BlogCreateView(PermissionRequiredMixin, CreateView):
    model = Blog
    fields = ['title', 'content', 'preview', 'is_published']
    success_url = reverse_lazy('blog:blog_list')
    permission_required = 'blog.add_blog'


class BlogUpdateView(PermissionRequiredMixin, UpdateView):
    model = Blog
    fields = ['title', 'content', 'preview', 'is_published']
    success_url = reverse_lazy('blog:blog_list')
    permission_required = 'blog.change_blog'

    def get_success_url(self):
        return reverse('blog:blog_detail', args=[self.kwargs.get('pk')])


class BlogDeleteView(PermissionRequiredMixin, DeleteView):
    model = Blog
    success_url = reverse_lazy('blog:blog_list')
    permission_required = 'blog.delete_blog'
