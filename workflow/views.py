from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

#ワークフローメイン ※ログインしていないと見れないページ
class WorkflowIndexView(LoginRequiredMixin, TemplateView):
    template_name = "workflow.html"