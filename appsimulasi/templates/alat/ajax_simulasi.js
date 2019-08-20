<script>
function ceknilai(elem)
{
    $('#'+elem).keydown(function(event) {
    if (event.keyCode == 46 || event.keyCode == 8 || event.keyCode == 9 || event.keyCode == 27 || event.keyCode == 190 ||  
                 // Allow: Ctrl+A
                (event.keyCode == 65 && event.ctrlKey === true) || 
                 // Allow: home, end, left, right
                (event.keyCode >= 35 && event.keyCode <= 39) || event.keyCode==13) {
                     // let it happen, don't do anything
                     return;
            }
            else {
                // Ensure that it is a number and stop the keypress
                if ((event.keyCode < 48 || event.keyCode > 57) && (event.keyCode < 96 || event.keyCode > 105 )) {
                    event.preventDefault();
                    $('#'+elem).val(''); 
                }   
    };
    });
}
    
function cek_usia_form()
{
    var usia = $('#thnusia').val();
    var bulan = $('#blnusia').val();
    var hari = $('#hariusia').val();
    var tglinput = $('#tglinput').val();
    var produk = $('#produk').val();
    var sts_pens= $('#id_status_pensiun').val();
    var j_aju =$('#id_jenis_pengajuan').val();
    var kode_inst = $('#kode_inst').val();
    var kode_bank = $('#id_kode_bank').val()    
    var dataString = 'usia='+usia+'&produk='+produk+'&bulan='+bulan+'&hari='+hari+'&tglinput='+tglinput+'&kode_inst='+kode_inst+'&sts_pens='+sts_pens+'&j_aju='+j_aju+'&kode_bank='+kode_bank;
    $.ajax({
        url: "/cek_usia/",
        data: dataString,        
        dataType: "JSON",        
        success: function(data){            
    if(data.result=='1'){
         if(data.tenor_maks <= '0'){
             jAlert('Kriteria usia tidak memasuki persyaratan untuk produk ini!')                     
                 tenor_kosong()
                 $('#produk').val('')
                 return false;
         }else{
                 $('#tenormaks').val(data.tenor_maks);
                 $('#pers_max').val(data.dsr);
                 $('#id_param').val(data.id_param);
                 maks_angsuran()     
         }                                
    }else{
         jAlert('Perhatian:  Anda Memilih Produk Yang Salah !!!!')
                $('#produk').val('')
                tenor_kosong();
        return false;
        }
        }
    });   
}

function validasi_tenor()
{

    var tenormaks = parseFloat(to_number($("#tenormaks").val()))
    tahun =$('#tenor').val();
    
    if(tahun > tenormaks )
    {
        jAlert('Tenor Pengajuan Melebihi Tenor Maksimal');
        $('#tenor').val('');
        $('#tenor').focus();
    }
}

function cek_usul()
{

    var maksplafon = parseFloat(to_number($("#plafonmax").val()))
    var usul = parseFloat(to_number($("#plafonusul").val()))
    
    if(usul > maksplafon )
    {
        jAlert('Plafon Melebihi');
        $('#plafonusul').val('');
        $('#plafonusul').focus();
    }
}


function h_mutasi()
{
    var param = $('#id_param').val();
    var tenor = $('#tenor').val();
    var plafond = parseFloat(to_number($("#plafonusul").val()));
    var mutasi = $('#id_mutasi').val();

    var dataString ='param='+param+'&tenor='+tenor+'&plafond='+plafond+'&mutasi='+mutasi;
    $.ajax({
        url: "/hitung_mutasi/",
        data: dataString,        
        dataType: "JSON",        
        success: function(data){      
        if(data.result=='2'){
            $('#id_retensi').val(data.retensi);
            $('#id_n_retensi').val(format_number(String(Math.round(data.n_retensi))));
        }else{
            $('#id_retensi').val('');
            $('#id_n_retensi').val(format_number(String(Math.round(data.n_retensi))));
        }
        }
    });   

}

function validasi_retensi(){
    var mutasi = $('#id_mutasi').val();
    var retensi = $('#id_retensi').val();
    var param = $('#id_param').val();
    var tenor = $('#tenor').val();
    var plafond = parseFloat(to_number($("#plafonusul").val()));
    var dataString ='param='+param+'&tenor='+tenor+'&plafond='+plafond+'&mutasi='+mutasi+'&retensi='+retensi;    
    $.ajax({
        url: "/val_retensi/",
        data: dataString,
        dataType: "JSON",
        success: function(data){
        if(data.result == '1'){
            $('#id_n_retensi').val(format_number(String(Math.round(data.n_retensi))));

        }if(data.result == '2'){
            jAlert('Retensi Tidak Bisa 1 Kali Karna Mutasi');
            $('#id_retensi').val('2');
        }else{
            $('#id_n_retensi').val(format_number(String(Math.round(data.n_retensi))));

       }
    }
});
}


function maks_plafond()
{
    var gaji = parseFloat(to_number($("#gajibersih").val()));
    var usia = $('#thnusia').val();
    var produk = $('#produk').val();
    var kode_inst = $('#kode_inst').val();
    var sts_pens= $('#id_status_pensiun').val();
    var j_aju =$('#id_jenis_pengajuan').val();
    var tenor = $('#tenor').val();

    var dataString ='usia='+usia+'&produk='+produk+'&kode_inst='+kode_inst+'&sts_pens='+sts_pens+'&j_aju='+j_aju+'&gaji='+gaji+'&tenor='+tenor;
    $.ajax({
        url: "/maks_plafond/",
        data: dataString,        
        dataType: "JSON",        
        success: function(data){            
        $('#plafonmax').val(format_number(String(Math.round(data.plafond))));
            $('#flat_bln').val(data.flatbulan);
            $('#flat').val(data.flattahun);
            $('#effektif').val(data.effektif);
            //tenor_kosong();
        }
    });   
    
}




function choose_kri()
{
    $('#tenor').val('');
    $('#plafonusul').val('');
    $('#plafonmax').val('0');
}
function kosong()
{
    $('#jenis').val('');
}
function id_kos()
{
    $('#id_param').val('');
    $('#pers_max').val('');
    $('#tenormaks').val('')
}

function id_dkos()
{
    $('#id_param').val('');
    $('#pers_max').val('');
    $('#tenormaks').val('');
    $('#produk').val('');
   
}
function tenor_kosong()
{
    $('#tenor').val('');
    $('#plafonusul').val('');
    $('#angsuran').val('');
}
function kosongkan()
{
    $('#id_plafonmax').val('');
    $('#id_effektif').val('');
    $('#id_flat').val('');
    $('#plafonusul').val('0');
    $('#plafonmax').val('0');
}
</script>
