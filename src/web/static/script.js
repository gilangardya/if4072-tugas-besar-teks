function validateForm() {
    if ($("#ulasan").val() == "") {
        alert("Masukkan ulasanmu terlebih dahulu :)");
        return false;
    }
    return true;
}

$('document').ready(function() {
    // $('#result').css('display', 'none');

    $('#button-process').click(function() {
        if (!validateForm()) {
            return;
        }
        $('#button-process').attr('class', 'button is-primary is-rounded is-loading');
    
        var formData = new FormData();
        formData.append('nama', $('#nama').val());
        formData.append('ulasan', $('#ulasan').val());
        
        $.ajax({
            url : '/predict',
            type : 'POST',
            data : formData,
            processData: false,  // tell jQuery not to process the data
            contentType: false,  // tell jQuery not to set contentType
            success : function(data) {
                $('#result').css('display', 'block');
                $('.rate-off').css('display', 'inline-block');
                $('.rate-on').css('display', 'none');
                for (var i=1; i<=data.rating; i++) {
                    console.log('masuk');
                    $('#rate'+ i + '-off').css('display', 'none');
                    $('#rate'+ i + '-on').css('display', 'inline-block');
                }
            },
            error: function() {
                alert ('Oops, Something went wrong');
            },
            complete: function() {
                $('#button-process').attr('class', 'button is-primary is-rounded');
            }
        });
    });
});