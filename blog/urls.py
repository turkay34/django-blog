from django.urls import path
from django.conf.urls import url
from blog.views import post_update, post_delete, post_create, post_list, post_detail, comment_add

urlpatterns = [
    path('', post_list, name='post-list'),
    path('post-create/', post_create, name='create'),
    url(r'post-delete/(?P<slug>[-\w]+)/$', post_delete, name='delete'),
    url(r'^update/(?P<slug>[-\w]+)/$', post_update, name='update'),
    url(r'^detail/(?P<slug>[-\w]+)/$', post_detail, name='detail'),
    url(r'^add_comment/(?P<slug>[-\w]+)/$', comment_add, name='comment_add')
]
