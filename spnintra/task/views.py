from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

#タスクメイン ※ログインしていないと見れないページ
class TaskIndexView(LoginRequiredMixin, TemplateView):
    template_name = "task.html"