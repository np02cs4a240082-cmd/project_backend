import django_filters
from rest_framework import serializers
from sql.models import Expense

class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = ['id', 'user', 'amount', 'type','category','description', 'date']
        read_only_fields = ['user']

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than zero.")
        return value
    
    def validate(self, data):
        user = self.context['request'].user
        expense_type = data.get('type', getattr(self.instance, 'type', None))
        amount = data.get('amount', getattr(self.instance, 'amount', None))

        if expense_type == 'Expense':
            required_amount = amount

            if self.instance and self.instance.type == 'Expense':
                # SAMIP REGMI: when editing an existing expense, only the extra delta needs new balance.
                required_amount = amount - self.instance.amount

            if required_amount > 0 and user.balance < required_amount:
                raise serializers.ValidationError("Insufficient balance for this expense.")
        return data
    

class ExpenseFilter(django_filters.FilterSet):
    start_date = django_filters.DateFilter(field_name='date', lookup_expr='gte')
    end_date = django_filters.DateFilter(field_name='date', lookup_expr='lte')
    min_amount = django_filters.NumberFilter(field_name='amount', lookup_expr='gte')
    max_amount = django_filters.NumberFilter(field_name='amount', lookup_expr='lte')

    class Meta:
        model = Expense
        fields = ['type', 'category', 'start_date', 'end_date', 'min_amount', 'max_amount']
