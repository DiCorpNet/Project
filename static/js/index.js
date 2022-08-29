class Index {

    static initPaginator(){
        document.body.querySelectorAll('.pagination > li > a')
            .forEach(link => link.addEventListener('click', Index.pagination_link_clickHandler));
    }

    static pagination_link_clickHandler(event) {
        event.preventDefault();

        let path = event.target.href;
        let page = getURLParameter(path,'page');

        if(typeof page !== 'undefined') {
            axios.post(
                $(this)[0].href,
                {
                    page:getURLParameter(path, 'page'),
                },
                {
                    headers: {
                        'X-CSRFToken': csrftoken,
                    },
                    onUploadProgress: progressEvent => {
                        // loader();
                        console.log('Start Upload')
                    },
                    onDownloadProgress: progressEvent => {
                        console.log('End Upload')
                    }
                }
                ).then(res => {
                           if (res.data.result){
                                window.history.pushState({route: path}, 'NSP', path);
                                $("#articles-list").html(res.data.articles);
                                Index.initPaginator();
                                // $(window).scrollTop(0);
                               $("body,html").animate({scrollTop: 0}, 800)
                            }
            })
            // $.ajax({
            //     url: $(this).attr('action'),
            //     type: 'POST',
            //     data: {'page':getURLParameter(path, 'page'), 'csrfmiddlewaretoken': csrftoken},
            //     success: function (json) {
            //         if (json.result){
            //             window.history.pushState({route: path}, 'NSP', path);
            //             $("#articles-list").html(json.articles);
            //             Index.initPaginator();
            //             $(window).scrollTop(0);
            //         }
            //     }
            // })
        }
    }
}
Index.initPaginator();

function getURLParameter(sUrl, sParam) {
    let sPageURL = sUrl.substring(sUrl.indexOf('?') + 1);
    let sURLVariables = sPageURL.split('&');
    for (let i = 0; i < sURLVariables.length; i++) {
        let sParameterName = sURLVariables[i].split('=');
        if (sParameterName[0] == sParam) {
            return sParameterName[1];
        }
    }
}

// function loader(){
//     let height = $('#articles-list').height()
//     let widht = $('#articles-list').outerWidth() - 20
//     $('.loader').css({"height": height, 'width': widht})
//     console.log(height, widht)
// }


