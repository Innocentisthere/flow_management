from django.urls import path
from . import views

app_name = "flow"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("<int:pk>/edit", views.FlowUpdateView.as_view(), name="edit"),
    path('add', views.MoneyFlowCreateView.as_view(), name='add'),
    path('<int:pk>/delete', views.MoneyFlowDeleteView.as_view(), name='delete'),
    path('api/categories/', views.get_categories, name='api_categories'),
    path('api/subcategories/', views.get_subcategories, name='api_subcategories'),
    path('manage/', views.manage_references, name='manage_references'),
]
