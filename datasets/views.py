import os
from urllib.parse import urlencode

from django.contrib.auth.views import LoginView, TemplateView, FormView
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from datasets.forms import UserLoginForm, CreateSchemaForm, ColumnSchemaForm
from datasets.models import SchemaModel
from datasets.service import write_csv


class UserLoginView(LoginView):
    form_class = UserLoginForm
    template_name = 'login.html'

    def get_context_data(self, **kwargs):
        context = super(UserLoginView, self).get_context_data()
        context['title'] = 'Login'
        return context


def data_schemas(request):
    Schemas = SchemaModel.objects.all()
    context = {
        'schemas': Schemas
    }
    return render(request, 'data_schemas.html', context=context)


class NewSchemaView(TemplateView):
    template_name = 'new_schema.html'

    def get_context_data(self, **kwargs):
        context = super(NewSchemaView, self).get_context_data()
        context['title'] = 'New Schema1'
        context['create_schema_form'] = CreateSchemaForm
        context['column_schema_form'] = ColumnSchemaForm
        return context

    def post(self, request, *args, **kwargs):
        somestring = []
        name = request.POST.get('name')
        delimiter = request.POST.get('delimiter')
        quotechar = request.POST.get('quotechar')
        column_name = request.POST.getlist('column_name')
        column_type = request.POST.getlist('column_type')
        from_value = request.POST.getlist('from_value')
        to_value = request.POST.getlist('to_value')
        order = request.POST.getlist('order')

        print(len(order))
        for i in range(len(order)):
            somestring.append((int(order[i]), column_name[i], column_type[i], from_value[i], to_value[i]))
            print(somestring)
        sorted_list = sorted(somestring, key=lambda x: x[0])
        list_to_query = []
        for tpl in sorted_list:
            str_val = f'{tpl[0]}, {tpl[1]}, {tpl[2]}, {tpl[3]}, {tpl[4]}'
            list_to_query.append(str_val)
        querystring_for_metadata = urlencode({
            'name': name,
            'delimiter': delimiter,
            'quotechar': quotechar,
        })
        query_string = '&'.join([f"{k}={v}" for k, v in enumerate(list_to_query)]) + '&' + querystring_for_metadata
        print(query_string)
        return redirect(reverse('datasets:datasets') + f"?{query_string}")


class DatasetView(TemplateView):
    template_name = 'datasets.html'

    def get_context_data(self, **kwargs):
        context = super(DatasetView, self).get_context_data()
        context['title'] = 'Datasets'
        context['schema'] = self.get_schema_data()
        context['name'] = self.request.GET.get('name')
        context['delimiter'] = self.request.GET.get('delimiter')
        context['quotechar'] = self.request.GET.get('quotechar')
        return context

    def get_schema_data(self):
        schema = []
        for k, v in self.request.GET.items():
            if k not in ['name', 'delimiter', 'quotechar']:
                schema.append(tuple(v.split(',')))
        return schema

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        rows = request.POST.get('rows_number')
        write_csv(context['schema'], rows, context['name'], context['delimiter'], context['quotechar'])
        file_src = os.path.join('media/csv/', context['name']) + '.csv'
        file = SchemaModel(
            title=context['name'],
            separator=context['delimiter'],
            quotechar=context['quotechar'],
            src=file_src,
            author=request.user)
        file.save()
        context['files'] = SchemaModel.objects.all()
        return render(request, 'datasets.html', context=context)

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        context['files'] = SchemaModel.objects.all()
        return render(request, 'datasets.html', context=context)


def delete_schema(request, schema_id):
    schema = SchemaModel.objects.filter(id=schema_id)
    schema.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])
