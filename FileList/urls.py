from django.contrib import admin
from django.urls import path, include
# from . import views
from . import newviews as views
app_name = 'FileList'
 
urlpatterns = [
    path('storelist/',views.storelist,name = 'storelist'),
    path('deleteStore/',views.deleteStore,name  = 'deleteStore'),
    path('addStore/',views.addStore,name = 'addStore'),
    path('storeContent/',views.storeContent,name = 'storeContent'),
    path('upload/', views.upload, name='upload'),  # 删除
    path('getToken/',views.getToken,name='getToken'),
    path('getFileList/',views.getFileList,name = 'getFileList'),
    path('mkDir/',views.mkDir,name = 'mkDir'),
    path('download/', views.download, name='download'),  # 下载
    path('commit/', views.create_commit, name='create_commit'),  # 下载
    path('branchHistory/',views.getBranchHistory),
    path('deleteFileDir/',views.deleteFileDir),
    path('getBranchList/',views.getBranchList),
    path('changeWorkBranch/',views.changeWorkBranch),
    path('NewBranch/',views.NewBranch),
    path('resetBranch/',views.reset_branch)
] 
'''
urlpatterns = [
    path('',views.storelist,name = 'storelist'),
    path('store/<int:store_id>/<path:path>', views.storecontent, name='storecontent'),  # 仓库的主页
    path('store/<int:store_id>/', views.storemain, name='storemain'),  # 仓库的主页
    path('create_store/', views.create_store, name='create_store'),  # 创建仓库
    path('create_commit/<int:store_id>', views.create_commit, name='create_commit'),  # 仓库的主页
    path('branch_history/<int:store_id>', views.branch_history, name='branch_history'),  # 仓库的主页
    path('create_branch/', views.create_branch, name='create_branch'),  # 仓库的主页
    path('checkout_branch/<int:store_id>/<int:branch_id>/', views.checkout_branch, name='checkout_branch'),  # 仓库的主页
    path('create_dir/<int:store_id>/<path:path>', views.create_dir, name='create_dir'),  # 仓库的主页
    path('create_dir/<int:store_id>/', views.create_dir,kwargs={'path':'.'}, name='create_dir'),  # 仓库的主页
    
    
    
    
    path('test/<path:path>', views.test,name = 'test'),  # 列表
    path('download/<int:store_id>/<path:path>', views.download, name='download'),  # 下载
    path('delete/<int:store_id>/<path:path>', views.delete, name='delete'),  # 删除
    path('upload/', views.upload, name='upload'),  # 删除
]
'''