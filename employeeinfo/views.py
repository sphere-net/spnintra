from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

#社員情報メイン ※ログインしていないと見れないページ
class EmployeeInfoIndexView(LoginRequiredMixin, TemplateView):
    template_name = "employeeinfo.html"