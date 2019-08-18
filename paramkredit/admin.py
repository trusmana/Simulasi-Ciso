from django.contrib import admin
from import_export.admin import ImportExportMixin, ExportActionModelAdmin
from paramkredit.models import ParameterPencairan,Produk

class ParameterPencairanAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ['id', 'produk', 'kantor_bayar','kode_bank','bunga','jenis_bunga','status_pensiun','jenis_pengajuan','min_usia','max_usia',\
        'min_tenor','max_tenor','min_plafon','max_plafon']
    search_fields = ['id']
admin.site.register(ParameterPencairan,ParameterPencairanAdmin)

class ProdukAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ['id', ]
    search_fields = ['id']
admin.site.register(Produk,ProdukAdmin)


