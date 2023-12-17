from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import datetime
from django.core.exceptions import ValidationError

from .models import User_info


class CustomModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, User_info):
        return User_info.user_name

class RegForm(forms.Form):
    #初回受付日時
    f_day = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))
    f_time = forms.TimeField(widget=forms.TextInput(attrs={'type': 'time'}))
    #終了日時   
    e_day = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))
    e_time = forms.TimeField(widget=forms.TextInput(attrs={'type': 'time'}))

    #対応合計時間
    total_time = forms.IntegerField()
    #対応者ID
    name_id = CustomModelChoiceField(queryset=User_info.objects.all())
    #name_id = forms.TypedChoiceField(choices=name, coerce=int, label='選択肢', validators=[MinValueValidator(0), MaxValueValidator(255)])

    #会社名
    company_name = forms.CharField(initial='不明',widget=forms.TextInput(attrs={'class': 'custom-input'})) 
    #問い合わせ内容
    q_contents = forms.CharField(widget=forms.Textarea(attrs={'style': 'width:400px; height:300px;'}),required=False)
    #回答内容
    a_contents = forms.CharField(widget=forms.Textarea(attrs={'style': 'width:400px; height:300px;'}),required=False)

    #未解決
    unsolved = forms.BooleanField(required=False, initial=False, label='My Checkbox')

    def clean_unsolved(self):
         val = self.cleaned_data['unsolved']

         if val == True:
              return -1
         else:
              return 0


    class Meta:
            model = User_info
            fields = ('user_id', 'user_name')


class Index(forms.Form):

    #管理番号
    control_id = forms.IntegerField(required=False)
     
    #初回受付日時
    f_day = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}),required=False)
    #終了日時   
    e_day = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}),required=False)

    name_id = CustomModelChoiceField(queryset=User_info.objects.all(),required=False)

    #会社名
    company_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'custom-input', 'style': 'width:300px;'}),required=False) 

    #内容検索
    qa_contents = forms.CharField(widget=forms.TextInput(attrs={'class': 'custom-input', 'style': 'width:500px;'}),required=False)

    order = [(1,"昇順"), (2,"降順")]
    order_of_display = forms.ChoiceField(widget=forms.RadioSelect, choices= order, initial = 1)

