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

            fetch('http://192.168.88.30:8000/liveness/', {
            // fetch('http://127.0.0.1:8000/liveness/', {
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


document.getElementById('analyze').addEventListener('click', function() {
    var photoInput = document.getElementById('analyzePhotoInput').files[0];
    var formData = new FormData();
    formData.append('file', photoInput);

    fetch('http://192.168.88.30:8000/analyze/', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        alert('Analysis Result: ' + JSON.stringify(data.prediction));
    })
    .catch(error => {
        console.error('Error:', error);
    });
});

document.getElementById('verify').addEventListener('click', function() {
    var photo1Input = document.getElementById('photo1Input').files[0];
    var photo2Input = document.getElementById('photo2Input').files[0];
    var formData = new FormData();
    formData.append('file1', photo1Input);
    formData.append('file2', photo2Input);

    fetch('http://192.168.88.30:8000/verification/', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if(data) {
            alert('Verification Successful');
        } else {
            alert('Verification Failed');
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
});


navigator.mediaDevices.getUserMedia({ video: true })
    .then(function(stream) {
        var video = document.getElementById('analysisVideo');
        video.srcObject = stream;
    })
    .catch(function(err) {
        console.log("An error occurred: " + err);
    });


document.getElementById('captureAnalysis').addEventListener('click', function() {
    var canvas = document.getElementById('analysisCanvas');
    var video = document.getElementById('analysisVideo');
    canvas.getContext('2d').drawImage(video, 0, 0, 320, 240);

    canvas.toBlob(function(blob) {
        var formData = new FormData();
        formData.append('file', blob, 'analysis_photo.png');

        fetch('http://192.168.88.30:8000/analyze/', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            alert('Analysis Result: ' + JSON.stringify(data.prediction));
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }, 'image/png');
});
    

// This is a simple approach - you may need more sophisticated state management for multiple images
var verificationImage1 = null;

document.getElementById('captureVerification').addEventListener('click', function() {
    var canvas = document.getElementById('analysisCanvas');
    var video = document.getElementById('analysisVideo');
    canvas.getContext('2d').drawImage(video, 0, 0, 320, 240);

    canvas.toBlob(function(blob) {
        if (!verificationImage1) {
            verificationImage1 = blob;
            alert('First image captured. Please capture the second image.');
        } else {
            var formData = new FormData();
            formData.append('file1', verificationImage1, 'verification_photo1.png');
            formData.append('file2', blob, 'verification_photo2.png');

            fetch('http://192.168.88.30:8000/verification/', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if(data) {
                    alert('Verification Successful');
                } else {
                    alert('Verification Failed');
                }
                // Reset the first image for the next verification
                verificationImage1 = null;
            })
            .catch(error => {
                console.error('Error:', error);
            });
        }
    }, 'image/png');
});
