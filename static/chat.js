// chat.js
$(document).ready(function() {
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

    socket.on('message', function(msg) {
        if (msg.html) {
            $('#messages').append($('<li>').html(msg.data));
        } else {
            $('#messages').append($('<li>').text(msg));
        }
    });

    $('#sendButton').click(function() {
        socket.send($('#myMessage').val());
        $('#myMessage').val('');
        return false;
    });

    $('#analyzeButton').click(function() {
        socket.send('analyze: ' + $('#myMessage').val());
        $('#myMessage').val('');
        return false;
    });

    // Ensures the message box scrolls to the bottom for each new message
    var messageBox = $('#messages');
    var scrollDown = function() {
        messageBox.scrollTop(messageBox.prop('scrollHeight'));
    };
    socket.on('message', scrollDown);
});
