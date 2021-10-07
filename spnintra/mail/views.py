from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

#メールメイン ※ログインしていないと見れないページ
class MailIndexView(LoginRequiredMixin, TemplateView):
    template_name = "mail.html"