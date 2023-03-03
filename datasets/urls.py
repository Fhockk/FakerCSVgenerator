from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LogoutView
from django.contrib.auth.decorators import login_required

from datasets.views import UserLoginView, data_schemas, delete_schema, NewSchemaView, DatasetView

app_name = 'datasets'

urlpatterns = [
    path('', UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('data_schemas/', login_required(data_schemas), name='data_schemas'),
    path('new_schema/', login_required(NewSchemaView.as_view()), name='new_schema'),
    path('datasets/', login_required(DatasetView.as_view()), name='datasets'),
    path('delete/<int:schema_id>/', login_required(delete_schema), name='delete'),
]
