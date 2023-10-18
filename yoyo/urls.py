from django.urls import path
from . import views

urlpatterns=[
    path('', views.front_page, name='front_page'),
    path('signup', views.signup, name='signup'),
    path('signin', views.signin, name='signin'),
    path('logout', views.logout_user, name='logout_user'),
    path('upload', views.upload, name='upload'),
    path('home', views.index, name='index'),
    path('delete/<int:id>', views.delete_post, name='delete_post'),
    path('comment/<int:id>', views.do_comment, name='comment'),
    path('comment/del_cmnt/<int:id>', views.delete_comment, name='del_cmnt'),
    path('add_comment/<int:id>', views.add_comment, name='add_commment'),
    path('create_profile', views.create_profile, name='create_profile'),
    path('edit_profile', views.edit_profile, name='edit_profile'),
    path('like_post/<int:id>', views.like_post, name='like_post'),
    path('see_who_liked/<int:id>', views.see_who_liked, name='see_who_liked'),
    path('del_like/<int:id>', views.del_like, name='del_like'),
    path('est_connection/<int:id>', views.est_connection, name='est_connection'),
    path('list_connection', views.list_connection, name='list_connection'),
    path('del_connection/<int:id>', views.del_connection, name='del_connection'),
    path('my_connected_list', views.my_connected_list, name='my_connected_list'),

    # path('', views.index, name='index'),
]