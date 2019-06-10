var namespace='/long_task';
var io = require('socket.io-client')('http://' + document.domain + ':' + "5000"+namespace);

io.on('connect', function() {
	console.log("Room Joining.....")
	io.emit('join_room_2', {'sid': '22222'});
});

export default io;