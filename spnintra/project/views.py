from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

#プロジェクト管理メイン ※ログインしていないと見れないページ
class ProjectIndexView(LoginRequiredMixin, TemplateView):
    template_name = "project.html"