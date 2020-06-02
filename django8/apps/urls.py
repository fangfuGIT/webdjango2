# -*- coding: utf-8 -*-

# Author： fangfu


# from apps import views
# from apps.views import CpuInfoView
#
# urlpatterns = [
#
# ]


from django.conf.urls import url, include
from apps.views import CpuViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'', CpuViewSet)

urlpatterns = [
    url('', include(router.urls))
]