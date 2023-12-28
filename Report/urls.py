from django.urls import path
from Report.views import ReportApiHandler, ReportByDatePdfHandler, ReportProductByCategoryPdfHandler, ReportByOrderDatePdfHandler

urlpatterns = [
    path("", ReportApiHandler.as_view(), name="report_handler"),
    path("date", ReportByDatePdfHandler.as_view(), name="report_by_date_handler"),
    path("product/category", ReportProductByCategoryPdfHandler.as_view(), name="product_by_category_handler"),
    path("order", ReportByOrderDatePdfHandler.as_view(), name="report_by_order_date"),
]