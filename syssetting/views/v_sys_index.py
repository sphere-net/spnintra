from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

#システム設定メイン ※ログインしていないと見れないページ
class SysSettingIndexView(LoginRequiredMixin, TemplateView):
    template_name = "syssetting.html"