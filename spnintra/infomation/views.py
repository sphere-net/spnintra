import logging

from django.contrib import messages
from django.urls import reverse_lazy
from django.views import generic
from .forms import InquiryForm

logger = logging.getLogger(__name__)

class IndexView(generic.TemplateView):
    template_name = "infomation.html"

class InquiryView(generic.FormView):
    template_name = "inquiry.html"
    form_class = InquiryForm
    success_url = reverse_lazy('infomation:infomation_inquiry')

    #親クラスで定義されているメソッドをオーバーライド
    #フォームバリデーションに問題がなかったら実行される
    def form_valid(self, form):
        form.send_email()
        messages.success(self.request, 'メッセージを送信しました。')
        logger.info('Inquiry sent by {}'.format(form.cleaned_data['name']))
        return super().form_valid(form)
