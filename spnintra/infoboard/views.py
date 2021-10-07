from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

#掲示板メイン ※ログインしていないと見れないページ
class InfoboardIndexView(LoginRequiredMixin, TemplateView):
    template_name = "infoboard.html"