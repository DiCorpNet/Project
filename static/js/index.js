class Index {

    static initPaginator(){
        document.body.querySelectorAll('.pagination > li > a')
            .forEach(link => link.addEventListener('click', Index.pagination_link_clickHandler));
    }

    static pagination_link_clickHandler(event) {
        event.preventDefault();

        let path = event.target.href;
        let page = Global.getURLParameter(path,'page');

        if(typeof page !== 'undefined') {
            JQuery.ajax({
                url: JQuery(this).attr('action'),
                type: 'POST',
                data: {'page':getURLParameter(path, 'page')},
                success: function (json) {
                    if (json.result){
                        window.history.pushState({route: path}, 'NSP', path);
                        JQuery("#articles-list").replaceWith(articles);
                        Index.initPaginator();
                        JQuery(window).scrollTop(0);
                    }
                }
            })
        }
    }
}

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

Index.initPaginator();