from django.db import models
from django.utils import timezone

class Blob(models.Model):
    
    SHA = models.CharField(max_length = 40,primary_key = True)
    content = models.FileField(upload_to = 'Blob')

class Tree(models.Model):
    SHA = models.CharField(max_length = 40,primary_key = True)
    name = models.CharField(max_length = 256)
    time = models.DateTimeField(auto_now_add=True)
    # 如果为空表示目录，否则表示在Blob中含有其文件
    blob = models.ForeignKey('Blob',on_delete=models.CASCADE,null = True)

# 该项是Tree对象之间的关系
class TreeGraph(models.Model):
    parent = models.ForeignKey('Tree',related_name = 'parent_tree',on_delete = models.CASCADE)
    child = models.ForeignKey('Tree',related_name = 'child_tree',on_delete = models.CASCADE)
    
class Commit(models.Model):
    id = models.AutoField(primary_key = True)
    root = models.ForeignKey("Tree", on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now = True)
    author = models.CharField(max_length = 256)
    state = models.CharField(max_length = 256)
    parent = models.ForeignKey('self',on_delete = models.CASCADE,blank=True,null = True)
    child_num = models.IntegerField(default = 0)
    
class Branch(models.Model):
    id =models.AutoField(primary_key = True)
    name  = models.CharField(max_length= 256)
    commit  = models.ForeignKey('Commit',on_delete = models.CASCADE,null = True)
    store = models.ForeignKey('Store',on_delete = models.CASCADE)
    class Meta:
        constraints=[
            models.UniqueConstraint(fields=['name', 'store'], name='unique name of each store')
        ]
    
class Store(models.Model):
    id = models.AutoField(primary_key = True)
    # work_path = models.CharField(max_length = 256)
    name = models.CharField(max_length = 256)
    time = models.DateTimeField(auto_now_add=True)
    work_branch = models.ForeignKey('Branch',related_name = 'work_branch',on_delete = models.SET_NULL,null = True)