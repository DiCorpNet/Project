$('.reply').on('click',function (e) {
    e.preventDefault();
    var parentId = $(this).attr('data-id')
    var author = $(this).attr('data-author')
    var auth = $('#auth')
    $('#auth>strong').html(author)
    auth.fadeIn()
    $('#id_parent_comment').val(parentId)
    $('html, body').animate({
        scrollTop: $('#com').offset().top
    },{
        duration: 400,
        easing: "linear"
    })
})

$('#closed-reply').on('click', function (e){
    e.preventDefault()
    $('#auth').fadeOut(10)
    $('#auth>strong').html('')
    $('#id_parent_comment').val("")
})

$('#comfile').on('click', function (e){
    e.preventDefault()
    $('#id_file').click()
    $('#id_file').change(function (){
        var file =  document.getElementById('id_file').files[0]
        $('.previev').fadeIn()
        $('.previev').children('span').html(file.name)

    })
})

$('#clearComFile').on('click', function (e){
    e.preventDefault()
    $('.previev').fadeOut(function (){
        $('.previev').children('span').html('')
    })
    $('#id_file').remove()

})