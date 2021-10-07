from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

#ファイル管理メイン ※ログインしていないと見れないページ
class DirectoryIndexView(LoginRequiredMixin, TemplateView):
    template_name = "directory.html"