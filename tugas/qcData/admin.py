from django.contrib import admin
from .models import Stasiun, Pegawai, dataStasiun

# Register your models here.

# admin.site.register(Stasiun)
# admin.site.register(Pegawai)
# admin.site.register(dataStasiun)


@admin.register(Stasiun)
class StasiunAdmin(admin.ModelAdmin):
    list_display = ('nama', 'alamat', 'telepon', 'email', 'kepalaStasiun')


@admin.register(Pegawai)
class PegawaiAdmin(admin.ModelAdmin):
    list_display = ('nip', 'nama', 'stasiunKerja')
    list_filter = ('stasiunKerja',)


@admin.register(dataStasiun)
class dataStasiunAdmin(admin.ModelAdmin):
    list_filter = ('stasiun',)
