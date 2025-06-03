require('dotenv').config();
const express = require('express');
const session = require('express-session');
const fs = require('fs');
const path = require('path');
const { TwitterApi } = require('twitter-api-v2');

const app = express();
const port = 3000;

app.use(session({
  secret: 'some-secret',
  resave: false,
  saveUninitialized: true,
}));

// Старт авторизации
app.get('/login', async (req, res) => {
  const client = new TwitterApi({
    appKey: process.env.TWITTER_API_KEY,
    appSecret: process.env.TWITTER_API_SECRET,
  });

  try {
    const { url, oauth_token, oauth_token_secret } = await client.generateAuthLink('http://localhost:3000/callback');
    req.session.oauth_token = oauth_token;
    req.session.oauth_token_secret = oauth_token_secret;
    res.redirect(url);
  } catch (e) {
    console.error('Ошибка при генерации ссылки авторизации:', e);
    res.status(500).send('Ошибка авторизации');
  }
});

// Callback после авторизации
app.get('/callback', async (req, res) => {
  const { oauth_token, oauth_verifier } = req.query;
  const { oauth_token: token, oauth_token_secret } = req.session;

  if (!oauth_token || !oauth_verifier || !token || !oauth_token_secret) {
    return res.status(400).send('Плохой запрос.');
  }

  const client = new TwitterApi({
    appKey: process.env.TWITTER_API_KEY,
    appSecret: process.env.TWITTER_API_SECRET,
    accessToken: token,
    accessSecret: oauth_token_secret,
  });

  try {
    // Получаем клиента с токенами доступа пользователя
    const { client: loggedClient, accessToken, accessSecret } = await client.login(oauth_verifier);

    // Сохраняем токены пользователя в сессии, чтобы можно было обновить профиль
    req.session.accessToken = accessToken;
    req.session.accessSecret = accessSecret;

    // Обновляем профиль пользователя: аватарка, ник и описание
    // Замените путь на ваш файл с аватаркой
    const imagePath = path.resolve(__dirname, 'avatar.jpg');
    const imageData = fs.readFileSync(imagePath, { encoding: 'base64' });

    // Загрузка изображения
    const mediaId = await loggedClient.v1.uploadMedia(Buffer.from(imageData, 'base64'), { type: 'image/jpeg' });

    // Обновление профиля
    await loggedClient.v1.updateAccountProfile({
      name: 'Новый Ник',
      description: 'Новое описание профиля',
      profile_image_url: null, // Игнорируем, т.к. меняем через mediaId
      profile_banner_url: null, // Оставляем пустым, если не меняем
    });

    // Установка аватарки через mediaId (в API v1.1 нет прямой смены аватарки через mediaId, но uploadMedia возвращает mediaId для твитов.
    // Для смены аватарки используется updateProfileImage)
    await loggedClient.v1.updateProfileImage(imageData);

    const user = await loggedClient.currentUser();
    res.send(`Вы вошли как @${user.screen_name}. Профиль обновлен.`);
  } catch (e) {
    console.error('Ошибка при логине или обновлении профиля:', e);
    res.status(500).send('Ошибка авторизации или обновления профиля');
  }
});

app.listen(port, () => {
  console.log(`Сервер запущен: http://localhost:${port}`);
});
