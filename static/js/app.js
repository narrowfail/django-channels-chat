let currentRecipient = '';
let chatInput = $('#chat-input');
let chatButton = $('#btn-send');
let userList = $('#user-list');
let messageList = $('#messages');

function updateUserList() {
    $.getJSON('api/v1/user/', function (data) {
        userList.children('.user').remove();
        for (let i = 0; i < data.length; i++) {
            const userItem = `<a class="list-group-item user">${data[i]['username']}</a>`;
            $(userItem).appendTo('#user-list');
        }
        $('.user').click(function () {
            userList.children('.active').removeClass('active');
            let selected = event.target;
            $(selected).addClass('active');
            setCurrentRecipient(selected.text);
        });
    });
}

function drawMessage(message) {
    let position = 'left';
    const date = new Date(message.timestamp);
    if (message.user === currentUser) position = 'right';
    let messageItem="";
    if(message.body && !(message.image || message.file))
    {
        messageItem = `
            <li class="message ${position}">
                <div class="avatar">${message.user}</div>
                    <div class="text_wrapper">
                        <div class="text">${message.body}<br>
                            <span class="small">${date}</span>
                            <span class="small">${message.is_read}</span>
                        </div>
                    </div>
                </div>
            </li>`;    
    }
    else if(message.image)
    {
        messageItem = `
            <li class="message ${position}">
                <div class="avatar">${message.user}</div>
                    <div class="text_wrapper">
                        <a target="_blank" href="`+message.image+`">
                          <img src="`+message.image+`" height="100%" width="100%" />
                        </a>
                        <br>
                        <span class="small">${date}</span>
                    </div>
                </div>
            </li>`;
    }
    else if(message.file)
    {
        messageItem = `
            <li class="message ${position}">
                <div class="avatar">${message.user}</div>
                    <div class="text_wrapper">
                        <a target="_blank" href="`+message.file+`">
                           <iframe width= "100px" height="100px" src="`+message.file+`">
                            </iframe>                        
                        </a>
                        <br>
                        <span class="small">${date}</span>
                    </div>
                </div>
            </li>`;   
    }
    $(messageItem).appendTo('#messages');
}

function getConversation(recipient) {
    $.getJSON(`/api/v1/message/?target=${recipient}`, function (data) {
        messageList.children('.message').remove();
        for (let i = data['results'].length - 1; i >= 0; i--) {
            drawMessage(data['results'][i]);
        }
        $.ajax({
          type:'POST',
          url:'read/',
          data:{
            user:recipient,
          },
          dataType:"json",
        });
        messageList.animate({scrollTop: messageList.prop('scrollHeight')});
    });

}

function getMessageById(message) {
    id = JSON.parse(message).message
    $.getJSON(`/api/v1/message/${id}/`, function (data) {
        if (data.user === currentRecipient ||
            (data.recipient === currentRecipient && data.user == currentUser)) {
            drawMessage(data);
        }
        messageList.animate({scrollTop: messageList.prop('scrollHeight')});
    });
}

function sendMessage(recipient,body, image, file) {
    $.post('/api/v1/message/', {
        recipient: recipient,
        body: body,
        image: image,
        file: file,

    }).fail(function (response) { 
        alert('Error: ' + response.responseText);
    });
}


function setCurrentRecipient(username) {
    currentRecipient = username;
    getConversation(currentRecipient);
    enableInput();
}


function enableInput() {
    chatInput.prop('disabled', false);
    chatButton.prop('disabled', false);
    chatInput.focus();
}

function disableInput() {
    chatInput.prop('disabled', true);
    chatButton.prop('disabled', true);
}

$(document).ready(function () {
    updateUserList();
    disableInput();

//    let socket = new WebSocket(`ws://127.0.0.1:8000/?session_key=${sessionKey}`);
    var socket = new WebSocket(
        'ws://' + window.location.host +
        '/ws?session_key=${sessionKey}')


    document.getElementById("xxxx").addEventListener("change", readFile);
    function readFile() 
    {
        var fileTypes = ['pdf','doc', 'docx','txt'];
        let file = this.files[0];
        var extension = file.name.split('.').pop().toLowerCase();
        isfile = fileTypes.indexOf(extension) > -1;
        if(isfile)
        {
            let reader = new FileReader();
            reader.readAsDataURL(file);
            reader.onload = function() 
            {
                sendMessage(currentRecipient,"","", reader.result);
            }
        }
        else
        {
            let reader = new FileReader();
            reader.readAsDataURL(file);
            reader.onload = function() 
            {
                sendMessage(currentRecipient,"",reader.result,"");
            }
        }
        
    }

    chatInput.keypress(function (e) {
        if (e.keyCode == 13)
            chatButton.click();
    });

    chatButton.click(function () {
        if (chatInput.val().length > 0) {
            sendMessage(currentRecipient, chatInput.val(),"","");
            chatInput.val('');
        }
    });

    socket.onmessage = function (e) {
        getMessageById(e.data);
    };
});



