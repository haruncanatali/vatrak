from django.views import View
from django.http import HttpResponse, JsonResponse
from Report.models import Reports
from Product.models import Products
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
import json
from xhtml2pdf import pisa
from Product.serializers import ProductByCategoryReportSerializer
import base64
import html


class ReportApiHandler(View):
    def get(self, request):
        return


class ReportByDatePdfHandler(View):
    def get(self, request, start_date, end_date):
        return


class ReportByOrderDatePdfHandler(View):
    def get(self, request, start_date, end_date):
        return


class ReportProductByCategoryPdfHandler(View):
    def get(self, request):
        products_query_result = Products.objects.all()
        products = ProductByCategoryReportSerializer(products_query_result, many=True).data
        df = pd.DataFrame(products, columns=["name", "price", "category"])
        df.columns = ['Ürün', 'Fiyat', 'Kategori']

        df_to_html = df.to_html()

        category_counts = df['Kategori'].value_counts()

        # Matplotlib ile bir figür oluşturalım
        fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(12, 12))

        # İlk grafik: Pasta grafiği
        axes[0].pie(category_counts, labels=category_counts.index, autopct='%1.1f%%', startangle=90)
        axes[0].axis('equal')  # Daireyi daire olarak görüntülemek için
        axes[0].set_title('Kategori Dağılımı')

        # İkinci grafik: Fiyatlar
        axes[1].hist(df['Fiyat'], bins=20, color='skyblue', edgecolor='black')
        axes[1].set_title('Fiyat Dağılımı')
        axes[1].set_xlabel('Fiyat')
        axes[1].set_ylabel('Ürün Sayısı')

        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        plt.close()

        buffer_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

        html_table = '<h1 style=\'text-align: center;\'>Ürünler</h1>' + df_to_html
        html_graph = f'<img src="data:image/png;base64,{buffer_base64}" />'
        html_report = f'<h1 style=\'text-align: center;\'>Ürünler ve Kategorilere Göre Dağılım</h1>{html_table}{html_graph}'

        result = pisa.CreatePDF(html_report, dest=BytesIO())
        response = HttpResponse(content_type='application/pdf')
        response.write(result.dest.getvalue())

        return response
