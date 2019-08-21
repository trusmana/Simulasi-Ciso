from django.shortcuts import render
from .forms import SimulasiForm
import datetime,math
from decimal import *
from django.http import JsonResponse,HttpResponse
from paramkredit.models import ParameterPencairan
from django.template.loader import render_to_string
from dateutil.relativedelta import *
from dateutil import parser
from django.contrib.auth.decorators import login_required

def save_simulasi_form(request, h_ajax, template_name):
    data = dict()
    context = {'h_ajax': h_ajax}
    #data['mymodal'] = render_to_string('index_list.html')
    data['django_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)
@login_required
def show_simulasi(request):
    j_aju = request.GET.get('j_aju',None)
    produk = request.GET.get('produk',None)
    s_pens = request.GET.get('sts_pens', None)
    inst = request.GET.get('kantor_bayar', None)
    param = request.GET.get('param', None)
    tenor = request.GET.get('tenor', None)
    plafon = request.GET.get('plafond', None)
    flatbln = request.GET.get('flatbln', None)
    tgllahir = request.GET.get('tgllahir', None)
    retensi = request.GET.get('retensi',None)
    mutasi = request.GET.get('mutasi',None)
    hs_param = ParameterPencairan.objects.get(pk=param)
    provisi = Decimal(plafon) * (Decimal(hs_param.provisi))
    adm = Decimal(plafon) * (Decimal(hs_param.adm))
    adm_provisi = provisi + adm
    ang_pokok = int(plafon) / int(tenor)
    ang_bunga = Decimal(plafon) * ((Decimal(hs_param.bunga)) / Decimal(12));
    tgl = parser.parse(tgllahir).date()
    h_asuransi = load_usialunas(tgl,tenor,param,plafon,hs_param)   
    asumsi_jtempo = datetime.date.today() + relativedelta(months=+(int(tenor)))
    cek = asumsi_jtempo - tgl
    u_lunas= cek.days / 365
    if int(mutasi) == int(2):
        mt = 150000
    else:
        mt = 0
    terima_bersih = Decimal(plafon) - Decimal(adm_provisi) - Decimal(h_asuransi) - Decimal(retensi) - Decimal(mt)
    if hs_param.produk.id_prod == 1:
        angsuran = hs_param.angsuran_anuitas(int(plafon),int(tenor))
    else:
        angsuran = ang_pokok + ang_bunga
    h_ajax ={'hs_param':param,'bunga':(hs_param.bunga * 100),'tgl':datetime.date.today(),'tenor':tenor,\
        'plafon':plafon,'angsuran':angsuran,'adm_provisi':adm_provisi,'tb':terima_bersih,'asuransi':h_asuransi,
        'retensi':retensi,'h_mt':mt,'tgl_lahir':tgllahir,'param':param,'kb':inst,'s_pens':s_pens,
        'j_aju':j_aju,'produk':produk}
    return save_simulasi_form(request, h_ajax, 'create_simulasi.html')



def load_usialunas(tgl,tenor,param,plafon,hs_param):
    asumsi_jtempo = datetime.date.today() + relativedelta(months=+(int(tenor)))
    cek = asumsi_jtempo - tgl
    u_lunas= cek.days / 365
    print hs_param.produk.id_prod,type(hs_param.produk.id_prod)
    if hs_param.produk.id_prod == 1 and u_lunas < 65 :
        rate =float(0.0065) * float(plafon) * math.ceil(Decimal((tenor))/Decimal((12)))
    elif hs_param.produk.id_prod == 1 and u_lunas >= 65:
        rate = float(0.008) * float(plafon) * math.ceil(Decimal((tenor))/Decimal((12)))
    elif hs_param.produk.id_prod != 1 and int(tenor) <= 12:
        rate = float(0.06) * float(plafon) 
    elif hs_param.produk.id_prod != 1 and int(tenor) >= 13 and int(tenor) <= 24:
        rate = float(0.12) * float(plafon) 
    elif hs_param.produk.id_prod != 1 and int(tenor) >= 25 and int(tenor) <= 36:
        rate = float(0.15) * float(plafon) 
    elif hs_param.produk.id_prod != 1 and int(tenor) >= 37 and int(tenor) <= 48 :
        rate = float(0.16) * float(plafon) 
    elif hs_param.produk.id_prod != 1 and int(tenor) >= 49 and int(tenor) <= 60 :
        rate = float(0.19) * float(plafon) 
    return rate

def hitung_mutasi(request):
    if request.is_ajax():
        param = request.GET.get('param', None)
        tenor = request.GET.get('tenor', None)
        plafon = request.GET.get('plafond', None)
        mutasi = request.GET.get('mutasi',None)
        ang_pokok = int(plafon) / int(tenor)
        hs_param = ParameterPencairan.objects.get(pk=param)
        ang_bunga = Decimal(plafon) * ((Decimal(hs_param.bunga)) / Decimal(12));
        sts_mutasi = int(mutasi)
        if sts_mutasi == int(2) and hs_param.produk.id_prod == 1:
            angsuran = hs_param.angsuran_anuitas(int(plafon),int(tenor))
            result = '2'
            data = {'result':result,'retensi':2,'n_retensi':(angsuran * 2)}
            return HttpResponse(JsonResponse(data))
        elif sts_mutasi == int(2) and hs_param.produk.id_prod != 1:
            angsuran = ang_pokok + ang_bunga
            result = '2'
            data = {'result':result,'retensi':2,'n_retensi':(angsuran * 2)}
            return HttpResponse(JsonResponse(data))
        else:
            angsuran = hs_param.angsuran_anuitas(int(plafon),int(tenor))
            result ='1'
            data = {'result':result,'n_retensi':0}
            return HttpResponse(JsonResponse(data))
    else:
        data = {'result':0,'tenor_maks':0,'dsr':0,'id_param':0}
    return HttpResponse(JsonResponse(data))

def val_retensi(request):
    if request.is_ajax():
        retensi = request.GET.get('retensi', None)
        mutasi = request.GET.get('mutasi', None)
        param = request.GET.get('param', None)
        tenor = request.GET.get('tenor', None)
        plafon = request.GET.get('plafond', None)
        ang_pokok = int(plafon) / int(tenor)
        hs_param = ParameterPencairan.objects.get(pk=param)
        ang_bunga = Decimal(plafon) * ((Decimal(hs_param.bunga)) / Decimal(12));
        sts_mutasi = mutasi
        if sts_mutasi == 1 and hs_param.produk.id_prod != 1:
            angsuran = ang_pokok + ang_bunga
            result = '1'
            data = {'result':result,'retensi':0,'n_retensi':(angsuran * Decimal(retensi))}
            return HttpResponse(JsonResponse(data))
        elif sts_mutasi == 2 and retensi == '1':
            angsuran = hs_param.angsuran_anuitas(int(plafon),int(tenor))
            result = '2'
            data = {'result':result,'retensi':2,'n_retensi':(angsuran * Decimal(1))}
            return HttpResponse(JsonResponse(data))
        elif sts_mutasi == 2 and retensi != '1' and hs_param.produk.id_prod == 1:
            angsuran = ang_pokok + ang_bunga 
            result = '3'
            data = {'result':result,'retensi':2,'n_retensi':(angsuran * Decimal(retensi))}
            return HttpResponse(JsonResponse(data))
        else:
            angsuran = hs_param.angsuran_anuitas(int(plafon),int(tenor))
            result = '3'
            data = {'result':result,'retensi':2,'n_retensi':(angsuran * Decimal(retensi))}
            return HttpResponse(JsonResponse(data))
    else:
        data = {'result':0}
    return HttpResponse(JsonResponse(data))

@login_required
def index(request):
    sekarang = datetime.date.today()
    form = SimulasiForm(initial={'tglinput':sekarang,'min_usia':'40',
        'max_usia':'80'})
    return render(request, 'index.html',{'form':form})

def cek_usia(request):
    data = {'result':0,'tenor_maks':0,'dsr':0,'id_param':0}
    if request.is_ajax():
        usia = request.GET.get('usia', None)
        bulan = request.GET.get('bulan', None)
        hari = request.GET.get('hari',None)
        kode_inst = request.GET.get('kode_inst',None)
        produk = request.GET.get('produk',None)
        sts_pens = request.GET.get('sts_pens',None)
        j_aju = request.GET.get('j_aju',None)
        kode_bank = request.GET.get('kode_bank',None)
        param= ParameterPencairan.objects.filter(produk__id =produk,kantor_bayar=kode_inst,kode_bank= kode_bank,
            min_usia__lte=usia,max_usia__gt=usia,status_pensiun=sts_pens,jenis_pengajuan=j_aju)
        print param
        for htg in param:
            ten_tahun = (htg.max_usia - 1) - int(usia)
            ten_bulan = htg.max_bulan_usia - int(bulan)
            tenor= ((ten_tahun * 12)+(ten_bulan) - 1)
            if tenor >= htg.max_tenor:
                jw = htg.max_tenor
            else:
                jw = tenor
            dsr = (htg.dsr)
            result = '1'
            data = {'result':result,'tenor_maks':jw,'dsr':dsr,'id_param':htg.id}
            return HttpResponse(JsonResponse(data))
    else:
        data = {'result':0,'tenor_maks':0,'dsr':0,'id_param':0}
    return HttpResponse(JsonResponse(data))


def maks_plafond(request):
    data = {'result' : 0,'flattahun': 0,'flatbulan': 0,'effektif': 0}
    if request.is_ajax():
        usia = request.GET.get('usia', None)
        kode_inst = request.GET.get('kode_inst',None)
        produk = request.GET.get('produk',None)
        sts_pens = request.GET.get('sts_pens',None)
        j_aju = request.GET.get('j_aju',None)
        gaji= request.GET.get('gaji',None)
        tenor = request.GET.get('tenor',None)
        param= ParameterPencairan.objects.filter(produk__id=produk,kantor_bayar=kode_inst,
            min_usia__lte=usia,max_usia__gt=usia,status_pensiun=sts_pens,jenis_pengajuan=j_aju)
        for htg in param:

            if htg.produk.id_prod == 1:
                d_efek = efektifkeflat(htg,tenor)
                flatbl = round(d_efek/12,6)
            else:
                flatbl = htg.bunga/12

            plafon1 = 1 * (int(tenor))  * (0.9) * int(gaji)
            plafon2 = 1 + ((flatbl) * int(tenor))
            plafond = Decimal(plafon1)/Decimal(plafon2)

            if plafond > htg.max_plafon:
                h_plafon = htg.max_plafon
                result = 1
                flatbulan = flatbl
                flattahun = 10
                effektif = 10
            else:
                h_plafon = plafond
                flatbulan = flatbl
                flattahun = 10
                effektif = 10
                result = 1
            data = {'plafond':h_plafon,'result':result,'flatbulan':flatbulan,'flattahun':flattahun,'effektif':effektif}
            return HttpResponse(JsonResponse(data))
    else:
        return HttpResponse(JsonResponse(data))

def efektifkeflat(htg,tenor):
    tn = int(tenor)
    kons = 100000000
    data_bg = Decimal(Decimal(htg.bunga) * Decimal(100))
    bng = data_bg / 1200
    Y = pow((bng + 1 ), 0)
    z = pow((bng + 1), (-tn))
    X = ((1 - z) * Y)
    YY = (bng / X)
    XX = tn * YY
    zz = kons * XX
    XXX = ((zz - kons) / kons)
    hasil = (XXX / tn *12)
    return hasil
