$( document ).ready(function() {
        $(".conversation-list").scrollTop($(".conversation-list")[0].scrollHeight);
        $('#chattext').focus()
    });

let ws = ''
let message_list = document.querySelector('.conversation-list')


$(".chat-send").on('click', function (e){
    e.preventDefault();
    let message_input = $('#chattext');
    ws.send(JSON.stringify({
        'type': 'send',
        'message': message_input.val(),
        'username': user_in
    }));
    message_input.val('')
    $('#chattext').focus();
})

// Search User
$('#search-user').on('keyup', function(e){
    let search = $(this).val()
    let slist = document.getElementById('user-search-list')
    if((search != '') && (search.length > 3)){
        $('.search-to').fadeOut()
        slist.innerHTML = ''
        axios.get('/message/search-user/' + search + '/').then(response => {
            let user = response.data
            if(user.length != 0){
                for(i=0; user.length > i; i++){
                slist.innerHTML += '<li class="nav-item" value="'+ user[i].room +'">' +
                                    '       <div class="row">' +
                                    '           <div class="col-2">' +
                                    '               <img class="img-fluid rounded-circle" src="'+ user[i].image +'" alt="">' +
                                    '           </div>' +
                                    '           <div class="col-10" value="'+ user[i].username +'">' + user[i].username + '</div>' +
                                    '        </div>' +
                                    '</li>'
                }
                $('.search-to').fadeIn()
            }
        })
    }
})

 // Close search user
$('.close-search').on('click', function (e){
    $('.search-to').fadeOut()
})


// Create Dialog
$('#user-search-list').on('click', '.nav-item', function(e){
    let room = e.currentTarget.getAttribute('value')
    let toUser = e.currentTarget.lastElementChild.lastElementChild.getAttribute('value')
    create_room(room, toUser)
    $('.search-to').fadeOut()
})

// open dialog
$('.user-r').on('click', '.text-body' , function(e){
    e.preventDefault();
    let room = e.currentTarget.getAttribute('value')
    if(ws){
        if(ws.url){
            let webs = ws.url.split('/')
            if(room != webs[4]){
                ws.close()
                connectWS(room)
            }
        }
    }else{
        connectWS(room)
    }
    $(".conversation-list").animate({ scrollTop: 20000000 }, "slow");
})


// Open websocket
function connectWS(room){
    ws = new WebSocket('ws://' + window.location.host + '/ws/' + room + '/')

    ws.onopen = function (e){
        ws.send(JSON.stringify({
            'type': 'open'
        }));
        $(".conversation-list").animate({ scrollTop: 20000000 }, "slow");
        console.log('Connection Established')
    }

    ws.onmessage = function (e){
        let data = JSON.parse(e.data)
        switch (data.type){
            case 'open':
                OpenRoomData(data.data);
                OpenUserRoom(data.userTo);
                break
            default:
                GetMessage(data);
                break
        }
        $(".conversation-list").animate({ scrollTop: 20000000 }, "slow");
    }

    ws.onerror = function(e){
        message_list.innerHTML += '<div class="alert alert-info">Произошла ошибка! Попробуйте перезагрузить страницу или войти позже.</div>'
        console.log(e)
    }

    ws.onclose = function(e){
        console.log('Connect Close')
    }
}


function GetMessage(data){
    if(data.user == user_in){
        message_list.innerHTML += '<li class="clearfix odd" id="'+ data.id +'">' +
                                       ' <div class="chat-avatar">' +
                                            '<img src="'+ data.user_image +'" alt="dominic" class="rounded" />' +
                                            '<i>'+ data.created +'</i>' +
                                        '</div>' +
                                        '<div class="conversation-text">' +
                                            '<div class="ctext-wrap">' +
                                                '<i>' + data.user_in +'</i>' +
                                                '<p>' + data.message + '</p>' +
                                           ' </div>' +
                                        '</div>' +
                                        '<div class="conversation-actions dropdown">' +
                                            '<button class="btn btn-sm btn-link" data-bs-toggle="dropdown"aria-expanded="false"><i class="uil uil-ellipsis-v"></i></button>' +
                                            '<div class="dropdown-menu">' +
                                                '<a class="dropdown-item" href="#">Copy Message</a>' +
                                                '<a class="dropdown-item" href="#">Edit</a>' +
                                               ' <a class="dropdown-item" href="#">Delete</a>' +
                                            '</div>' +
                                        '</div>' +
                                    '</li>'
    }else {
        message_list.innerHTML += '<li class="clearfix" id="'+ data.id +'">' +
                                       ' <div class="chat-avatar">' +
                                            '<img src="'+ data.user_image +'" alt="dominic" class="rounded" />' +
                                            '<i>'+ data.created +'</i>' +
                                        '</div>' +
                                        '<div class="conversation-text">' +
                                            '<div class="ctext-wrap">' +
                                                '<i>' + data.user_in +'</i>' +
                                                '<p>' + data.message + '</p>' +
                                           ' </div>' +
                                        '</div>' +
                                        '<div class="conversation-actions dropdown">' +
                                            '<button class="btn btn-sm btn-link" data-bs-toggle="dropdown"aria-expanded="false"><i class="uil uil-ellipsis-v"></i></button>' +
                                            '<div class="dropdown-menu">' +
                                                '<a class="dropdown-item" href="#">Copy Message</a>' +
                                                '<a class="dropdown-item" href="#">Edit</a>' +
                                               ' <a class="dropdown-item" href="#">Delete</a>' +
                                            '</div>' +
                                        '</div>' +
                                    '</li>'
    }
}

function OpenUserRoom(item){
    document.getElementById('u-info').innerHTML = '<div class="card">\n' +
            '                                    <div class="card-body">\n' +
            '                                        <div class="dropdown float-end">\n' +
            '                                            <a href="#" class="dropdown-toggle arrow-none card-drop" data-bs-toggle="dropdown" aria-expanded="false">\n' +
            '                                                <i class="mdi mdi-dots-horizontal"></i>\n' +
            '                                            </a>\n' +
            '                                            <div class="dropdown-menu dropdown-menu-end">\n' +
            '                                                <!-- item-->\n' +
            '                                                <a href="javascript:void(0);" class="dropdown-item">View full</a>\n' +
            '                                                <!-- item-->\n' +
            '                                                <a href="javascript:void(0);" class="dropdown-item">Edit Contact Info</a>\n' +
            '                                                <!-- item-->\n' +
            '                                                <a href="javascript:void(0);" class="dropdown-item">Remove</a>\n' +
            '                                            </div>\n' +
            '                                        </div>\n' +
            '\n' +
            '                                        <div class="mt-3 text-center">\n' +
            '                                            <img src="'+ item[0].image +'" alt="shreyu"\n' +
            '                                                class="img-thumbnail avatar-lg rounded-circle" />\n' +
            '                                            <h4>'+ item[0].username +'</h4>\n' +
            '                                            <button class="btn btn-primary btn-sm mt-1"><i class=\'uil uil-envelope-add me-1\'></i>Send Email</button>\n' +
            '                                            <p class="text-muted mt-2 font-14">Last Interacted: <strong>Few hours back</strong></p>\n' +
            '                                        </div>\n' +
            '\n' +
            '                                        <div class="mt-3">\n' +
            '                                            <hr class="" />\n' +
            '\n' +
            '                                            <p class="mt-4 mb-1"><strong><i class=\'uil uil-at\'></i> Email:</strong></p>\n' +
            '                                            <p>'+ item[0].email +'</p>\n' +
            '\n' +
            '                                            <p class="mt-3 mb-1"><strong><i class=\'uil uil-location\'></i> Location:</strong></p>\n' +
            '                                            <p>'+ item[0].country +'</p>\n' +
            '\n' +
            '                                            <p class="mt-3 mb-1"><strong><i class=\'uil uil-globe\'></i> Languages:</strong></p>\n' +
            '                                            <p>'+ item[0].location +'</p>\n' +
            '\n' +
            '                                            <p class="mt-3 mb-2"><strong><i class=\'uil uil-users-alt\'></i> Groups:</strong></p>\n' +
            '                                            <p>\n' +
            '                                                <span class="badge badge-success-lighten p-1 font-14">Work</span>\n' +
            '                                                <span class="badge badge-primary-lighten p-1 font-14">Friends</span>\n' +
            '                                            </p>\n' +
            '                                        </div>\n' +
            '                                    </div> <!-- end card-body -->\n' +
            '                                </div>'
}


function OpenRoomData(data){
    for(i = data.length - 1; i >= 0; i--){
                if(data[i].user == data[i].user_in){
                message_list.innerHTML += '<li class="clearfix odd" id="'+ data[i].id +'">' +
                                               ' <div class="chat-avatar">' +
                                                    '<img src="'+ data[i].user_image +'" alt="dominic" class="rounded" />' +
                                                    '<i>'+ data[i].created +'</i>' +
                                                '</div>' +
                                                '<div class="conversation-text">' +
                                                    '<div class="ctext-wrap">' +
                                                        '<i>' + data[i].user_in +'</i>' +
                                                        '<p>' + data[i].text + '</p>' +
                                                   ' </div>' +
                                                '</div>' +
                                                '<div class="conversation-actions dropdown">' +
                                                    '<button class="btn btn-sm btn-link" data-bs-toggle="dropdown"aria-expanded="false"><i class="uil uil-ellipsis-v"></i></button>' +
                                                    '<div class="dropdown-menu">' +
                                                        '<a class="dropdown-item" href="#">Copy Message</a>' +
                                                        '<a class="dropdown-item" href="#">Edit</a>' +
                                                       ' <a class="dropdown-item" href="#">Delete</a>' +
                                                    '</div>' +
                                                '</div>' +
                                            '</li>'
            }else{
                message_list.innerHTML += '<li class="clearfix" id="'+ data[i].id +'">' +
                                               ' <div class="chat-avatar">' +
                                                    '<img src="'+ data[i].user_image +'" alt="dominic" class="rounded" />' +
                                                    '<i>'+ data[i].created +'</i>' +
                                                '</div>' +
                                                '<div class="conversation-text">' +
                                                    '<div class="ctext-wrap">' +
                                                        '<i>' + data[i].user +'</i>' +
                                                        '<p>' + data[i].text + '</p>' +
                                                   ' </div>' +
                                                '</div>' +
                                                '<div class="conversation-actions dropdown">' +
                                                    '<button class="btn btn-sm btn-link" data-bs-toggle="dropdown"aria-expanded="false"><i class="uil uil-ellipsis-v"></i></button>' +
                                                    '<div class="dropdown-menu">' +
                                                        '<a class="dropdown-item" href="#">Copy Message</a>' +
                                                        '<a class="dropdown-item" href="#">Edit</a>' +
                                                       ' <a class="dropdown-item" href="#">Delete</a>' +
                                                    '</div>' +
                                                '</div>' +
                                            '</li>'
            }
         }
         $('#message-input').fadeIn()
}


// Functions
function create_room(room, toUser){
    axios.post(
        '/message/create-room/',
        {
            room: room,
            userto: toUser
        },
        {
           headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': csrftoken,
        }
        }).then(res=>{
            console.log(res.data)
    })
}
