import django_filters as df
from .models import Order


class OrderFilter(df.FilterSet):
    start_date = df.DateTimeFilter(
        field_name='date_created',
        lookup_expr='gte',
        label='Starting date:'
    )
    end_date = df.DateTimeFilter(
        field_name='date_created',
        lookup_expr='lte',
        label='Ending date:'
    )

    # text = df.CharFilter(
    #     field_name='text',
    #     lookup_expr='icontains',
    #     label='Contains:'
    # )

    class Meta:
        model = Order
        fields = '__all__'
        exclude = ['customer', 'date_created']
