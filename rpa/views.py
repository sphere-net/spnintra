from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

#RPAメイン ※ログインしていないと見れないページ
class RpaIndexView(LoginRequiredMixin, TemplateView):
    template_name = "rpa.html"