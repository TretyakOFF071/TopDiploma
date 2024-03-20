from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.db.models import Sum, F
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import DetailView, ListView


from .forms import UserForm, ProfileForm, GoodForm, ProviderForm, GoodCategoryForm, SupplyForm, \
    SaleForm, SupplyGoodFormSet, SaleItemFormSet
from .models import Profile, Provider, Good, GoodCategory, Supply, Sale




def register_view(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = ProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            birthday = profile_form.cleaned_data['birthday']
            phone = profile_form.cleaned_data['phone']
            position = profile_form.cleaned_data['position']
            profile = Profile.objects.create(
                user=user,
                birthday=birthday,
                phone=phone,
                position=position
            )
            profile.save()

            username = user_form.cleaned_data['username']
            raw_password = user_form.cleaned_data['password1']
            auth_user = authenticate(username=username, password=raw_password)
            login(request, auth_user)
            return redirect('goods_list')
        else:
            for field, errors in user_form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
            for field, errors in profile_form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")

    else:
        user_form = UserForm()
        profile_form = ProfileForm()

    return render(request, 'app_store/register.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })



class CustomLoginView(LoginView):
    template_name = 'app_store/login.html'
    next_page = 'goods_list'

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()

        form = super().get_form(form_class)
        form.fields['username'].widget.attrs.update({'class': 'form-control', 'style': 'width: 250px; margin: 0 auto;'})
        form.fields['password'].widget.attrs.update({'class': 'form-control', 'style': 'width: 250px; margin: 0 auto;'})
        return form

    def form_valid(self, form):
        response = super().form_valid(form)
        return response


class CustomLogoutView(LogoutView):
    template_name = 'app_store/logout.html'
    next_page = 'login'

class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        profile = get_object_or_404(Profile, user=request.user)
        return render(request, 'app_store/profile.html', {'profile': profile})


class ProviderListView(LoginRequiredMixin, View):
    def get(self, request):
        providers = Provider.objects.all()
        categories = GoodCategory.objects.all()
        selected_category = request.GET.get('category')
        name_filter = request.GET.get('name')

        if 'clear_filters' in request.GET:
            selected_category = None
            name_filter = ''

        if selected_category:
            providers = providers.filter(categories__id=selected_category)

        if name_filter:
            providers = providers.filter(name__icontains=name_filter)

        form = ProviderForm()
        return render(request, 'app_store/providers_list.html', {
            'providers': providers,
            'form': form,
            'categories': categories,
            'selected_category': selected_category,
            'name_filter': name_filter,
        })

    def post(self, request):
        form = ProviderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('providers_list')
        else:
            providers = Provider.objects.all()
            categories = GoodCategory.objects.all()
            return render(request, 'app_store/providers_list.html', {
                'providers': providers,
                'form': form,
                'categories': categories,
            })

@login_required
def delete_provider(request, provider_id):
    provider = get_object_or_404(Provider, pk=provider_id)
    if request.method == 'POST':
        provider.delete()
    return redirect('providers_list')

@login_required
def edit_provider(request, provider_id):
    provider = get_object_or_404(Provider, pk=provider_id)
    if request.method == 'POST':
        form = ProviderForm(request.POST, instance=provider)
        if form.is_valid():
            form.save()
            return redirect('providers_list')
    else:
        form = ProviderForm(instance=provider)
    return render(request, 'app_store/edit_provider.html', {'form': form, 'provider': provider})


class GoodCategoryListView(LoginRequiredMixin, View):
    def get(self, request):
        categories = GoodCategory.objects.all()
        form = GoodCategoryForm()
        return render(request, 'app_store/categories_list.html', {'categories': categories, 'form': form})

    def post(self, request):
        form = GoodCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('categories_list')
        else:
            categories = GoodCategory.objects.all()
            return render(request, 'app_store/categories_list.html', {'categories': categories, 'form': form})

@login_required
def delete_category(request, category_id):
    category = get_object_or_404(GoodCategory, pk=category_id)
    if request.method == 'POST':
        category.delete()
    return redirect('categories_list')


class GoodsListView(LoginRequiredMixin, View):
    def get(self, request):
        goods = Good.objects.all()
        categories = GoodCategory.objects.all()
        selected_category = request.GET.get('category')
        name_filter = request.GET.get('name')
        part_number_filter = request.GET.get('part_number')

        if 'clear_filters' in request.GET:
            selected_category = None
            name_filter = ''
            part_number_filter = ''

        if selected_category:
            goods = goods.filter(category__id=selected_category)
        if name_filter:
            goods = goods.filter(name__icontains=name_filter)
        if part_number_filter:
            goods = goods.filter(part_number__icontains=part_number_filter)

        total_selling_price = goods.aggregate(total=Sum(F('selling_price') * F('quantity')))['total'] or 0
        total_purchase_price = goods.aggregate(total=Sum(F('purchase_price') * F('quantity')))['total'] or 0
        form = GoodForm()
        return render(request, 'app_store/goods_list.html', {
            'goods': goods,
            'form': form,
            'categories': categories,
            'selected_category': selected_category,
            'name_filter': name_filter,
            'part_number_filter': part_number_filter,
            'total_purchase_price': total_purchase_price,
            'total_selling_price': total_selling_price
        })

    def post(self, request):
        form = GoodForm(request.POST, request.FILES)
        if form.is_valid():
            part_number = form.cleaned_data['part_number']
            if Good.objects.filter(part_number=part_number).exists():
                messages.error(request, 'Товар с таким артикулом уже существует.')
                return redirect('goods_list')
            form.save()
            return redirect('goods_list')
        else:
            goods = Good.objects.all()
            categories = GoodCategory.objects.all()
            return render(request, 'app_store/goods_list.html', {
                'goods': goods,
                'form': form,
                'categories': categories,
            })

@login_required
def delete_good(request, good_id):
    good = get_object_or_404(Good, pk=good_id)
    if request.method == 'POST':
        good.delete()
    return redirect('goods_list')

@login_required
def edit_good(request, good_id):
    good = get_object_or_404(Good, pk=good_id)
    if request.method == 'POST':
        form = GoodForm(request.POST, request.FILES, instance=good)
        if form.is_valid():
            form.save()
            return redirect('goods_list')
    else:
        form = GoodForm(instance=good)
    return render(request, 'app_store/edit_good.html', {'form': form, 'good': good})

class GoodDetailView(LoginRequiredMixin ,DetailView):
    model = Good
    template_name = 'app_store/good_detail.html'
    context_object_name = 'good'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest_supplies'] = self.object.supplygood_set.order_by('-supply__supply_date')[:3]
        context['latest_sales'] = self.object.saleitem_set.order_by('-sale__sale_date')[:3]
        return context


class CreateSupplyView(View):
    form_class = SupplyForm
    formset_class = SupplyGoodFormSet
    template_name = 'app_store/create_supply.html'

    def get(self, request):
        form = self.form_class()
        formset = self.formset_class()
        return render(request, self.template_name, {'supply_form': form, 'supply_good_formset': formset})

    def post(self, request):
        form = self.form_class(request.POST)
        formset = self.formset_class(request.POST)
        if form.is_valid() and formset.is_valid():
            for form_data in formset.cleaned_data:
                if form_data and form_data['quantity'] <= 0:
                    messages.error(request, "Количество должно быть больше 0")
                    form = self.form_class()
                    formset = self.formset_class()
                    break
            else:
                supply = form.save()
                instances = formset.save(commit=False)
                for instance in instances:
                    instance.supply = supply
                    instance.save()
                return redirect('supply_list')
        return render(request, self.template_name, {'supply_form': form, 'supply_good_formset': formset})

class SupplyListView(LoginRequiredMixin, ListView):
    model = Supply
    template_name = 'app_store/supply_list.html'
    context_object_name = 'supplies'



class CreateSaleView(LoginRequiredMixin, View):
    template_name = 'app_store/create_sale.html'

    def get(self, request):
        sale_form = SaleForm()
        sale_item_formset = SaleItemFormSet()
        return render(request, self.template_name, {'sale_form': sale_form, 'sale_item_formset': sale_item_formset})

    def post(self, request):
        sale_form = SaleForm(request.POST)
        sale_item_formset = SaleItemFormSet(request.POST)
        if sale_form.is_valid() and sale_item_formset.is_valid():
            for form in sale_item_formset:
                good = form.cleaned_data.get('good')
                quantity = form.cleaned_data.get('quantity')
                if good and good.quantity < quantity:
                    messages.error(request, f"Недостаточно товара '{good.name}' в наличии для продажи")
                    empty_formset = SaleItemFormSet()
                    return render(request, self.template_name, {'sale_form': sale_form, 'sale_item_formset': empty_formset})
                elif good and quantity <= 0:
                    messages.error(request, f"Количество товара '{good.name}' должно быть больше 0")
                    empty_formset = SaleItemFormSet()
                    return render(request, self.template_name, {'sale_form': sale_form, 'sale_item_formset': empty_formset})
            sale = sale_form.save()
            instances = sale_item_formset.save(commit=False)
            for instance in instances:
                instance.sale = sale
                instance.save()
            return redirect('sales_list')
        else:
            return render(request, self.template_name, {'sale_form': sale_form, 'sale_item_formset': sale_item_formset})

class GetGoodPriceView(LoginRequiredMixin, View):
    def get(self, request, good_id):
        try:
            good = Good.objects.get(id=good_id)
            return JsonResponse({'price': float(good.selling_price)})
        except Good.DoesNotExist:
            return JsonResponse({'error': 'Товар не найден'}, status=404)


class SalesListView(LoginRequiredMixin, ListView):
    model = Sale
    template_name = 'app_store/sales_list.html'
    context_object_name = 'sales'

    def get_queryset(self):
        sales = super().get_queryset()
        for sale in sales:
            final_cost = sale.final_cost_with_discount()
            sale.final_cost = final_cost
            sale.save()
        return sales

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        total_sum = self.get_queryset().aggregate(total_sum=Sum('final_cost'))['total_sum']
        context['total_sum'] = total_sum
        return context