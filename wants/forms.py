from django.forms import ModelForm, TextInput, Textarea, CheckboxInput, SelectDateWidget, URLField
from .models import Want


class WantsCreateForm(ModelForm):
    class Meta:
        model = Want
        fields = ('status', 'content', 'target_date', 'publish_set')
        labels = {
            'status': 'ステータス',
            'content': 'Wants',
            'target_date': '目標日付',
            'publish_set': '公開設定',
        }
        widgets = {
            #'status': TextInput(attrs={'class': ''}),
            'content': TextInput(attrs={'class': ''}),
            'target_date': SelectDateWidget(attrs={'class': ''}),
            'publish_set': CheckboxInput(attrs={'class': ''}),
        }

class WantsUpdateForm(ModelForm):
    class Meta:
        model = Want
        fields = ('achieve_date', 'achieve_text', 'achieve_url')
        labels = {
            'achieve_date': '達成日',
            'achieve_text': '達成コメント',
            'achieve_url': '参照URL',
        }
        widgets = {
            'achieve_date': SelectDateWidget(attrs={'class': ''}),
            'achieve_text': Textarea(attrs={'class': ''}),
            #'achieve_url': CheckboxInput(attrs={'class': ''}),
        }

# class WantsForm(ModelForm):

#     class Meta:
#         model = Want
#         fields = ['content', 'status', 'target_date', 'publish_set']
#         labels = {
#             'content': 'Wants',
#             'status': 'ステータス',
#             'target_date': '目標日付',
#             'publish_set': '公開設定',
#         }
#         # widgets = {
#         #     'content': TextInput(attrs={'class': ''}),
#         #     'status': TextInput(attrs={'class': ''}),
#         #     'target_date': SelectDateWidget(attrs={'class': ''}),
#         #     'publish_set': CheckboxInput(attrs={'class': ''}),
#         # }



