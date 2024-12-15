from django.urls import path

from .views import (FormulaView, FormulaCreationView, GetFormulasListView,
                    FormulaAnalysisView, GetUserFormulasListView, EstimateOperatingTimeView)


urlpatterns = [
    path("formula", FormulaCreationView.as_view(), name='create_formula'),
    path("formula/<int:formula_id>", FormulaView.as_view(), name="get_formula"),
    path("formulas", GetFormulasListView.as_view(), name="get_formulas_list"),
    path("user/formulas", GetUserFormulasListView.as_view(), name="get_user_formulas_list"),
    path("formula/<int:formula_id>/analysis", FormulaAnalysisView.as_view(), name="formula_analysis"),
    path("formula/<int:formula_id>/analysis/time", EstimateOperatingTimeView.as_view(), name="formula_analysis_time"),
]