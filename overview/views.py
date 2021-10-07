from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

#オーバービューメイン ※ログインしていないと見れないページ
class OverviewIndexView(LoginRequiredMixin, TemplateView):
    template_name = "overview.html"