from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.functional import cached_property
# モデルインポート
from overview.models import *
from schedule.models import *
# 標準インポート
from django.db.models import F
import datetime
import time
# オリジナルライブラリインポート
from commonutil.libraries import *
#この下はお試し用
from django.db import connection

#=====================================================================================
# 個人週画面 ※ログインしていないと見れないページ
#=====================================================================================
class SchedulePweekView(LoginRequiredMixin, TemplateView):
    template_name = "pweek.html"

