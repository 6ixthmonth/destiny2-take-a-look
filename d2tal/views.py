from django.views.generic import ListView

from d2api.models import SalesItem


class HomeView(ListView):

    template_name = "d2api/index.html"
    paginate_by = 10

    def get_queryset(self):
        queryset = SalesItem.objects.order_by('-id')

        item_name = self.request.GET.get('itemName')
        if item_name:
            queryset = queryset.filter(item_hash__item_name__icontains=item_name)
        item_type_list = self.request.GET.getlist('itemType')
        if item_type_list:
            queryset = queryset.filter(item_hash__item_type__in=item_type_list)
            if 'Class Item' in item_type_list:
                pass
        class_list = self.request.GET.getlist('class')
        if class_list:
            queryset = queryset.filter(item_hash__class_type__in=class_list)
        vendor_list = self.request.GET.getlist('vendor')
        if vendor_list:
            queryset = queryset.filter(vendor_hash__vendor_name__in=vendor_list)
        start_date = self.request.GET.get('startDate')
        end_date = self.request.GET.get('endDate')
        if start_date and end_date:
            queryset = queryset.filter(sales_date__range=(start_date, end_date))
        # min_mobility = self.request.GET.get('minMobility')
        # max_mobility = self.request.GET.get('maxMobility')
        # min_resilience = self.request.GET.get('minResilience')
        # max_resilience = self.request.GET.get('maxResilience')
        # min_recovery = self.request.GET.get('minRecovery')
        # max_recovery = self.request.GET.get('maxRecovery')
        # min_discipline = self.request.GET.get('minDiscipline')
        # max_discipline = self.request.GET.get('maxDiscipline')
        # min_intellect = self.request.GET.get('minIntellect')
        # max_intellect = self.request.GET.get('maxIntellect')
        # min_strength = self.request.GET.get('minStrength')
        # max_strength = self.request.GET.get('maxStrength')

        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        item_name = self.request.GET.get('itemName')
        if item_name:
            context['item_name'] = item_name
        return context
