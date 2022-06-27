from .models import Blob,Tree,TreeGraph,Commit
import os
from django.core.files import File
import hashlib
import shutil
def GenBlob(file):

    sha1 = hashlib.sha1()

    for data in file.chunks():
        sha1.update(data)
    sha1 = sha1.hexdigest()

    blobs =Blob.objects.filter(SHA = sha1) 
    if not blobs.exists():
        path = 'Blob/'+sha1
        with open(path,'wb') as fp:
            for data in file.chunks():
                fp.write(data)
        blob = Blob(sha1,path)
        blob.save()
    else :
        blob = blobs[0]
    return blob
    
# 递归生成完整的commit，包括插入Tree表，TreeGraph表
def GenTree(path):
    print(path)
    sub_objlist = []
    sub_blob = None
    
    # 首先获取子级对象，可能是Blob也可能是Tree
    if os.path.isfile(path):
        with open(path,'rb') as f:
            sub_blob = GenBlob(File(f))
            sub_objlist.append(sub_blob)     
    elif os.path.isdir(path):
        for sub in os.listdir(path):
            subpath = os.path.join(path,sub)
            sub_objlist.append(GenTree(subpath))
    
    # 计算当前对象的SHA
    sha1 = hashlib.sha1()
    sha1.update(os.path.basename(path).encode('utf8'))
    for subobj in sub_objlist:
        sha1.update(subobj.SHA.encode('utf8'))
    sha1 = sha1.hexdigest()
    
    # 生成当前对象，并保存
    trees = Tree.objects.filter(SHA = sha1)
    if not trees.exists():
        tree = Tree(SHA = sha1,
                    name = os.path.basename(path),
                    blob = sub_blob)
        tree.save()
    else :
        tree = trees[0]
    
    #如果当前是目录的话，要生成TreeGraph
    if os.path.isdir(path):
        print(path)
        print(sub_objlist)
        for subtree in sub_objlist:
            if not TreeGraph.objects.filter(parent = tree,child = subtree).exists():
                relate = TreeGraph(parent = tree,child = subtree)
                relate.save()
    # 返回当前对象
    return tree



def GenCommit(path,parent):
    root = GenTree(path)
    if parent is not None:
        parent.child_num = parent.child_num +1
        parent.save()
    commit = Commit(root = root,author = 'wbh',state='test',parent = parent)
    commit.save()
    return commit
    

def ChangeTree(root_tree,root_path):
    relates = TreeGraph.objects.filter(parent = root_tree)
    childs = [relate.child for relate in relates]
    
    for child in childs:
        path = os.path.join(root_path,child.name)
        if child.blob == None:#means it is a dir
            os.makedirs(path)
            ChangeTree(child,path)     
        else:
            file = child.blob.content
            with open(path,'wb') as fp:
                for data in file.chunks():
                    fp.write(data)
        os.utime(path,(child.time.timestamp(),child.time.timestamp()))
            
def ChangeToCommit(commit,root_path):
    
    root = commit.root
    if os.path.exists(root_path):
        shutil.rmtree(root_path)
    os.makedirs(root_path)
    ChangeTree(root,root_path)