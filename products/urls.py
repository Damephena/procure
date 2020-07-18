from django.urls import path, re_path, include
from rest_framework.routers import SimpleRouter, DefaultRouter

import products.views as view

router = SimpleRouter()
router.register('', view.ProductReadOnlyViewSet, basename='products'),

urlpatterns = [
    path('tags/', view.TagView.as_view(), name='tag-list'),
    path('tags/<str:pk>/', view.TagDetail.as_view(), name='tag-detail'),
    path('categories/', view.CategoryView.as_view(), name='category-list'),
    path('categories/<str:pk>/', view.CategoryDetail.as_view(), name='category-detail'),
    path('status/', view.ProductStatusView.as_view(), name='status-list'),
]

urlpatterns += router.urls
