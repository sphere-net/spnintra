from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

#備品管理メイン ※ログインしていないと見れないページ
class EquipmentIndexView(LoginRequiredMixin, TemplateView):
    template_name = "equipment.html"