TikTokAutoUploader — FIX BUILD

Что исправлено
===============
1. TikTok verification больше не считается обычным tutorial popup.
2. Скрипт не нажимает Escape/Cancel поверх human verification.
3. Если TikTok показывает несколько verification подряд, скрипт ждёт, пока окно стабильно исчезнет.
4. Добавлены verification checkpoints:
   - перед выбором видео;
   - после выбора видео;
   - перед caption;
   - после caption;
   - во время обработки видео;
   - перед добавлением музыки;
   - перед публикацией.
5. Исправлен race, когда verification появляется ровно перед кликом по caption.
6. В ожидании обработки видео скрипт также отслеживает verification.
7. Добавлена команда video в photo_uploader.py для загрузки одного видео сразу на несколько аккаунтов.
8. Сохранены предыдущие исправления: photo carousel, multi-account, Windows npm.cmd.

ВАЖНО ПРО CAPTCHA
=================
Скрипт не обходит verification автоматически.
Если TikTok показывает "Verify that you're not a robot", запускай с --visible-browser,
пройди все проверки руками и не закрывай браузер. Скрипт продолжит сам.

Установка / перенос
===================
1. Распакуй архив в новую папку.
2. Из старой рабочей папки скопируй в корень:
   TK_cookies_acc1.json
   TK_cookies_acc2.json
   ...
   TK_cookies_acc7.json

   Не отправляй эти файлы другим людям — это сессии аккаунтов.

3. Видео положи в корень как:
   video.mp4

4. Если Node-зависимости ещё не установлены:
   cd tiktokautouploader\Js_assets
   npm install
   cd ..\..

Логин нового аккаунта
=====================
py photo_uploader.py login acc8

Видео на acc6 + acc7 с видимым браузером
=========================================
py photo_uploader.py video .\video.mp4 --accounts acc6 acc7 --caption "релиз в тг t.me/donutgram" --hashtags iphone ayugram рек ayugramios --sound "ДИНАСТИЯ - VILLIAN & madk1d" --sound-volume mix --visible-browser

Видео на acc1-acc7
==================
py photo_uploader.py video .\video.mp4 --accounts acc1 acc2 acc3 acc4 acc5 acc6 acc7 --caption "релиз в тг t.me/donutgram" --hashtags iphone ayugram рек ayugramios --sound "ДИНАСТИЯ - VILLIAN & madk1d" --sound-volume mix --visible-browser

После того как TikTok перестанет показывать verification, можно убрать:
--visible-browser

Фото-карусель на все аккаунты
=============================
py photo_uploader.py photos .\photos --accounts acc1 acc2 acc3 acc4 acc5 acc6 acc7 --caption "релиз в тг t.me/donutgram" --hashtags iphone ayugram рек ayugramios --visible-browser

Если verification зависла на белом окне со спиннером
====================================================
Не перезапускай все аккаунты сразу.
Попробуй обновить сам challenge кнопкой refresh в окне TikTok.
Если конкретный аккаунт продолжает получать сломанную verification-сессию:
1. останови запуск;
2. удали только TK_cookies_accN.json для проблемного аккаунта;
3. py photo_uploader.py login accN
4. снова запусти только этот аккаунт с --visible-browser.


НОВЫЙ FIX ДЛЯ БЕСКОНЕЧНО ПЕРЕЗАГРУЖАЮЩЕЙСЯ VERIFICATION
=========================================================
Теперь каждый аккаунт использует постоянный браузерный профиль:
.tiktok_profiles\acc1
.tiktok_profiles\acc2
...

Используется установленный Google Chrome без поддельного Chrome/124 и без
жёсткой таймзоны America/New_York. Это сохраняет device/session storage TikTok
между запусками и уменьшает пересоздание verification challenge.

Для первого теста запускай только проблемный аккаунт:
py photo_uploader.py video .\video.mp4 --accounts acc6 --caption "релиз в тг t.me/donutgram" --hashtags iphone ayugram рек ayugramios --sound "ДИНАСТИЯ - VILLIAN & madk1d" --sound-volume mix --visible-browser

Если раньше уже запускал эту новую persistent-profile версию и профиль acc6
получился сломанным, закрой все окна Chrome, удали только:
.tiktok_profiles\acc6
и запусти acc6 ещё раз. Cookie-файл TK_cookies_acc6.json оставь.
