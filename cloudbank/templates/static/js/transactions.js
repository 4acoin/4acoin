var socket = null;
var isopen = false;

window.onload = function() {

   //socket = new WebSocket("ws://{{ip}}:9000");
   socket.binaryType = "arraybuffer";

   socket.onopen = function() {
      console.log("Connected!");
      isopen = true;
   }

   socket.onmessage = function(e) {
     console.log(e);
      if (typeof e.data == "string") {
         console.log("Text message received: " + e.data);
      } else {
         var arr = new Uint8Array(e.data);
         var hex = '';
         for (var i = 0; i < arr.length; i++) {
            hex += ('00' + arr[i].toString(16)).substr(-2);
         }
         console.log("Binary message received: " + hex);
      }
   }

   socket.onclose = function(e) {
      console.log("Connection closed.");
      socket = null;
      isopen = false;
   }
};



function sendBinary() {
   if (isopen) {
       console.log("Bınaryy .");
       var bson = new BSON();
       console.log(bson);

      x = {"server":false,"message":"hello everyone"}



       var buf = bson.serialize(x)
     console.log(buf);
      socket.send(buf);
      console.log("Binary message sent.");
   } else {
      console.log("Connection not opened.")
   }
};
