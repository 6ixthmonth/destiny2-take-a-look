from django.views.generic import ListView

from d2api.models import SalesItem


class HomeView(ListView):

    template_name = "d2api/index.html"

    def get_queryset(self):
        queryset = SalesItem.objects.order_by('-id')
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
