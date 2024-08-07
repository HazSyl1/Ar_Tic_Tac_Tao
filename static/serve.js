const processedVideo = document.getElementById('processed-video');


fetch('/reset', { method: 'POST' })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            console.log('Game state reset successfully.');
        } else {
            console.error('Error resetting game state: ', data.message);
        }
    })
    .catch(error => {
        console.error('Error resetting game state: ', error);
    });



// Request access to the camera
navigator.mediaDevices.getUserMedia({ video: true })
    .then(stream => {
        const videoTracks = stream.getVideoTracks();
        const track = videoTracks[0];
        const imageCapture = new ImageCapture(track);
        processFrames(imageCapture);
        

    })
    .catch(error => {
        console.error('Error accessing the camera: ', error);
    });

function processFrames(imageCapture) {
    const fps = 10; // Frames per second
    setInterval(() => {
        imageCapture.grabFrame()
            .then(imageBitmap => {
                const canvas = document.createElement('canvas');
                const context = canvas.getContext('2d');
                canvas.width = 1280;
                canvas.height = 900;
                context.drawImage(imageBitmap, 0, 0, canvas.width, canvas.height);
                canvas.toBlob(blob => {
                    const formData = new FormData();
                    formData.append('frame', blob, 'frame.jpg');
                    fetch('/process_frame', {
                        method: 'POST',
                        body: formData
                    })
                    .then(response => response.json())
                    .then(data => {
                        if (data.success) {
                            // Display the processed frame
                            
                            processedVideo.src = 'data:image/jpeg;base64,' + data.frame;
                        } else {
                            console.error('Error processing frame: ', data.message);
                        }
                    })
                    .catch(error => {
                        console.error('Error processing frame: ', error);
                    });
                }, 'image/jpeg');
            })
            .catch(error => {
                console.error('Error grabbing frame: ', error);
            });
    }, 1000 / fps);
}

