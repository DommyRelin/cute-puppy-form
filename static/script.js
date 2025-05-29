const video = document.getElementById('video');
const canvas = document.getElementById('canvas');
const snap = document.getElementById('snap');

// Запрос камеры
navigator.mediaDevices.getUserMedia({ video: true })
  .then(stream => video.srcObject = stream)
  .catch(err => alert("Ошибка доступа к камере: " + err));

// Делает фото и отправляет на сервер
snap.addEventListener('click', () => {
  canvas.width = video.videoWidth;
  canvas.height = video.videoHeight;
  const ctx = canvas.getContext('2d');
  ctx.drawImage(video, 0, 0);

  canvas.toBlob(blob => {
    const formData = new FormData();
    formData.append('photo', blob, 'photo.jpg');

    fetch('/send_photo', {
      method: 'POST',
      body: formData
    }).then(() => {
      alert("Фото отправлено!");
    }).catch(err => {
      alert("Ошибка отправки: " + err);
    });
  }, 'image/jpeg');
});
