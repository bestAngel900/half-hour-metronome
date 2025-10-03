# half-hour-metronome

Автокоміти **кожні 30 хвилин (UTC)**. Кожен запуск створює JSON-снапшот у `data/YYYY-MM-DD/HHMMSS.json` з базовими полями (UTC timestamp, unix, “півгодинний бакет”) та коротким checksum.  
Проєкт **без зовнішніх API** (лише стандартна бібліотека Python), тому працює стабільно та передбачувано.

## Що всередині
- `scripts/update.py` — пише унікальний JSON-файл на кожен запуск
- `snapshot.yml` — GitHub Actions з cron `:00` та `:30` щогодини
- `requirements.txt` — порожній (stdlib only)

## Швидкий старт
1. Створи публічний репозиторій **half-hour-metronome** (або іншу назву).
2. Додай файли з цього README (включно з папками `scripts` та `.github/workflows/`).
3. У **Settings → Secrets and variables → Actions → New repository secret** створи секрет:
   - **Name:** `GH_TOKEN`
   - **Value:** **Fine-grained** Personal Access Token з правами **Contents: Read and write** і доступом **тільки до цього репозиторію**.
4. Відкрий `.github/workflows/snapshot.yml` і заміни:
   - `YOUR_LOGIN` → твій GitHub логін  
   - `YOUR_ID+YOUR_LOGIN@users.noreply.github.com` → твій no-reply email (див. GitHub → Profile → Emails)
5. Зроби коміт у `main` і виконай перший запуск вручну: **Actions → snapshot → Run workflow**.
6. Далі ранити буде **автоматично**: `:00` та `:30` (UTC). Дозволено запізнення на 5–10 хв.

## Перевірка
- У вкладці **Actions** для ранiв має стояти подія **Scheduled** (не тільки `workflow_dispatch`).
- У логах побачиш рядок `wrote file: data/YYYY-MM-DD/HHMMSS.json` і коміт `snapshot: YYYY-MM-DD HH:MM:SSZ`.

## Чому стабільно
- Жодних зовнішніх HTTP-запитів → не зламається через мережу / ключі.
- Кожен файл має унікальну назву по секунді та “сіль”, тож diff завжди є.

## Ідеї для форку
- Додати поля: `weekday_name`, `quarter`, `day_of_year`.
- Писати ще `latest.json` з дублем останнього снапшоту.
- Додати бейдж “Last run” у README.
