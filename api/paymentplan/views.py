from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db import transaction as db_transaction
from sql.models import PaymentPlan, Expense
from .serializers import PaymentPlanSerializer
from rest_framework.decorators import action

class PaymentPlanViewSet(viewsets.ModelViewSet):
    queryset = PaymentPlan.objects.all()
    serializer_class = PaymentPlanSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return PaymentPlan.objects.filter(user=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def mark_completed(self, request, pk=None):
        plan = self.get_object()
        if plan.status != 'PENDING':
            return Response({"error": "Plan is already completed or canceled."},status=status.HTTP_400_BAD_REQUEST)
        # SAMIP REGMI
        # Convert payment plan into expense and update status
        if hasattr(plan, 'transaction'):
            return Response({"error": "Plan is already linked to a transaction."},status=status.HTTP_400_BAD_REQUEST,)

        with db_transaction.atomic():
            Expense.objects.create(
                user=request.user,
                type='Expense',
                amount=plan.amount,
                category=plan.title[:50],
                description=plan.description,
            )
            plan.status = 'COMPLETED'
            plan.save(update_fields=['status'])

        return Response(self.get_serializer(plan).data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def mark_canceled(self, request, pk=None):
        plan = self.get_object()
        if plan.status != 'PENDING':
            return Response({"error": "Plan is already completed or canceled."},status=status.HTTP_400_BAD_REQUEST)
        plan.status = 'CANCELED'
        plan.save()
        return Response(self.get_serializer(plan).data, status=status.HTTP_200_OK)
