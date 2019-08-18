from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal

JENIS_PENGAJUAN =(
    ('1','SKEP ON HAND'),('2','TAKE OVER'),
)

JENIS_ANGSURAN=(
    ('0','--PILIH--'),('1','FLAT'), ('2','ANUITAS'),('3','EFEKTIF'),
)

KODE_BANK = (('','---PILIH---'),('9','Bank Syariah Bukopin'),('8','Bank Bukopin'))

JENIS_PENGAJUAN_KREDIT =(
    ('1','SKEP ON HAND'),('2','TAKE OVER'),
)

JENIS_PENGAJUAN =(
    ('1','SK Ditangan'),('2','TakeOver'))

STATUS_PARAM =(
    ('1','Aktif'),('2','None Aktif'),
)

JENIS_PENSIUN =(
    ('','--PILIH--'),('1','Sendiri'),('2','Janda'),('3','Duda Sendiri'),('4','Duda Turunan'),
)

BANK_KREDIT_CHOICES = (
    ('','--PILIH--'),('1', 'Kantor Pos'),('2', 'Bank BSB'),('3', 'Bank Bukopin'),
)

AKTIF_CHOICES = (('1','AKTIF'),('2','NONAKTIF'),)

class Produk(models.Model):
    id_prod = models.IntegerField(null=True)
    nama_produk = models.CharField(max_length=100,null=True)
    tgl_aktif = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=4,choices=AKTIF_CHOICES)

    class Meta:
        db_table = 'produk'
        verbose_name= 'Produk'
        verbose_name_plural =verbose_name

    def __unicode__(self):
        return '%s-%s' %(self.id, self.nama_produk)


class ParameterPencairan(models.Model):
    kode_bank = models.CharField(choices = KODE_BANK,blank=True,max_length=2)
    status_pensiun = models.CharField(max_length=2,choices=JENIS_PENSIUN,blank=True,null=True)
    produk = models.ForeignKey(Produk, null=True, blank=True)
    max_usia = models.IntegerField(null=True,blank=True)
    min_usia = models.IntegerField(null=True,blank=True)
    max_plafon = models.FloatField(null=True)
    min_plafon = models.FloatField(null=True)
    max_tenor = models.IntegerField(null=True)
    min_tenor = models.IntegerField(null=True)
    max_tiring_tenor = models.IntegerField(null=True,blank=True)
    min_tiring_tenor = models.IntegerField(null=True,blank=True)
    rete_produk = models.FloatField(null=True)
    jenis_bunga = models.CharField(max_length=10,blank=True,null=True,choices=JENIS_ANGSURAN)
    adm = models.DecimalField(max_digits=12, decimal_places=2,null=True,blank=True,default=0)
    provisi = models.DecimalField(max_digits=12, decimal_places=2,null=True,blank=True,default=0)
    bunga = models.DecimalField(max_digits=12, decimal_places=4,null=True,blank=True,default=0,
        help_text='Bunga Pertahun Tetapi Sudah Di bagi 100 ch jika 24% Pertahun maka input 0,24')
    dsr = models.DecimalField(max_digits=12, decimal_places=2,null=True,blank=True,default=0)
    jenis_pengajuan = models.CharField(max_length=2,choices=JENIS_PENGAJUAN_KREDIT,blank=True,null=True)
    kantor_bayar = models.CharField(max_length=2, choices=BANK_KREDIT_CHOICES,blank=True,null=True)
    status = models.CharField(max_length=50,null=True,blank=True,choices=STATUS_PARAM)
    tanggal= models.DateField(blank=True,null=True)
    max_bulan_usia = models.IntegerField(blank=True,null=True)
    max_hari_usia = models.IntegerField(blank=True,null=True)
    cu = models.ForeignKey(User, related_name='+', editable=False, null=True, blank=True)
    mu = models.ForeignKey(User, related_name='+', editable=False, null=True, blank=True)
    cdate = models.DateTimeField(auto_now_add=True)
    mdate = models.DateTimeField(auto_now=True)
    bunga_bank = models.DecimalField(max_digits=12,decimal_places=4,null=True,blank=True,default=0,
            help_text='Bunga Pertahun Tetapi Sudah Di bagi 100 ch jika 24% Pertahun maka input 0,24')

    class Meta:
        db_table = 'parameterpencairan'
        verbose_name = 'ParameterPencairan'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return '%s - [ Kantor Bayar:%s ]' %(self.produk.nama_produk, self.get_kantor_bayar_display())

    ### HITUNG ANGSURAN UNTUK SIMULASI DAN YANG INTI JUGA
    def angsuran_anuitas(self,plafon,tenor):
        rate = self.bunga / 12
        angs = (Decimal(plafon)* rate)/(1-1/(1+rate)**int(tenor))
        bunga = Decimal(plafon) * rate
        pokok = (round((angs - bunga), 2))
        return bunga + Decimal(pokok)
