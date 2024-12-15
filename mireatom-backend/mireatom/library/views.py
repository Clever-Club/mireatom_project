from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.db.models import Q
from django.shortcuts import get_object_or_404
from math import ceil
import json

from .models import Formula, Variable
from .serializers import FormulaSerializer
from modules.lexer import count_coef


class FormulaCreationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        formula = json.loads(request.body).get("formula", None)
        if formula and formula.get("value", None):
            formula_obj = Formula.objects.create(value=formula['value'], user_id=user)
            return Response({'id': formula_obj.id}, status=status.HTTP_201_CREATED)
        return Response({'error': 'Отсутствует параметр "formula" или "value"'})


class FormulaView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, formula_id):
        formula_obj = get_object_or_404(Formula, pk=formula_id)
        formula = FormulaSerializer(formula_obj)

        return Response({'formula': formula.data}, status=status.HTTP_200_OK)

    def patch(self, request, formula_id):
        user = request.user
        formula = json.loads(request.body).get("formula", None)
        if formula:
            formula_obj = get_object_or_404(Formula, pk=formula_id)
            if formula.get('value', None):
                formula_obj.value = formula['value']
            if formula.get('name', None):
                formula_obj.name = formula['name']
            formula_obj.save()
            if formula.get('variables', None):
                for i in formula['variables']:
                    if not i:
                        continue
                    if not (i.get('value', None) and
                            i.get('name', None)):
                        return Response(
                            {'error': 'Variables json must contain "value" and "name"'},
                            status=status.HTTP_400_BAD_REQUEST
                        )
                    var = Variable.objects.create(
                        value=i['value'],
                        name=i['name'],
                        formula=formula_obj
                    )
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({'error': 'Request\'s body must contain "formula"'}, status=status.HTTP_400_BAD_REQUEST)


def time_func(n, m):
    return (len(n) + len(m)) * 0.1


class EstimateOperatingTimeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, formula_id):
        estimated_time = 0
        formula_obj = get_object_or_404(Formula, pk=formula_id)
        for i in Formula.objects.filter(~Q(pk=formula_id)):
            estimated_time += time_func(formula_obj.value, i.value)
        return Response({'time': ceil(estimated_time)}, status=status.HTTP_200_OK)


class FormulaAnalysisView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, formula_id):
        user = request.user
        formula_obj = get_object_or_404(Formula, pk=formula_id)
        formula_qs = Formula.objects.filter(~Q(pk=formula_id))
        match = []
        for i in formula_qs:
            result = json.loads(count_coef(formula_obj.value, i.value))
            match.append({
                'percentage': result['coefficient'],
                'value': i.value,
                'indexes': result['indexes']
            })
        return Response({'match': match}, status=status.HTTP_200_OK)


class GetFormulasListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        user = None
        if request.user.is_authenticated:
            user = request.user
        limit = request.GET.get("limit", None)
        page = request.GET.get("page", None)
        if not (limit and page and limit.isdigit() and page.isdigit()):
            return Response({'error': 'Invalid arguments'}, status=status.HTTP_400_BAD_REQUEST)
        limit = int(limit)
        page = int(page)
        formulas = Formula.objects.all()[limit * (page - 1):limit * page]
        formulas_serializer = FormulaSerializer(formulas, many=True)
        return Response({'formulas': formulas_serializer.data}, status=status.HTTP_200_OK)


class GetUserFormulasListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        limit = request.GET.get("limit", None)
        page = request.GET.get("page", None)
        if not (limit and page and limit.isdigit() and page.isdigit()):
            return Response({'error': 'Invalid arguments'}, status=status.HTTP_400_BAD_REQUEST)
        limit = int(limit)
        page = int(page)
        formulas = Formula.objects.filter(Q(user_id=user))[limit * (page - 1):limit * page]
        formulas_serializer = FormulaSerializer(formulas, many=True)
        return Response({'formulas': formulas_serializer.data}, status=status.HTTP_200_OK)

