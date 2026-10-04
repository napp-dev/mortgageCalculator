# Ипотечник / Mortgage Tracker — правовые документы и поддержка

Публичные документы iOS-приложения «Ипотечник» (Mortgage Tracker) на 15 локалях App Store:
политика конфиденциальности, условия использования и страница поддержки. Сайт отдаёт GitHub Pages
из ветки `main`, корень репозитория.

**Сайт: https://napp-dev.github.io/mortgageCalculator/**

Единственный контакт во всех документах и на поддержке — почта `napp.dev.support@gmail.com`
(`contact_email` в `site.json`, в футере каждой страницы).

## Структура

- `<локаль>/privacy.md`, `<локаль>/terms.md`, `<локаль>/support.md` — исходники, их и правят.
- `<локаль>/<документ>/index.html` — готовые страницы, результат сборки. Руками не правятся.
- `en/` — псевдоним `en-US` для старых адресов `/en/privacy/` и `/en/terms/`: они зашиты в уже
  отправленные сборки приложения. Исходников в `en/` нет, страницы собираются из `en-US`.
- `index.md`, `index.html` — указатель языков.
- `site.json` — базовый путь, почта, дата сборки, локали и псевдонимы.
- `assets/style.css` — стили на палитре приложения, светлая и тёмная тема; без внешних шрифтов и скриптов.
- `scripts/build_pages.py` — сборка на Python 3 без внешних зависимостей.
- `.nojekyll` — Pages публикует готовый HTML без Jekyll.

## Правила

- **Адреса зашиты в приложение и в App Store Connect.** Коды локалей и имена документов
  не менять, репозиторий не переименовывать, псевдоним `en` не удалять — сломаются ссылки
  в выпущенных версиях.
- **Репозиторий публичный.** Сюда не попадают личные контакты кроме почты поддержки,
  внутренние заметки, ссылки на внутренние задачи и токены.
- **Все переводы меняются одним коммитом** и не расходятся по смыслу. Региональные варианты
  (en-GB/AU/CA, fr-CA, es-MX, pt-PT) отличаются от базовых только языком, не содержанием.
- Названия пунктов меню приложения в текстах — как в интерфейсе на этом языке. У pt-PT
  интерфейс бразильский, поэтому пути внутри приложения там в варианте pt-BR.

## Обновление

1. Изменить документ во всех локалях и дату редакции в каждой. Поменять `updated` в `site.json`.
2. Выполнить `python3 scripts/build_pages.py` из корня репозитория. Сборка падает на битой
   локальной ссылке, front matter, незакрытом `**` и документе без единственного заголовка `#`.
3. Проверить HTML, закоммитить исходники вместе с результатом сборки, push в `main`.
   Pages пересоберёт сайт за 1–2 минуты — статус во вкладке **Actions**.
4. Открыть изменённые адреса в режиме инкогнито и убедиться, что видна новая редакция.

Генератор понимает заголовки `#`–`###`, абзацы, списки `- `, ссылки и `**жирный**`. Таблиц нет.

Старые редакции отдельно не публикуются: новая заменяет предыдущую по тому же адресу,
история — в коммитах.

## Адреса

| Локаль | Privacy Policy | Terms of Use | Support |
| --- | --- | --- | --- |
| ru | https://napp-dev.github.io/mortgageCalculator/ru/privacy/ | https://napp-dev.github.io/mortgageCalculator/ru/terms/ | https://napp-dev.github.io/mortgageCalculator/ru/support/ |
| en-US | https://napp-dev.github.io/mortgageCalculator/en-US/privacy/ | https://napp-dev.github.io/mortgageCalculator/en-US/terms/ | https://napp-dev.github.io/mortgageCalculator/en-US/support/ |
| en-GB | https://napp-dev.github.io/mortgageCalculator/en-GB/privacy/ | https://napp-dev.github.io/mortgageCalculator/en-GB/terms/ | https://napp-dev.github.io/mortgageCalculator/en-GB/support/ |
| en-AU | https://napp-dev.github.io/mortgageCalculator/en-AU/privacy/ | https://napp-dev.github.io/mortgageCalculator/en-AU/terms/ | https://napp-dev.github.io/mortgageCalculator/en-AU/support/ |
| en-CA | https://napp-dev.github.io/mortgageCalculator/en-CA/privacy/ | https://napp-dev.github.io/mortgageCalculator/en-CA/terms/ | https://napp-dev.github.io/mortgageCalculator/en-CA/support/ |
| de-DE | https://napp-dev.github.io/mortgageCalculator/de-DE/privacy/ | https://napp-dev.github.io/mortgageCalculator/de-DE/terms/ | https://napp-dev.github.io/mortgageCalculator/de-DE/support/ |
| fr-FR | https://napp-dev.github.io/mortgageCalculator/fr-FR/privacy/ | https://napp-dev.github.io/mortgageCalculator/fr-FR/terms/ | https://napp-dev.github.io/mortgageCalculator/fr-FR/support/ |
| fr-CA | https://napp-dev.github.io/mortgageCalculator/fr-CA/privacy/ | https://napp-dev.github.io/mortgageCalculator/fr-CA/terms/ | https://napp-dev.github.io/mortgageCalculator/fr-CA/support/ |
| es-ES | https://napp-dev.github.io/mortgageCalculator/es-ES/privacy/ | https://napp-dev.github.io/mortgageCalculator/es-ES/terms/ | https://napp-dev.github.io/mortgageCalculator/es-ES/support/ |
| es-MX | https://napp-dev.github.io/mortgageCalculator/es-MX/privacy/ | https://napp-dev.github.io/mortgageCalculator/es-MX/terms/ | https://napp-dev.github.io/mortgageCalculator/es-MX/support/ |
| pt-BR | https://napp-dev.github.io/mortgageCalculator/pt-BR/privacy/ | https://napp-dev.github.io/mortgageCalculator/pt-BR/terms/ | https://napp-dev.github.io/mortgageCalculator/pt-BR/support/ |
| pt-PT | https://napp-dev.github.io/mortgageCalculator/pt-PT/privacy/ | https://napp-dev.github.io/mortgageCalculator/pt-PT/terms/ | https://napp-dev.github.io/mortgageCalculator/pt-PT/support/ |
| it | https://napp-dev.github.io/mortgageCalculator/it/privacy/ | https://napp-dev.github.io/mortgageCalculator/it/terms/ | https://napp-dev.github.io/mortgageCalculator/it/support/ |
| ja | https://napp-dev.github.io/mortgageCalculator/ja/privacy/ | https://napp-dev.github.io/mortgageCalculator/ja/terms/ | https://napp-dev.github.io/mortgageCalculator/ja/support/ |
| ko | https://napp-dev.github.io/mortgageCalculator/ko/privacy/ | https://napp-dev.github.io/mortgageCalculator/ko/terms/ | https://napp-dev.github.io/mortgageCalculator/ko/support/ |
