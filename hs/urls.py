from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns('',

                       # /hs/
                       url(r'^$', views.index, name='index'),
                       # /hs/rank/
                       url(r'^rank/$', views.rank, name='rank'),
                       # /hs/contestant/5
                       url(r'^contestant/(?P<contestant_id>\d+)/$', views.contestant_detail, name='contestant_detail'),
                       # /hs/challenge/5
                       url(r'^challenge/(?P<challenge_id>\d+)/$', views.challenge_detail, name='challenge_detail'),
                       # /hs/new_attack/
                       url(r'^new_attack/$', views.new_attack, name='new_attack'),

                       # /hs/login etc
                       # url(r'^', include('django.contrib.auth.urls')),
                       # /hs/login
                       url(r'^login/$', 'django.contrib.auth.views.login',
                           {'template_name': 'hs/auth/login.html'}, name='login'),
                       # /hs/logout
                       url(r'^logout/$', 'django.contrib.auth.views.logout',
                           {'template_name': 'hs/auth/logged_out.html'}, name='logout'),
                       # /hs/change_password
                       url(r'^change_password/$', 'django.contrib.auth.views.password_change',
                           {'template_name': 'hs/auth/change_password.html',
                            'post_change_redirect': 'hs:password_change_done'}, name='password_change'),
                       # /hs/change_password/done
                       url(r'^change_password/done/$', 'django.contrib.auth.views.password_change_done',
                           {'template_name': 'hs/auth/change_password_done.html'}, name='password_change_done'),

                       # /hs/403/
                       url(r'^403/', views.error_not_hs_member, name='error_not_hs_member'),

                       # Personal Index
                       # /hs/my/
                       url(r'^my/$', views.contestant_my_index, name='contestant_my_index'),
                       # /hs/my/set_result
                       url(r'^my/set_result/$', views.attacker_set_challenge_result,
                           name='attacker_set_challenge_result'),

                       # url(),
                       )
