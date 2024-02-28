from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView, LogoutView
from django.db.models import Sum, F
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import DetailView

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.cache import cache
from .forms import UserForm, ProfileForm, GoodForm, ProviderForm, GoodCategoryForm, SupplyForm, \
    SaleForm, SupplyGoodFormSet, SaleItemFormSet
from .models import Profile, Provider, Good, GoodCategory, Supply, Sale
from .serializers import ProviderSerializer, GoodSerializer

def register_view(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = ProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            birthday = profile_form.cleaned_data['birthday']
            phone = profile_form.cleaned_data['phone']
            profile = Profile.objects.create(
                user=user,
                birthday=birthday,
                phone=phone,
            )
            profile.save()

            username = user_form.cleaned_data['username']
            raw_password = user_form.cleaned_data['password1']
            auth_user = authenticate(username=username, password=raw_password)
            login(request, auth_user)
            return redirect('profile')
        else:
            messages.add_message(request, messages.ERROR, 'Форма невалидна!')

    user_form = UserForm()
    profile_form = ProfileForm()
    return render(request, 'app_store/register.html', context={
        'user_form': user_form,
        'profile_form': profile_form
    })



class CustomLoginView(LoginView):
    template_name = 'app_store/login.html'
    next_page = 'profile'

    def form_valid(self, form):
        response = super(CustomLoginView, self).form_valid(form)
        return response


class CustomLogoutView(LogoutView):
    template_name = 'app_store/logout.html'
    next_page = 'register'

def profile_view(request):
    profile = get_object_or_404(Profile, user=request.user)
    return render(request, 'app_store/profile.html', context={'profile': profile})


# ------------------------------------API----------------------------------------------------------------------------
CACHE_TIME = 60 * 60 * 2

class ProviderAPIView(APIView):

    def get(self, request):
        data = cache.get_or_set('providers_list', Provider.objects.all(), CACHE_TIME)
        return JsonResponse(ProviderSerializer(data, many=True).data, safe=False)

    def post(self, request):
        serializer = ProviderSerializer(data=request.data)
        if serializer.is_valid():
            cache.delete('providers_list')
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProviderDetailAPI(APIView):

    def get(self, request, pk):
        provider = get_object_or_404(Provider, pk=pk)
        data = cache.get_or_set(f'provider_{pk}', provider, CACHE_TIME)
        return JsonResponse(ProviderSerializer(data).data, safe=False)

    def put(self, request, pk):
        provider = get_object_or_404(Provider, pk=pk)
        serializer = ProviderSerializer(provider, data=request.data)
        if serializer.is_valid():
            cache.delete(f'provider_{pk}')
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GoodAPIView(APIView):

    def get(self, request):
        data = cache.get_or_set('goods_list', Good.objects.all(), CACHE_TIME)
        return JsonResponse(GoodSerializer(data, many=True).data, safe=False)

    def post(self, request):
        serializer = GoodSerializer(data=request.data)
        if serializer.is_valid():
            cache.delete('goods_list')
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GoodDetailAPI(APIView):

    def get(self, request, pk):
        good = get_object_or_404(Good, pk=pk)
        data = cache.get_or_set(f'good_{pk}', good, CACHE_TIME)
        return JsonResponse(GoodSerializer(data).data, safe=False)

    def put(self, request, pk):
        good = get_object_or_404(Good, pk=pk)
        serializer = GoodSerializer(good, data=request.data)
        if serializer.is_valid():
            cache.delete(f'good_{pk}')
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ---------------------------------------------------Views--------------------------------------------------------------

class ProviderListView(View):
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

def delete_provider(request, provider_id):
    provider = get_object_or_404(Provider, pk=provider_id)
    if request.method == 'POST':
        provider.delete()
    return redirect('providers_list')

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


class GoodCategoryListView(View):
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

def delete_category(request, category_id):
    category = get_object_or_404(GoodCategory, pk=category_id)
    if request.method == 'POST':
        category.delete()
    return redirect('categories_list')


class GoodsListView(View):
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

def delete_good(request, good_id):
    good = get_object_or_404(Good, pk=good_id)
    if request.method == 'POST':
        good.delete()
    return redirect('goods_list')

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

class GoodDetailView(DetailView):
    model = Good
    template_name = 'app_store/good_detail.html'
    context_object_name = 'good'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest_supplies'] = self.object.supplygood_set.order_by('-supply__supply_date')[:3]
        context['latest_sales'] = self.object.saleitem_set.order_by('-sale__sale_date')[:3]
        return context


def create_supply(request):
    if request.method == 'POST':
        supply_form = SupplyForm(request.POST)
        supply_good_formset = SupplyGoodFormSet(request.POST)
        if supply_form.is_valid() and supply_good_formset.is_valid():
            supply = supply_form.save()
            instances = supply_good_formset.save(commit=False)
            for instance in instances:
                instance.supply = supply
                instance.save()
            return redirect('supply_list')
    else:
        supply_form = SupplyForm()
        supply_good_formset = SupplyGoodFormSet()
    return render(request, 'app_store/create_supply.html', {'supply_form': supply_form, 'supply_good_formset': supply_good_formset})

def supply_list(request):
    supplies = Supply.objects.all()
    return render(request, 'app_store/supply_list.html', {'supplies': supplies})



def create_sale(request):
    if request.method == 'POST':
        sale_form = SaleForm(request.POST)
        sale_item_formset = SaleItemFormSet(request.POST)
        if sale_form.is_valid() and sale_item_formset.is_valid():
            sale = sale_form.save()
            instances = sale_item_formset.save(commit=False)
            for instance in instances:
                instance.sale = sale
                instance.save()
            return redirect('sales_list')
    else:
        sale_form = SaleForm()
        sale_item_formset = SaleItemFormSet()
    return render(request, 'app_store/create_sale.html', {'sale_form': sale_form, 'sale_item_formset': sale_item_formset})

def get_good_price(request, good_id):
    try:
        good = Good.objects.get(id=good_id)
        return JsonResponse({'price': float(good.selling_price)})
    except Good.DoesNotExist:
        return JsonResponse({'error': 'Товар не найден'}, status=404)


def sales_list(request):
    sales = Sale.objects.all()
    for sale in sales:
        final_cost = sale.final_cost_with_discount()
        sale.final_cost = final_cost
        sale.save()
    return render(request, 'app_store/sales_list.html', {'sales': sales})