from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.functional import cached_property

#=====================================================================================
# スケジュール管理画面 ※ログインしていないと見れないページ
#=====================================================================================
class SysSettingScheduleView(LoginRequiredMixin, TemplateView):
    template_name = "syssetting_schedule.html"

