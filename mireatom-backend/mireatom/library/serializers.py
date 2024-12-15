from rest_framework import serializers

from .models import Formula, Variable


class VariableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variable
        fields = ('name', 'value')


class FormulaSerializer(serializers.ModelSerializer):
    variables = VariableSerializer(source='variable_set', many=True)

    class Meta:
        model = Formula
        fields = ('value', 'name', 'variables')