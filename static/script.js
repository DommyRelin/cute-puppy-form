const video = document.getElementById('video');
const canvas = document.getElementById('canvas');
const photoInput = document.getElementById('photoInput');
const form = document.getElementById('uploadForm');

navigator.mediaDevices.getUserMedia({ video: true })
  .then(stream => {
    video.srcObject = stream;
  });

function takePhoto() {
  const context = canvas.getContext('2d');
  canvas.width = video.videoWidth;
  canvas.height = video.videoHeight;
  context.drawImage(video, 0, 0);

  canvas.toBlob(blob => {
    const file = new File([blob], 'photo.jpg', { type: 'image/jpeg' });
    const dataTransfer = new DataTransfer();
    dataTransfer.items.add(file);
    photoInput.files = dataTransfer.files;
    form.submit();
  }, 'image/jpeg');
}
