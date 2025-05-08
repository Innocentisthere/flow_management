from django import forms

from .models import MoneyFlow, Category, Subcategory, Type, Status


class MoneyFlowForm(forms.ModelForm):
    class Meta:
        model = MoneyFlow
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if 'type' in self.data:
            try:
                type_id = int(self.data.get('type'))
                self.fields['category'].queryset = Category.objects.filter(type_id=type_id)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['category'].queryset = Category.objects.filter(type=self.instance.type)
        else:
            self.fields['category'].queryset = Category.objects.none()

        if 'category' in self.data:
            try:
                category_id = int(self.data.get('category'))
                self.fields['subcategory'].queryset = Subcategory.objects.filter(category_id=category_id)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['subcategory'].queryset = Subcategory.objects.filter(category=self.instance.category)
        else:
            self.fields['subcategory'].queryset = Subcategory.objects.none()

    def clean(self):
        cleaned_data = super().clean()
        type_ = cleaned_data.get('type')
        category = cleaned_data.get('category')
        subcategory = cleaned_data.get('subcategory')

        if category and category.type != type_:
            raise forms.ValidationError("Категория не соответствует выбранному типу.")
        if subcategory and subcategory.category != category:
            raise forms.ValidationError("Подкатегория не соответствует выбранной категории.")


class MoneyFlowFilterForm(forms.Form):
    type = forms.ModelChoiceField(queryset=Type.objects.all(), required=False, label='Тип')
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=False, label='Категория')
    subcategory = forms.ModelChoiceField(queryset=Subcategory.objects.all(), required=False, label='Подкатегория')
    date_from = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}), label='С даты')
    date_to = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}), label='По дату')


class StatusForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = ['name']

    def clean_name(self):
        name = self.cleaned_data['name'].strip()
        qs = Status.objects.filter(name__iexact=name)
        if qs.exists():
            raise forms.ValidationError("Такой статус уже существует.")
        return name


class TypeForm(forms.ModelForm):
    class Meta:
        model = Type
        fields = ['name']

    def clean_name(self):
        name = self.cleaned_data['name'].strip()
        qs = Type.objects.filter(name__iexact=name)
        if qs.exists():
            raise forms.ValidationError("Такой тип уже существует.")
        return name


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'type']

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        type = cleaned_data.get('type')

        if name and type:
            name = name.strip()
            if Category.objects.filter(name__iexact=name, type=type).exists():
                raise forms.ValidationError("Категория с таким именем уже существует в выбранном типе.")
        return cleaned_data


class SubcategoryForm(forms.ModelForm):
    class Meta:
        model = Subcategory
        fields = ['name', 'category']

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        category = cleaned_data.get('category')

        if name and category:
            name = name.strip()
            if Subcategory.objects.filter(name__iexact=name, category=category).exists():
                raise forms.ValidationError("Подкатегория с таким именем уже существует в выбранной категории.")
        return cleaned_data
