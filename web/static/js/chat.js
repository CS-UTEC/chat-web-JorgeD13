function sendMessage(){
    alert("Heyyyy");
}

function get_current(){
    $('#messages').empty();
    console.log("Voy a traer a este usuario");
    $.getJSON("/current", function(data){
        console.log(data['username'])
        var div = '<div><span>username</span></div>';
        div = div.replace('username', data['username']);
        $('#contacts').append(div);
        get_users(data['id']);
    });
}

function get_users(user_from_id){
    $('#messages').empty();
    console.log("Voy a traer todos los usuarios");
    $.getJSON("/users", function(data){
        console.log(data);
        var i = 0;
        $.each(data, function(){
            let vari = '<div class="btn btn-secondary" onclick = "get_messages(user_from_id, user_to_id)"> <span>username: </span><span>name</span></div>';
            vari = vari.replace('username', data[i]['username']);
            vari = vari.replace('name', data[i]['name']);
            vari = vari.replace('user_to_id', data[i]['id']);
            vari = vari.replace('user_from_id', user_from_id);
            console.log(vari);
            $("#Contacts").append(vari);
            i = i+1;
        });
    });
}


function get_messages(user_from, user_to){
    $('#messages').empty();
    $.getJSON("/messages/" + user_from + "/" + user_to, function(data){
        let i = 0;
        $.each(data, function(){
            let div = '<div>content</div>';
            div = div.replace('content', data[i]['content']);
            $("#messages").append(div);
            i = i+1;
        });
    });
}
/*
function send_messages(user_from, user_to){
    $('#sending').empty();
    $.getJSON("/messages", function(data){
        let div = <div>Content</div>
        
    });
}*/