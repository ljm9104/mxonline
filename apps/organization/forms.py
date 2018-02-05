from django import forms

from operation.models import UserAsk
import re

# 普通版本的form
# class UserAskForm(forms.Form):
#     name = forms.CharField(required=True, min_length=2, max_length=20)
#     phone = forms.CharField(required=True, max_length=11, min_length=11)
#     course_name = forms.CharField(required=True, min_length=5, max_length=50)


# 进阶版本的modelform：它可以向model一样save
class UserAskForm(forms.ModelForm):
    # 继承之余还可以新增字段
    # my_feild = forms.CharField()
    # 是由哪个model转换的
    class Meta:
        model = UserAsk
        # 需要验证的字段
        fields = ['name', 'mobile', 'course_name']

    # 手机号验证
    def clean_mobile(self):
        mobile = self.cleaned_data['mobile']
        REGEX_MOBILE = "^1[358]\d{9}$|^147\d{8}$|^176\d{8}$"
        p = re.compile(REGEX_MOBILE)
        if p.match(mobile):
            return mobile
        else:
            raise forms.ValidationError(u"手机号码非法", code="mobile_invalid")
