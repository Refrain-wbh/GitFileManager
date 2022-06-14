from django.shortcuts import render
from django.http import HttpResponseRedirect,HttpResponseNotAllowed, HttpResponseNotFound
from django.http import HttpResponse

from django.http import FileResponse
from django.template import RequestContext
from django.urls import reverse
import shutil
from pdb import  set_trace
# from django.utils.http import urlquote
 

import os
from django.core.files.storage import FileSystemStorage
from .GitGen import GenCommit,ChangeToCommit


from .forms import CreateStoreForm,CreateBranchForm,UploadForm
from .models import Branch,Store,Commit

UserLocal = 'User/'
location = 'D:/2022_03/GitFileManager/'
fs = FileSystemStorage(location = location,base_url = 'user')


# 上传文件

def upload(request):
    # Handle file upload
    # set_trace()
    print(request.FILES)
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            store_id = request.POST.get('store_id')
            files = request.FILES.getlist('file')
            path = request.POST.get('path')
            print(files)
            print('path:',path)
            print('store_id:',store_id)
            for f in files:
                # file_name = fs.save(f.name)
                # set_trace()
                file_dir = os.path.join(UserLocal,str(store_id),path)
                file_path = os.path.join(file_dir,f.name)
                with open(file_path,'wb+') as fp :
                    for chunk in f.chunks():
                        fp.write(chunk)
                #file_info = FileInfo(file_name=f.name, file_size=1 if 0 < f.size < 1024 else f.size / 1024, file_path=os.path.join('D:\\upload', f.name))
                #file_info.save()    
            # 返回上传页
            
            return HttpResponseRedirect(reverse('FileList:storecontent',kwargs={'store_id':store_id,'path':path}))
    else:
        form = UploadForm()  # A empty, unbound form
    #return HttpResponseRedirect(reverse('FileList:upload'))
    #return render(request, 'uploader/upload.html', {'form': form})
    return  HttpResponseNotFound('upload failed')


def storemain(request,store_id):
    return storecontent(request,store_id,'.') 
# store 内容

def storecontent(request,store_id,path):
    #set_trace()
    temp_path = os.path.join(UserLocal,str(store_id),path)
    if not os.path.exists(temp_path):
        print(temp_path,'not exist!')
        return None
    
    cont = fs.listdir(temp_path)
    cont_with_path = list(fs.listdir(temp_path))
    if path != '.':
        cont_with_path[0] = [os.path.join(path,i) for i in cont_with_path[0]]
        cont_with_path[1] = [os.path.join(path,i) for i in cont_with_path[1]]
    
    dirs = list(zip(cont[0],cont_with_path[0]))
    files = list(zip(cont[1],cont_with_path[1]))
    store = Store.objects.filter(id = store_id).first()
    
    # pdb.set_trace()
    branch_set = store.branch_set.all()
    
    return render(request, 'FileList/store_content.html',
                  {'dirs':dirs,
                   'files':files,
                   'branch_set':branch_set,
                   'work_branch':store.work_branch,
                   'store_id':store_id,
                   'path':path,
                   })

def test(request,path):
    return HttpResponse('test sucess:%s'%(path))
 
# 下载文件
def download(request,store_id, path):
    
    path = os.path.join(UserLocal,str(store_id),path)
    print('下载的文件名：'+path)
    
    response = FileResponse(open(path,'rb'),as_attachment=True)
    # response['Content-Disposition'] = 'attachment;filename="%s"' % urlquote(file_info.file_name)
    return response
 
 
# 删除文件
def delete(request,store_id, path):
    temppath = os.path.join(UserLocal,str(store_id),path)
    if os.path.isfile(temppath):
        print('删除文件：'+temppath)
        os.remove(temppath) 
    elif os.path.isdir(temppath):
        shutil.rmtree(temppath)
    ptree = os.path.split(path)[0] 
    if ptree == '':
        ptree = '.'
    return HttpResponseRedirect(
        reverse('FileList:storecontent',kwargs={'store_id':store_id,'path':ptree})
    )
def create_dir(request,store_id,path):
    # Handle file upload
    # set_trace()
    if request.method == 'POST':
        dir_name = request.POST.get('dir_name')
        subpath = os.path.join(UserLocal,str(store_id),path,dir_name)
        os.makedirs(subpath)
    return HttpResponseRedirect(
        reverse('FileList:storecontent',kwargs={'store_id':store_id,'path':path})
    )
    
# 将内容全部提交，生成commit，父commit指向branch的commit，
# branch切换到当前Commit
def create_commit(request,store_id):
    temp_path = os.path.join(UserLocal,str(store_id))
    store = Store.objects.filter(id = store_id).first()
    work_branch = store.work_branch
    
    commit = GenCommit(temp_path,work_branch.commit)
    work_branch.commit = commit
    work_branch.save()
    
    return HttpResponseRedirect(
        reverse('FileList:branch_history',kwargs={'store_id':store.id}))




def branch_history(request,store_id):
    store = Store.objects.filter(id = store_id).first()
    work_branch = store.work_branch
    # to show the history of work_branch
    pre_commit = work_branch.commit
    
    commit_list = []
    while pre_commit is not None:
        commit_list.append(pre_commit)
        pre_commit = pre_commit.parent
    branch_form = CreateBranchForm()
    return render(request, 'FileList/branch_history.html',
                  {
                    'commit_list' : commit_list,
                    'create_branch' : branch_form,
                    'store_id':store_id,
                   })


# 
def create_branch(request):
    #set_trace()
    if request.method =='POST':
        form = CreateBranchForm(request.POST)
        if form.is_valid(): 
            branch_name = request.POST.get('branch_name')
            commit = Commit.objects.filter(id = request.POST.get('commit_id')).first()
            store = Store.objects.filter(id = request.POST.get('store_id')).first()
            branch = Branch(name =  branch_name,
                            commit = commit,
                            store = store)
            branch.save()
            store = Store.objects.filter(id = request.POST.get('store_id')).first()
            
            return HttpResponseRedirect(
                reverse('FileList:checkout_branch',
                        kwargs={'store_id':store.id,'branch_id':branch.id}))
    return HttpResponse('create branch fail!')

def checkout_branch(request,store_id,branch_id):
    store  = Store.objects.filter(id=  store_id).first()
    new_branch = Branch.objects.filter(id = branch_id).first()
    store.work_branch = new_branch
    store.save()
    path = os.path.join(UserLocal,str(store_id))
    ChangeToCommit(new_branch.commit,path)
    return HttpResponseRedirect(
        reverse('FileList:storemain',kwargs={'store_id':store.id})
    )
    
def storelist(request):
    storelist = Store.objects.all()
    create_store = CreateStoreForm()
    return render(request,'FileList/storelist.html',
                  {'storelist':storelist,'create_store':create_store})

def create_store(request):
    if request.method =='POST':
        form = CreateStoreForm(request.POST)
        if form.is_valid():
            print(form) 
            store = Store(work_path = form.fields['work_path'],
                          name = form.fields['store_name'])
            store.save()
            valid_branch = Branch(name = 'main',store = store,commit = None)
            valid_branch.save()
            store.work_branch = valid_branch
            store.save()
            # 生成了一个仓库以及默认的main 分支
            
            # 为其在User中创建一个临时工作区
            temp_path = os.path.join(UserLocal,str(store.id))
            if os.path.exists(temp_path):
                shutil.rmtree(temp_path)
            os.makedirs(temp_path)
            
            return HttpResponseRedirect(
                reverse('FileList:storemain',kwargs={'store_id':store.id}))

    return HttpResponseRedirect(
        reverse('FileList:storelist'))          


def reset_branch(request,store_id,commit_id):
    store  = Store.objects.filter(id=store_id).first()
    work_branch = store.work_branch
    pre_commit = work_branch.commit
    on_delete = True
    if pre_commit.num_child == 0:
        pre_commit.delete()
    else :
        on_delete = False
    
    while pre_commit.id !=commit_id:
        par = pre_commit.parent
        if on_delete:
            if pre_commit.num_child == 0:
                pre_commit.delete()
            else :
                on_delete = False
                pre_commit.num_child = pre_commit.num_child - 1
                pre_commit.save()
        pre_commit = par
    work_branch.commit = pre_commit
    work_branch.save()
    