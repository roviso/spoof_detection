document.getElementById('capture').addEventListener('click', function() {
    var canvas = document.getElementById('canvas');
    var video = document.getElementById('video');
    canvas.getContext('2d').drawImage(video, 0, 0, 320, 240);

    // Hide video and show canvas
    video.style.display = 'none';
    $('#canvas').show();
});

navigator.mediaDevices.getUserMedia({ video: true })
    .then(function(stream) {
        var video = document.getElementById('video');
        video.srcObject = stream;
    })
    .catch(function(err) {
        console.log("An error occurred: " + err);
    });

document.getElementById('submit').addEventListener('click', function() {
    var canvas = document.getElementById('canvas');
    var livePhoto = canvas.toDataURL('image/png');
    var photoIdInput = document.getElementById('photoIdInput').files[0];

    // Convert base64 to blob
    fetch(livePhoto)
        .then(res => res.blob())
        .then(blob => {
            var formData = new FormData();
            // formData.append('file', photoIdInput, 'photo_id.png');
            formData.append('file', blob, 'live_photo.png');

            // fetch('http://192.168.88.30:8000/liveness/', {
            fetch('http://127.0.0.1:8000/liveness/', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    alert('Verified Successfully');
                } else if (data.status === 'failed') {
                    alert('Verification Failed');
                } else if (data.status === 'liveliness_not_verified') {
                    alert('Unable to Verify Liveliness. Please Retake the Photo');
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
        });
});
