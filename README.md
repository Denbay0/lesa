# lesa# 🌲 LESA – Анализ лесных массивов

**LESA** — это веб-приложение для визуализации и анализа лесных массивов с помощью спутниковых снимков, дронов и нейросетей.  
Пользователь может:
- Просматривать карту лесных массивов (с интерактивным поиском и метками).  
- «Импортировать» собственные снимки для последующей обработки нейросетью.  
- Оставить заявку от юридического лица на получение услуг мониторинга и анализа.  
- Запустить сегментацию изображения через встроенный API.

---

## 📂 Структура проекта

├── css/
│ └── title.css ← Стили страницы
├── html/
│ ├── index.html ← Главная страница
│ ├── map.html ← Карта лесных массивов
│ ├── products.html ← Страница «Продукты и услуги»
│ ├── request.html ← Форма заявки для юр. лиц
│ └── segment.html ← Интерфейс сегментации изображений
├── js/
│ ├── index.js ← Скрипты для index.html
│ ├── map.js ← Логика карты и загрузки изображений
│ ├── request.js ← Отправка формы заявки
│ └── segment.js ← Вызов API сегментации
├── src/
│ ├── backend/ ← FastAPI + SQLAlchemy бэкенд
│ │ ├── db.py ← Инициализация SQLite-базы (database.db)
│ │ ├── main_api.py ← Точка входа FastAPI, статические маршруты
│ │ ├── models.py ← SQLAlchemy-модели (LegalEntity, ImageUpload)
│ │ ├── schemas.py ← Pydantic-схемы (LegalEntityCreate, ImageUploadRead)
│ │ ├── routers/ ← Роуты API
│ │ │ ├── legal.py ← POST /legal/ — создать заявку юр. лица
│ │ │ ├── images.py ← POST /images/ — загрузить картинку
│ │ │ ├── segmentation.py ← POST /segment/ — сегментация через нейросеть
│ │ └── database.db ← Локальный файл SQLite
│ └── model/ ← Весы и скрипты нейросети (PyTorch .pt)
│ ├── yolov11n-seg.pt
│ └── …
├── uploads/ ← Загруженные через API изображения
├── venv/ ← Виртуальное окружение
├── requirements.txt ← Список зависимостей Python
└── README.md ← Этот файл

---

## ⚙️ Быстрый старт

1. **Клонируйте репозиторий**  
   ```bash
   git clone <URL>
   cd LESA

2. Создайте и активируйте виртуальное окружение
python3 -m venv venv
# macOS/Linux
source venv/bin/activate
# Windows (PowerShell)
.\venv\Scripts\Activate.ps1

3. Установите зависимости
pip install --upgrade pip
pip install -r requirements.txt

4. Запустите сервер
uvicorn src.backend.main_api:app --reload

API доступно по адресу: http://localhost:8000

Swagger UI: http://localhost:8000/docs

Статические страницы: http://localhost:8000/index.html, map.html, request.html, segment.html и т. д.
