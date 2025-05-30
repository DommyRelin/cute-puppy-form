const video = document.getElementById('video');
const canvas = document.getElementById('canvas');
const snap = document.getElementById('snap');
const submitButton = document.getElementById('submit-button');
const photoData = document.getElementById('photoData');
const form = document.querySelector('form');

navigator.mediaDevices.getUserMedia({ video: true })
  .then(stream => {
    video.srcObject = stream;
  })
  .catch(err => {
    alert("Camera access error: " + err);
  });

snap.addEventListener('click', () => {
  canvas.width = video.videoWidth;
  canvas.height = video.videoHeight;
  const ctx = canvas.getContext('2d');
  ctx.drawImage(video, 0, 0);

  // Get Base64 data from the canvas
  const dataUrl = canvas.toDataURL('image/jpeg');
  photoData.value = dataUrl;

  submitButton.disabled = false;
  alert("Photo taken and ready to send!");
});

submitButton.addEventListener('click', async () => {
  if (!photoData.value) {
    alert("Please take a photo first!");
    return;
  }

  const formData = new FormData(form);

  try {
    const response = await fetch('/send', {
      method: 'POST',
      body: formData
    });

    const result = await response.json();

    if (result.success) {
      alert("Sent to Telegram! 💖");
      submitButton.disabled = true;
      photoData.value = '';
      form.reset();
    } else {
      alert("Error: " + (result.error || "Unknown error"));
    }
  } catch (err) {
    alert("Sending error: " + err.message);
  }
});
