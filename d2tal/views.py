from django.views.generic import ListView

from dbapp.models import SalesItem


class HomeView(ListView):

    template_name = "d2tal/index.html"
    paginate_by = 10

    def get_queryset(self):
        queryset = SalesItem.objects.order_by('-id')

        item_name = self.request.GET.get('itemName')
        if item_name:
            queryset = queryset.filter(item_hash__item_name__icontains=item_name)
        item_type_list = self.request.GET.getlist('itemType')
        if item_type_list:
            queryset = queryset.filter(item_hash__item_type__in=item_type_list)
        class_list = self.request.GET.getlist('class')
        if class_list:
            queryset = queryset.filter(item_hash__class_type__in=class_list)
        vendor_list = self.request.GET.getlist('vendor')
        if vendor_list:
            queryset = queryset.filter(vendor_hash__vendor_name__in=vendor_list)
        start_date = self.request.GET.get('startDate')
        if start_date:
            queryset = queryset.filter(sales_date__gte=start_date)
        end_date = self.request.GET.get('endDate')
        if end_date:
            queryset = queryset.filter(sales_date__lte=end_date)
        min_mobility = self.request.GET.get('minMobility')
        if min_mobility:
            queryset = queryset.filter(mobility__gte=min_mobility)
        max_mobility = self.request.GET.get('maxMobility')
        if max_mobility:
            queryset = queryset.filter(mobility__lte=max_mobility)
        min_resilience = self.request.GET.get('minResilience')
        if min_resilience:
            queryset = queryset.filter(resilience__gte=min_resilience)
        max_resilience = self.request.GET.get('maxResilience')
        if max_resilience:
            queryset = queryset.filter(resilience__lte=max_resilience)
        min_recovery = self.request.GET.get('minRecovery')
        if min_recovery:
            queryset = queryset.filter(recovery__gte=min_recovery)
        max_recovery = self.request.GET.get('maxRecovery')
        if max_recovery:
            queryset = queryset.filter(recovery__lte=max_recovery)
        min_discipline = self.request.GET.get('minDiscipline')
        if min_discipline:
            queryset = queryset.filter(discipline__gte=min_discipline)
        max_discipline = self.request.GET.get('maxDiscipline')
        if max_discipline:
            queryset = queryset.filter(discipline__lte=max_discipline)
        min_intellect = self.request.GET.get('minIntellect')
        if min_intellect:
            queryset = queryset.filter(intellect__gte=min_intellect)
        max_intellect = self.request.GET.get('maxIntellect')
        if max_intellect:
            queryset = queryset.filter(intellect__lte=max_intellect)
        min_strength = self.request.GET.get('minStrength')
        if min_strength:
            queryset = queryset.filter(strength__gte=min_strength)
        max_strength = self.request.GET.get('maxStrength')
        if max_strength:
            queryset = queryset.filter(strength__lte=max_strength)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        item_name = self.request.GET.get('itemName')
        if item_name:
            context['item_name'] = item_name
        item_type_list = self.request.GET.getlist('itemType')
        if item_type_list:
            context['item_type'] = item_type_list
        class_list = self.request.GET.getlist('class')
        if class_list:
            context['class'] = class_list
        vendor_list = self.request.GET.getlist('vendor')
        if vendor_list:
            context['vendor'] = vendor_list
        start_date = self.request.GET.get('startDate')
        if start_date:
            context['startDate'] = start_date
        end_date = self.request.GET.get('endDate')
        if end_date:
            context['endDate'] = end_date
        min_mobility = self.request.GET.get('minMobility')
        if min_mobility:
            context['minMobility'] = min_mobility
        max_mobility = self.request.GET.get('maxMobility')
        if max_mobility:
            context['maxMobility'] = max_mobility
        min_resilience = self.request.GET.get('minResilience')
        if min_resilience:
            context['minResilience'] = min_resilience
        max_resilience = self.request.GET.get('maxResilience')
        if max_resilience:
            context['maxResilience'] = max_resilience
        min_recovery = self.request.GET.get('minRecovery')
        if min_recovery:
            context['minRecovery'] = min_recovery
        max_recovery = self.request.GET.get('maxRecovery')
        if max_recovery:
            context['maxRecovery'] = max_recovery
        min_discipline = self.request.GET.get('minDiscipline')
        if min_discipline:
            context['minDiscipline'] = min_discipline
        max_discipline = self.request.GET.get('maxDiscipline')
        if max_discipline:
            context['maxDiscipline'] = max_discipline
        min_intellect = self.request.GET.get('minIntellect')
        if min_intellect:
            context['minIntellect'] = min_intellect
        max_intellect = self.request.GET.get('maxIntellect')
        if max_intellect:
            context['maxIntellect'] = max_intellect
        min_strength = self.request.GET.get('minStrength')
        if min_strength:
            context['minStrength'] = min_strength
        max_strength = self.request.GET.get('maxStrength')
        if max_strength:
            context['maxStrength'] = max_strength

        return context
