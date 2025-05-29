// js/segment.js

const fileInput  = document.getElementById('file-input');
const uploadBtn  = document.getElementById('upload-btn');
const processBtn = document.getElementById('process-btn');
const previewImg = document.getElementById('preview');
const resultImg  = document.getElementById('result');

let selectedFile = null;

// Когда пользователь кликает «Выбрать фото»
uploadBtn.addEventListener('click', () => fileInput.click());

// После выбора файла — показываем предпросмотр
fileInput.addEventListener('change', () => {
  if (!fileInput.files.length) return;
  selectedFile = fileInput.files[0];
  const url = URL.createObjectURL(selectedFile);
  previewImg.src = url;
  previewImg.style.display = 'block';
  resultImg.style.display  = 'none';
  processBtn.style.display = 'inline-block';
});

// По клику «Запустить анализ» шлём на бэкенд
processBtn.addEventListener('click', async () => {
  if (!selectedFile) return alert('Сначала выберите фото');
  
  processBtn.textContent = 'Обработка…';
  processBtn.disabled   = true;
  
  // Собираем form-data
  const form = new FormData();
  form.append('file', selectedFile);
  
  try {
    const resp = await fetch('/segment/file', {
      method: 'POST',
      body: form
    });
    if (!resp.ok) throw new Error(`Ошибка: ${resp.status}`);
    
    // Получаем blob-изображение
    const blob = await resp.blob();
    const imgUrl = URL.createObjectURL(blob);
    
    resultImg.src = imgUrl;
    resultImg.style.display = 'block';
  
  } catch (e) {
    alert('Не удалось обработать снимок:\n' + e.message);
  } finally {
    processBtn.textContent = 'Запустить анализ';
    processBtn.disabled    = false;
  }
});
