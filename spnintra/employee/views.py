from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

#社員評価メイン ※ログインしていないと見れないページ
class EmployeeIndexView(LoginRequiredMixin, TemplateView):
    template_name = "employee.html"