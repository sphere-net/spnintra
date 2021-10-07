from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

#報告書メイン ※ログインしていないと見れないページ
class ReportIndexView(LoginRequiredMixin, TemplateView):
    template_name = "report.html"