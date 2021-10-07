from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.functional import cached_property

#=====================================================================================
# グループ日画面 ※ログインしていないと見れないページ
#=====================================================================================
class ScheduleGdayView(LoginRequiredMixin, TemplateView):
    template_name = "gday.html"

