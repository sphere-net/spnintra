from django.contrib import admin

from .models import MstAccount              #アカウント登録マスタモデル
from .models import MstAdmin                #管理者マスタモデル
from .models import MstUseFncType           #使用機能種別マスタモデル
from .models import MstGroup                #グループマスタモデル
from .models import MstBelongGroup          #グループ登録マスタモデル
from .models import MstOfficer              #役職マスタモデル
from .models import MstDepartment           #部署マスタモデル
from .models import MstBelongDepartment     #部署登録マスタモデル

admin.site.register(MstAccount)
admin.site.register(MstAdmin)
admin.site.register(MstUseFncType)
admin.site.register(MstGroup)
admin.site.register(MstBelongGroup)
admin.site.register(MstOfficer)
admin.site.register(MstDepartment)
admin.site.register(MstBelongDepartment)
