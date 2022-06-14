from django.shortcuts import render
from django.http import HttpResponseRedirect,HttpResponseNotAllowed, HttpResponseNotFound
from django.http import HttpResponse
import datetime
from django.http import FileResponse
from django.template import RequestContext
from django.urls import reverse
import shutil
from pdb import  set_trace
# from django.utils.http import urlquote
from django.middleware.csrf import get_token

import os
from django.core.files.storage import FileSystemStorage
from .GitGen import GenCommit,ChangeToCommit


from .forms import CreateStoreForm,CreateBranchForm,UploadForm
from .models import Branch,Store,Commit

from django.http import JsonResponse
from django.core import serializers
import json

UserLocal = 'User/'
location = 'D:/2022_03/GitFileManager/'
fs = FileSystemStorage(location = location,base_url = 'user')


def reset_branch(request):
    store_id = request.GET.get('store_id')
    commit_id = int(request.GET.get('commit_id'))
    store  = Store.objects.filter(id=store_id).first()
    work_branch = store.work_branch
    pre_commit = work_branch.commit
    
    # 首先判断需不需要reset分支
    if pre_commit.id == commit_id:
        return HttpResponse('sucess')
    
    pre_commit.child_num -= 1
    pre_commit.save()
    
    new_commit = Commit.objects.filter(id = commit_id).first()
    if new_commit :
        new_commit.child_num += 1
        pre_commit.save()
    work_branch.commit = new_commit
    work_branch.save()
    
    on_delete = True
    while pre_commit and pre_commit.id != commit_id:
        parent = pre_commit.parent
        if on_delete:
            if pre_commit.child_num <= 0:
                pre_commit.delete()
                if parent :
                    parent.child_num -= 1
                    parent.save()
            else :
                on_delete = False
        pre_commit = parent
        
    
    path = os.path.join(UserLocal,str(store_id))
    ChangeToCommit(new_commit,path)
    
    
    return HttpResponse('sucess')
    

def NewBranch(request):
    #set_trace()
    branch_name = request.GET.get('branch_name')
    store_id = request.GET.get('store_id')
    commit_id = request.GET.get('commit_id')
    commit = Commit.objects.filter(id = commit_id).first()
    
    store = Store.objects.filter(id = store_id).first()
    
    branch = Branch(name =  branch_name,
                    commit = commit,
                    store = store)
    branch.save()
    
    # 有新的分支指向commit 
    commit.child_num = commit.child_num + 1
    commit.save()
    
    store.work_branch = branch
    store.save()
    
    return HttpResponse('sucess')

def getBranchList(request):
    store_id = request.GET.get('store_id')
    store  = Store.objects.filter(id=  store_id).first()
    work_branch = store.work_branch
    branchList = Branch.objects.filter(store = store)
    
    branchList = [{'id':branch.id,'name':branch.name} for branch in branchList]
    res = {'cur_branch_id':work_branch.id,
           'branchList':branchList}
    
    return JsonResponse(res)

def changeWorkBranch(request):
    store_id = request.GET.get('store_id')
    new_branch_id = request.GET.get('new_branch_id')
    store  = Store.objects.filter(id=store_id).first()
    new_branch = Branch.objects.filter(id = new_branch_id).first()
    if new_branch is None:
        return HttpResponse('分支不存在',status = 403)
    store.work_branch = new_branch
    store.save()
    path = os.path.join(UserLocal,str(store_id))
    ChangeToCommit(new_branch.commit,path)
    
    return HttpResponse('sucess')

def deleteFileDir(request):
    store_id = request.GET.get('store_id')
    path = request.GET.get('path')
    name = request.GET.get('name')
    path = os.path.join(UserLocal,str(store_id),path)
    path = os.path.join(path,name)
    if not os.path.exists(path):
        return HttpResponse("文件或文件夹不存在",status = 403)
    
    if os.path.isfile(path):
        print('删除文件：'+path)
        os.remove(path) 
    elif os.path.isdir(path):
        shutil.rmtree(path)
    return HttpResponse('sucess')

def getBranchHistory(request):
    store_id = request.GET.get('store_id')
    store = Store.objects.filter(id = store_id).first()
    work_branch = store.work_branch
    # to show the history of work_branch
    pre_commit = work_branch.commit
    
    commitList = []
    while pre_commit is not None:
        item = {}
        item['time'] = str(datetime.datetime.fromtimestamp(int(pre_commit.time.timestamp())))
        item['state'] = pre_commit.state
        item['author'] = pre_commit.author
        item['id'] = pre_commit.id
        
        point_to_branchs = Branch.objects.filter(commit = pre_commit)
        item['branchs'] = [branch.name for branch in point_to_branchs]
        commitList.append(item)
        pre_commit = pre_commit.parent
    
    res = {'commitList':commitList}
    return JsonResponse(res)



def create_commit(request):
    print("pst",request)
    store_id = request.GET.get('store_id')
    state = request.GET.get('state')
    print("store_id",store_id)
    temp_path = os.path.join(UserLocal,str(store_id))
    
    store = Store.objects.filter(id = store_id).first()
    
    work_branch = store.work_branch
    
    commit = GenCommit(temp_path,work_branch.commit)
    commit.state = state
    commit.child_num = 1
    commit.save()
    if work_branch.commit: # 当前分支可能无提交
        work_branch.commit.child_num -= 1
        work_branch.commit.save()
    work_branch.commit = commit
    work_branch.save()
    
    return HttpResponse('sucess')

# 下载文件
def download(request):
    store_id = request.GET.get('store_id')
    path = request.GET.get('path')
    name = request.GET.get('name')
    path = os.path.join(UserLocal,str(store_id),path)
    file_path = os.path.join(path,name)
    print('下载的文件名：'+ file_path)
        
    if not os.path.exists(file_path):
        return HttpResponse("文件不存在",status = 403)
    elif not os.path.isfile(file_path):
        return HttpResponse(name+'不是文件',status = 403)
    else :
        return FileResponse(open(file_path,'rb'),as_attachment=True)


def  mkDir(request):
    store_id = request.GET.get('store_id')
    path = request.GET.get('path')
    dirname = request.GET.get('dirName')
    path = os.path.join(UserLocal,str(store_id),path)
    dir_path = os.path.join(path,dirname)
    if os.path.exists(dir_path):
        return HttpResponse("文件夹名重复",status = 403)
    os.makedirs(dir_path)
    return HttpResponse('sucess')
    

def getFileList(request):
    
    store_id = request.GET.get('store_id')
    path = request.GET.get('path')
    path = os.path.join(UserLocal,str(store_id),path)
    fileList = []
    childs = os.listdir(path)
    print(childs)
    for child in childs :
        childpath = os.path.join(path,child)
        fileinfo = os.stat(childpath)
        time = str(datetime.datetime.fromtimestamp(int(fileinfo.st_mtime)))
        item = {'name':child,'time':time}
        if os.path.isdir(os.path.join(path,child)):
            item['isdir'] = True
        else :
            item['isdir'] = False
        fileList.append(item)
    print('path',path)
    fileList.sort(key = lambda x:x['isdir'],reverse = True)
    print('fileList',fileList)  
    res = {}
    res['fileList'] = fileList
    return JsonResponse(res)


def getToken(request):
    res = {}
    res['csrf_token'] = get_token(request)
    return JsonResponse(res)

def upload(request):
    print(request)
    files = request.FILES.getlist('file')
    path = request.POST.get('path')
    store_id = request.POST.get('store_id')
    for f in files:
        file_dir = os.path.join(UserLocal,str(store_id),path)
        file_path = os.path.join(file_dir,f.name)
        with open(file_path,'wb+') as fp :
            for chunk in f.chunks():
                fp.write(chunk)
    return JsonResponse({'status':'sucess'})


def storelist(request):
    res = {}
    storelist = Store.objects.all()
    
    storemsg = []
    for store in storelist:
        time = str(datetime.datetime.fromtimestamp(int(store.time.timestamp())))
        
        storemsg.append({'id':store.id,'name':store.name,'time':time})
    res['storelist'] = storemsg
    return JsonResponse(res)



def addStore(request):
    store_name = request.GET.get('store_name')
    if Store.objects.filter(name = store_name).exists():
        return HttpResponse('store名重复',status = 403)
    store = Store(name = store_name)
    store.save()
    valid_branch = Branch(name = 'main',store = store,commit = None)
    valid_branch.save()
    store.work_branch = valid_branch
    store.save()


    temp_path = os.path.join(UserLocal,str(store.id))
    if os.path.exists(temp_path):
        shutil.rmtree(temp_path)
    os.makedirs(temp_path)
    
    return HttpResponse('sucess')

def deleteStore(request):
    store_id = request.GET.get('store_id')
    store = Store(id = store_id)
    store.delete()
    return HttpResponse('sucess')
    
    

def walkTree(path,id):
    res = []
    childs = os.listdir(path)
    dirs = []
    files = []
    for child in childs :
        if os.path.isdir(os.path.join(path,child)):
            dirs.append(child)
        else :
            files.append(child)
    
    for dir in dirs:
        print(dir,dirs)
        subpath = os.path.join(path,dir)
        
        s = {'id':id,'label':dir,'isopen':False,'path':subpath}
        id += 1
        s['children'],id = walkTree(subpath,id)
        res.append(s)
    for file in files:
        subpath = os.path.join(path,file)
        s = {'id':id,'label':file,'path':subpath}
        id +=1
        res.append(s)
        
    return res,id
def storeContent(request):
    store_id = request.GET.get('store_id')
    res = {}
    work_path = os.path.join(UserLocal,str(store_id))
    if not os.path.exists(work_path):
        print(work_path,'not exist!')
        return HttpResponse("访问页面不存在",status = 404)
    
    os.chdir(work_path)
    fileTree,_ = walkTree('.',0)
    os.chdir('../../')
    res['fileTree'] = fileTree
    return JsonResponse(res)


