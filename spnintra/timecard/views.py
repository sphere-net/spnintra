from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

#タイムカードメイン ※ログインしていないと見れないページ
class TimecardIndexView(LoginRequiredMixin, TemplateView):
    template_name = "timecard.html"