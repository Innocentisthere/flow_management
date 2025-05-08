from django.contrib import messages
from django.db.models.deletion import ProtectedError
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .forms import (
    CategoryForm,
    MoneyFlowFilterForm,
    MoneyFlowForm,
    StatusForm,
    SubcategoryForm,
    TypeForm,
)
from .models import Category, MoneyFlow, Status, Subcategory, Type

# Create your views here.


class IndexView(generic.ListView):
    model = MoneyFlow
    template_name = "flow/index.html"
    context_object_name = "flows_list"
    paginate_by = 20  # по желанию

    def get_queryset(self):
        queryset = MoneyFlow.objects.select_related('type', 'category', 'subcategory').all()
        self.form = MoneyFlowFilterForm(self.request.GET)

        if self.form.is_valid():
            cd = self.form.cleaned_data
            if cd['type']:
                queryset = queryset.filter(type=cd['type'])
            if cd['category']:
                queryset = queryset.filter(category=cd['category'])
            if cd['subcategory']:
                queryset = queryset.filter(subcategory=cd['subcategory'])
            if cd['date_from']:
                queryset = queryset.filter(creation_date__gte=cd['date_from'])
            if cd['date_to']:
                queryset = queryset.filter(creation_date__lte=cd['date_to'])

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = self.form
        return context


class FlowUpdateView(UpdateView):
    model = MoneyFlow
    form_class = MoneyFlowForm
    template_name = 'flow/edit.html'
    context_object_name = 'flow'
    success_url = reverse_lazy('flow:index')


class MoneyFlowCreateView(CreateView):
    model = MoneyFlow
    form_class = MoneyFlowForm
    template_name = 'flow/create.html'
    success_url = reverse_lazy('flow:index')


class MoneyFlowDeleteView(DeleteView):
    model = MoneyFlow
    template_name = 'flow/delete.html'
    success_url = reverse_lazy('flow:index')


def get_categories(request):
    type_id = request.GET.get('type')
    categories = Category.objects.filter(type_id=type_id).values('id', 'name')
    return JsonResponse(list(categories), safe=False)


def get_subcategories(request):
    category_id = request.GET.get('category')
    subcategories = Subcategory.objects.filter(category_id=category_id).values('id', 'name')
    return JsonResponse(list(subcategories), safe=False)


def manage_references(request):
    status_form = StatusForm(request.POST or None, prefix='status')
    type_form = TypeForm(request.POST or None, prefix='type')
    category_form = CategoryForm(request.POST or None, prefix='category')
    subcategory_form = SubcategoryForm(request.POST or None, prefix='subcategory')

    if request.method == 'POST':
        if 'submit_status' in request.POST:
            status_form = StatusForm(request.POST, prefix='status')
            type_form = TypeForm(prefix='type')
            category_form = CategoryForm(prefix='category')
            subcategory_form = SubcategoryForm(prefix='subcategory')

            if status_form.is_valid():
                status_form.save()
                return redirect('flow:manage_references')

        elif 'submit_type' in request.POST:
            status_form = StatusForm(prefix='status')
            type_form = TypeForm(request.POST, prefix='type')
            category_form = CategoryForm(prefix='category')
            subcategory_form = SubcategoryForm(prefix='subcategory')

            if type_form.is_valid():
                type_form.save()
                return redirect('flow:manage_references')

        elif 'submit_category' in request.POST:
            status_form = StatusForm(prefix='status')
            type_form = TypeForm(prefix='type')
            category_form = CategoryForm(request.POST, prefix='category')
            subcategory_form = SubcategoryForm(prefix='subcategory')

            if category_form.is_valid():
                category_form.save()
                return redirect('flow:manage_references')

        elif 'submit_subcategory' in request.POST:
            status_form = StatusForm(prefix='status')
            type_form = TypeForm(prefix='type')
            category_form = CategoryForm(prefix='category')
            subcategory_form = SubcategoryForm(request.POST, prefix='subcategory')

            if subcategory_form.is_valid():
                subcategory_form.save()
                return redirect('flow:manage_references')

        if 'delete_status' in request.POST:
            status_id = request.POST.get('delete_status')
            try:
                get_object_or_404(Status, id=status_id).delete()
            except ProtectedError:
                messages.error(request, "Невозможно удалить статус: он используется в движении средств.")
            return redirect('flow:manage_references')

        if 'delete_type' in request.POST:
            type_id = request.POST.get('delete_type')
            try:
                get_object_or_404(Type, id=type_id).delete()
            except ProtectedError:
                messages.error(request, "Невозможно удалить тип: он используется в движении средств.")
            return redirect('flow:manage_references')

        if 'delete_category' in request.POST:
            category_id = request.POST.get('delete_category')
            try:
                get_object_or_404(Category, id=category_id).delete()
            except ProtectedError:
                messages.error(request, "Невозможно удалить категорию: она используется в движении средств.")
            return redirect('flow:manage_references')

        if 'delete_subcategory' in request.POST:
            subcategory_id = request.POST.get('delete_subcategory')
            try:
                get_object_or_404(Subcategory, id=subcategory_id).delete()
            except ProtectedError:
                messages.error(request, "Невозможно удалить подкатегорию: она используется в движении средств.")
            return redirect('flow:manage_references')
    else:
        status_form = StatusForm(prefix='status')
        type_form = TypeForm(prefix='type')
        category_form = CategoryForm(prefix='category')
        subcategory_form = SubcategoryForm(prefix='subcategory')

    context = {
        'status_form': status_form,
        'type_form': type_form,
        'category_form': category_form,
        'subcategory_form': subcategory_form,
        'statuses': Status.objects.all(),
        'types': Type.objects.all(),
        'categories': Category.objects.select_related('type'),
        'subcategories': Subcategory.objects.select_related('category__type'),
    }
    return render(request, 'flow/manage.html', context)
