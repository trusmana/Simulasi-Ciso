from django import forms
from paramkredit.models import ParameterPencairan,BANK_KREDIT_CHOICES,JENIS_PENSIUN,KODE_BANK, JENIS_PENGAJUAN,Produk

MUTASI_CH =(('1','Tidak'),('2','YA'))
RETENSI_CH =(('','--PILIH---'),('1','1'),('2','2'),('3','3'),('4','4'),('5','5'),('6','6'),
    ('7','7'),('8','8'))

class SimulasiForm(forms.Form):
    kode_inst = forms.ChoiceField(widget=forms.Select(attrs={'class':'input-mediun ttip_r','id':'kode_inst',
        'onchange':'choose_kri()','title':'Langkah Pertama Penginputan'}),choices=BANK_KREDIT_CHOICES)
    tglinput = forms.DateField(widget=forms.DateInput(attrs={'class':'input-small ',
        'readonly':True,'onblur':'masker cekusia_baru','id':'tglinput'},format="%d-%m-%Y"))
    tgllahir =forms.DateField(widget=forms.TextInput(attrs={'class':'input-small ttip_r','placeholder':'DD-MM-YYYY',
        'id':'tgllahir','onblur':'masker cekusia_baru','onchange':'','title':'Langkah Kedua'}))
    thnusia =forms.IntegerField(label='Usia',widget=forms.TextInput(attrs={'alt':'integer','readonly':'True',
        'class':'input-small','id':'thnusia'}))
    blnusia = forms.IntegerField(label='Usia',widget=forms.TextInput(attrs={'alt': 'integer','readonly':'True',
        'class':'input-small','id':'blnusia'}))
    hariusia = forms.IntegerField(label='Usia',widget=forms.TextInput(attrs={'alt': 'integer','readonly':'True',
        'class':'input-small','id':'hariusia'}))
    min_usia = forms.IntegerField(label='Usia',widget=forms.HiddenInput(attrs={'alt': 'integer',
        'class':'input-small','id':'min_usia'}))
    max_usia = forms.IntegerField(label='Usia',widget=forms.HiddenInput(attrs={'alt': 'integer',
        'class':'input-small','id':'max_usia'}))
    produk = forms.ModelChoiceField(queryset=Produk.objects.all(),
        widget=forms.Select(attrs={'onchange':'cek_usia_form();id_kos()','onblur':'cek_usia_form()','id':'produk',
            'class':'ttip_t','title':'Langkah Kelima'}))
    pers_max = forms.IntegerField(widget=forms.TextInput(attrs={'alt': 'integer','readonly':'True',
        'class':'uang input-small','id':'pers_max'}))#####DSR
    id_param = forms.IntegerField(widget=forms.TextInput(attrs={'alt': 'integer','readonly':'True',
        'class':'uang input-small ttip_r','id':'id_param','title':'Kode Produk'}))#####ID PARAMETER
    gajibersih= forms.IntegerField(widget=forms.TextInput(attrs={'size': 9,'class':'uang ttip_t input-small','alt': 'integer',
        'onblur':"maks_angsuran();plafon()",'id':'gajibersih','placeholder':'Gaji Bersih',
        'title':'Langkah Ke Enam'}),required =False)
    angs_max = forms.IntegerField(widget=forms.TextInput(attrs={'size': 9,'class':'input-small ttip_t',
        'alt':'integer','id':'angs_max','readonly':True,'placeholder':'Max Angsuran'}),required =False)
    status_pensiun = forms.ChoiceField(widget=forms.Select(attrs={'class':'ttip_r','title':'Langah Ke tiga','onchange':'id_dkos()'}),
        choices= JENIS_PENSIUN,required = False)
    jenis_pengajuan = forms.ChoiceField(widget=forms.Select(attrs={'class':'ttip_r','title':'Langah Keemmpat','onchange':'id_dkos()'}),
        choices=JENIS_PENGAJUAN,required = False)
    tenormaks =forms.IntegerField(widget=forms.TextInput(attrs={'alt': 'integer','readonly':'True',
        'class':'uang input-small','id':'tenormaks','placeholder':'Tenor Max'}))
    plafonmax = forms.IntegerField(label="Plafon max",widget=forms.TextInput(attrs={'size': 9,'readonly':'True',
        'class':'uang input-medium ttip_r','alt':'integer','id':'plafonmax','oldtitle':'Plafoni Usul','placeholder':'Plafon Max'}))
    plafonusul = forms.IntegerField(label="Plafon Usul",widget=forms.TextInput(attrs={'size': 9,'id':'plafonusul',
        'class':'uang input-medium ttip_r','alt':'integer','onblur':'h_mutasi()',
        'title':'Langkah Ke Sembilan','placeholder':'Plafon Usulan','onkeyup':'cek_usul()'}))
    mutasi = forms.ChoiceField(widget=forms.Select(attrs={'class':'ttip_r','title':'Langah KeTujuh','onchange':'h_mutasi()'}),choices=MUTASI_CH)
    retensi =forms.ChoiceField(choices=RETENSI_CH,widget=forms.Select(attrs={'class':'input-small ttip_r',
        'title':'Langkah Ke Sepuluh','onchange':'validasi_retensi()'}))
    n_retensi = forms.IntegerField(widget=forms.TextInput(attrs={'size': 9,'readonly':'True',
        'class':'uang input-medium ttip_r','alt':'integer','oldtitle':'Nilai Retensi'}))
    kode_bank = forms.ChoiceField(choices=KODE_BANK,widget=forms.Select(attrs={'class':'input-small ttip_r',
        'title':'9','onchange':'h_mutasi()'}))