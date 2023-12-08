from django.views import View
from Report.models import Reports
import json


class ReportApiHandler(View):
    def get(self, request):
        return 


class ReportByDatePdfHandler(View):
    def get(self, request, start_date, end_date):
        reports = Reports.objects.filter(date__range=[start_date,end_date]).all()


class ReportByOrderDatePdfHandler(View):
    def get(self, request, start_date, end_date):
        reports = Reports.objects.filter()
