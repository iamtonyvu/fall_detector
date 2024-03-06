//const IMAGE_INTERVAL_MS = 1000;

function changeTitle(value) {
  document.getElementById("titleTime").innerHTML = value

}

function createResponse(data) {
  data.event.forEach(event => {
    if(chat.children.length > 0 && chat.children[0].clientHeight * (chat.children.length+2)  >= video.clientHeight){
      chat.removeChild(chat.lastElementChild)
    }
    var tag = document.createElement("div");
    tag.classList.add("message");
    tag.classList.add("row");
    var div =  document.createElement("div");
    div.classList.add("col-xd-12");
    div.classList.add("col-sm-10");
    div.classList.add("col-xl-12");
    var p = document.createElement("h2");
    var text
    if(data.type == 'alert'){
      text = document.createTextNode(" "+event.text);
    }else{
      text = document.createTextNode(" "+event.name);
    }
    p.appendChild(get_fa_incon(event.name))
    p.appendChild(text)
    p.style.color = 'rgb('+event.color.toString()+')';
    div.appendChild(p)
    tag.appendChild(div)
    var span = document.createElement("div");
    span.classList.add("col-xd-12");
    span.classList.add("col-sm-2");
    span.classList.add("col-xl-12");
    span.classList.add("time-right");
    var date = new Date()
    time = document.createTextNode(date.getHours().toLocaleString(undefined, {minimumIntegerDigits: 2})
    +':'+date.getMinutes().toLocaleString(undefined, {minimumIntegerDigits: 2})
    +':'+date.getSeconds().toLocaleString(undefined, {minimumIntegerDigits: 2}));
    span.appendChild(time)
    tag.appendChild(span)
    chat.insertBefore(tag, chat.childNodes[0]);
    //chat.appendChild(tag)
  });

}

function get_fa_incon(type) {
  var i = document.createElement("i");
  i.classList.add("fa-solid");
  switch (type) {
    case "Sitting":
      i.classList.add("fa-chair");
      break;
    case "Standing":
      i.classList.add("fa-person");
      break;
    case "Falling":
      i.classList.add("fa-person-falling");
      break;
    case "Alert":
        i.classList.add("fa-bell");
        break;

    default:
      break;
  }
  return i;
}

function encode (input) {
  var keyStr = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=";
  var output = "";
  var chr1, chr2, chr3, enc1, enc2, enc3, enc4;
  var i = 0;

  while (i < input.length) {
      chr1 = input[i++];
      chr2 = i < input.length ? input[i++] : Number.NaN; // Not sure if the index
      chr3 = i < input.length ? input[i++] : Number.NaN; // checks are needed here

      enc1 = chr1 >> 2;
      enc2 = ((chr1 & 3) << 4) | (chr2 >> 4);
      enc3 = ((chr2 & 15) << 2) | (chr3 >> 6);
      enc4 = chr3 & 63;

      if (isNaN(chr2)) {
          enc3 = enc4 = 64;
      } else if (isNaN(chr3)) {
          enc4 = 64;
      }
      output += keyStr.charAt(enc1) + keyStr.charAt(enc2) +
                keyStr.charAt(enc3) + keyStr.charAt(enc4);
  }
  return output;
}

const chat = document.getElementById('chat');


const startDetection = (video, canvas, type, deviceId, speed, wait, model) => {
  var proto;
  if(document.location.protocol == 'http:'){
    proto = 'ws';
  } else {
    proto = 'wss';
  }
  var path;
  if(type == 1) {
    path = "fall-detection-classes"
  } else {
    path = "fall-detection"
  }
  const socket = new WebSocket(proto+'://'+window.location.hostname+':'+window.location.port+'/'+path+'/'+speed+'/'+wait+'/'+model);
  socket.binaryType = "arraybuffer";
  let intervalId;

  // Connection opened
  socket.addEventListener('open', function () {
    document.getElementById("button-start").disabled = true;
    document.getElementById("button-stop").disabled = false;
    // Start reading video from device
    navigator.mediaDevices.getUserMedia({
      audio: false,
      video: {
        deviceId,
        width: { ideal: 1920 },
        height: { ideal: 1080 },
      },
    }).then(function (stream) {
      video.srcObject = stream;
      video.play().then(() => {
        // Adapt overlay canvas size to the video size
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        //textarea.style.height = video.videoHeight+'px';


        // Send an image in the WebSocket every 42 ms
        intervalId = setInterval(() => {

        // Create a virtual canvas to draw current video image
        const canvas = document.createElement('canvas');
        const ctx = canvas.getContext('2d');
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        ctx.drawImage(video, 0, 0);

        // Convert it to JPEG and send it to the WebSocket
        canvas.toBlob((blob) => socket.send(blob), 'image/jpeg', 0.8);
        }, speed);
      });
    });
  });

  // Listen for messages
  socket.addEventListener('message',function (event) {

    //const blobUrl = URL.createObjectURL(event.data) // blob is the Blob object

    //var detection = document.getElementById('detection');
    //detection.innerHTML = detection.innerHTML+event.data+'\n';
    //detection.scrollTop = detection.scrollHeight;
    var typeSelect = document.getElementById('type-select');
    if(typeSelect.value == 1){
      data = JSON.parse(event.data)
      createResponse(data)
    } else {
      var arrayBuffer = event.data;
      var bytes = new Uint8Array(arrayBuffer);
      var image = document.getElementById('image');
      //console.log(arrayBuffer.getBytes())
      image.src = 'data:image/jpg;base64,'+encode(bytes);
    }



    //blob = new Blob(event.data[0], {type: 'image/jpeg'});
    //canvas.getContext('2d').drawImage(img);
    //blobURL = URL.createObjectURL(blob);
    //console.log(blobURL)
    //canvas.src = blobURL
    //drawFaceRectangles(video, canvas, event.data);
  });

  // Stop the interval and video reading on close
  socket.addEventListener('close', function () {
    document.getElementById("button-start").disabled = false;
    document.getElementById("button-stop").disabled = true;


    window.clearInterval(intervalId);
    // A video's MediaStream object is available through its srcObject attribute
    var mediaStream = video.srcObject;

    // Through the MediaStream, you can get the MediaStreamTracks with getTracks():
    var tracks = mediaStream.getTracks();

    // Tracks are returned as an array, so if you know you only have one, you can stop it with:
    tracks[0].stop();

    chat.innerHTML = '';
    video.removeAttribute('src');
    video.load()
    image.removeAttribute('src');
  });

  return socket;
};

window.addEventListener('DOMContentLoaded', (event) => {
  const video = document.getElementById('video');
  const image = document.getElementById('image');
  const canvas = document.getElementById('canvas');
  const typeSelect = document.getElementById('type-select');
  const cameraSelect = document.getElementById('camera-select');
  const speedSelect = document.getElementById('speed-select');
  const waitSelect = document.getElementById('wait-select');
  const modelSelect = document.getElementById('model-select');
  let socket;

  // List available cameras and fill select
  navigator.mediaDevices.enumerateDevices().then((devices) => {
    let idVideo = 0
    for (const device of devices) {
      if (device.kind === 'videoinput' && device.deviceId) {
        idVideo++
        const deviceOption = document.createElement('option');
        deviceOption.value = device.deviceId;
        deviceOption.innerText = device.label == '' ? 'Camera'+idVideo : device.label;
        cameraSelect.appendChild(deviceOption);
      }
    }
  });

  // Start detection on the selected camera on submit
  document.getElementById('form-connect').addEventListener('submit', (event) => {
    event.preventDefault();

    // Close previous socket is there is one
    if (document.getElementById("button-start").disabled) {
      socket.close();
    } else {
      if(typeSelect.value == 1){
        video.style.display = "block"
        image.style.display = "none"
      } else {
        video.style.display = "none"
        image.style.display = "block"
      }
      const deviceId = cameraSelect.value;
      socket = startDetection(video, canvas, typeSelect.value, deviceId, speedSelect.value, waitSelect.value, modelSelect.value);
    }
  });

});
