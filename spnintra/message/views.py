from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

#メッセージメイン ※ログインしていないと見れないページ
class MessageIndexView(LoginRequiredMixin, TemplateView):
    template_name = "message.html"