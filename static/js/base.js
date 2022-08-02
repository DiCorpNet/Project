$('.like').on('click', function(e){
    e.preventDefault()
    let article_id = $(this).attr('data-id')
    axios.post('/api/likes/'+ article_id +'/article/', {
        'article': article_id
        },
        {
           headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': csrftoken
        }
        }
    ).then( response => {
        if(response.data.status){
            $(this).children('.mdi').addClass('text-danger')
        }else{
            $(this).children('.mdi').removeClass('text-danger')
        }

        $(this).children('span').html(response.data.count)
    })
})

$('.like-comment').on('click', function (e){
    let commentId = $(this).attr('data-id')
    axios.post('/api/likes/'+ commentId +'/comment/',
        {
            'comment': commentId,
        },
        {
           headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': csrftoken,
        }
        }
    ).then(response => {
        if(response.data.status){
            $(this).removeClass('text-muted').addClass('text-danger')
        }else{
            $(this).removeClass('text-danger').addClass('text-muted')
        }
        let res = $(this).children('span')
        res.html(response.data.count)
    })
})

$('[data-action="bookmark"]').on('click', function (e){
    e.preventDefault()
    let articleId = $(this).attr('data-id')
    axios.post('/api/bookmark/'+ articleId +'/article/', {
        'article': articleId
    },
     {
           headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': csrftoken,
        }
     }

        ).then(res => {
            if(res.data.status){
                    $(this).children('i').addClass('text-danger')
                }else{
                    $(this).children('i').removeClass('text-danger')
                }
            let resp = $(this).children('span')
            resp.html(res.data.count)
    })
})


$('#top-search').on('keyup', function (e){
            let search = $(this).val()
            if((search != '') && (search.length > 3)){
                axios.get('/api/search/?search=' +search).then(response => {
                    let data = response.data
                    document.getElementById('search-length').innerHTML = data.length
                    document.getElementById('noti-search').innerHTML =""
                    for(i=0; data.length > i; i++){
                        document.getElementById('noti-search').innerHTML += '<a href="'+ data[i].slug +'" class="dropdown-item notify-item">' +
                    '<div class="d-flex"> <img class="d-flex me-2" src="'+ data[i].image +'" alt="Generic placeholder image" height="32" width="65">' +
                    ' <div class="w-100"> <h5 class="m-0 font-14">'+ data[i].title +'</h5> </div> </div> </a>'
                    }
                })
            }
})

