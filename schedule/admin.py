from django.contrib import admin

from .models import TrnScheduleNormal			#スケジュール(通常)
from .models import TrnScheduleContinue			#スケジュール(継続)
from .models import TrnScheduleSpan				#スケジュール(期間)
from .models import TrnScheduleRepeat			#スケジュール(リピート)
from .models import TrnScheduleMmember			#スケジュール参加者
from .models import TrnScheduleFile				#スケジュールファイル
from .models import MstScheduleType				#予定メニュー登録マスタ
from .models import MstScheduleTypeColor		#予定色マスタ
from .models import MstInstitutionGroup			#施設グループ登録マスタ
from .models import MstInstitution				#施設登録マスタ
from .models import MstCompany					#会社登録マスタ
from .models import MstHoliday					#祝日登録マスタ

admin.site.register(TrnScheduleNormal)
admin.site.register(TrnScheduleContinue)
admin.site.register(TrnScheduleSpan)
admin.site.register(TrnScheduleRepeat)
admin.site.register(TrnScheduleMmember)
admin.site.register(TrnScheduleFile)
admin.site.register(MstScheduleType)
admin.site.register(MstScheduleTypeColor)
admin.site.register(MstInstitutionGroup)
admin.site.register(MstInstitution)
admin.site.register(MstCompany)
admin.site.register(MstHoliday)