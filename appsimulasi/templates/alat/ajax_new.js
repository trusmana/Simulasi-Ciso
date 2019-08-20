<script>
$(function () {

  var loadForm = function () {
    var btn = $(this);
    var usia = $('#thnusia').val();
    var bulan = $('#blnusia').val();
    var hari = $('#hariusia').val();
    var tgl_pengajuan = $('#tglinput').val();
    var sts_pens= $('#id_status_pensiun').val();
    var j_aju =$('#id_jenis_pengajuan').val();        
    var produk = $('#produk').val();
    var kantor_bayar = $('#kode_inst').val();    
    var gaji = $('#gajibersih').val();
    var tenor = parseFloat(to_number($('#tenor').val()));
    var plafond = parseFloat(to_number($('#plafonusul').val()));
    var retensi = parseFloat(to_number($("#id_n_retensi").val())); 
    var param =$('#id_param').val()
    var mutasi =$('#id_mutasi').val()
    var flatbln =$('#flat_bln').val()
    var tgllahir = $('#tgllahir').val()
    var dataString = 'gaji='+gaji+'&produk='+produk+'&kantor_bayar='+kantor_bayar+'&tenor='+tenor+'&usia='+usia+'&bulan='+bulan+'&hari='+hari+'&plafond='+plafond+'&tgl_pengajuan='+tgl_pengajuan+'&sts_pens='+sts_pens+'&j_aju='+j_aju+'&param='+param+'&flatbln='+flatbln+'&tgllahir='+tgllahir+'&retensi='+retensi+'&mutasi='+mutasi;
    $.ajax({
      url: btn.attr("data-url"),
      data: dataString,
      dataType: 'json',
      
      beforeSend: function () {
      $("#mymodal .modal-content").html("");
      $("#mymodal").modal("show");
      },
      success: function (data) {
      $("#mymodal .modal-content").html(data.django_form);
     } 
    });
  };

$(".js-show-hitung").click(loadForm);
});
</script>

