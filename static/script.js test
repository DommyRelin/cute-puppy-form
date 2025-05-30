const video = document.getElementById('video');
const canvas = document.getElementById('canvas');
const snap = document.getElementById('snap');
const submitButton = document.getElementById('submit-button');
const photoData = document.getElementById('photoData');
const form = document.querySelector('form');
const preview = document.getElementById('preview'); // для превью

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

  // Show preview
  if (preview) {
    preview.src = dataUrl;
    preview.style.display = 'block';
  }

  submitButton.disabled = false;
  alert("Photo taken and ready to send!");
});

submitButton.addEventListener('click', async () => {
  if (!photoData.value || !photoData.value.startsWith('data:image/jpeg')) {
    alert("Please take a valid photo first!");
    return;
  }

  submitButton.disabled = true;
  submitButton.textContent = 'Sending...';

  const formData = new FormData(form);

  try {
    const response = await fetch('/send', {
      method: 'POST',
      body: formData
    });

    const result = await response.json();

    if (result.success) {
      alert("Sent to Mommy! 💖");
      photoData.value = '';
      form.reset();
      if (preview) preview.style.display = 'none';
    } else {
      alert("Error: " + (result.error || "Unknown error"));
    }
  } catch (err) {
    alert("Sending error: " + err.message);
  } finally {
    submitButton.disabled = false;
    submitButton.textContent = 'Submit';
  }
});
