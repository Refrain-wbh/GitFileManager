from django import forms
 
'''
上传表单
'''
'''
class UploadForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()
'''
class UploadForm(forms.Form):
    store_id = forms.IntegerField(label = 'store_id')
    path  = forms.CharField(label = 'path',max_length = 256)
    file = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'multiple': True}),  # 支持多文件上传
        label='选择文件...',
        help_text='最大100M',
        required = False 
    )

class CreateStoreForm(forms.Form):
    work_path = forms.CharField(label='work_path',max_length=256)
    store_name = forms.CharField(label='store_name',max_length=40)

class CreateBranchForm(forms.Form):
    branch_name = forms.CharField(label = 'branch_name',max_length = 40)
    commit_id = forms.IntegerField(label = 'commit_id')
    store_id = forms.IntegerField(label = 'store_id')