// js/map.js

ymaps.ready(init);

let map, currentPlacemark, searchControl;
let isSatelliteView = false;

function init() {
    // Инициализация карты
    map = new ymaps.Map("map", {
        center: [55.76, 37.64],
        zoom: 10,
        controls: []
    });
    map.controls.add('zoomControl', { position: { right: 10, top: 50 } });

    // Поиск
    searchControl = new ymaps.control.SearchControl({
        options: {
            provider: 'yandex#search',
            noPlacemark: true,
            placeholderContent: 'Поиск лесного массива',
            resultsPerPage: 5
        }
    });
    map.controls.add(searchControl, {
        float: 'none',
        position: { top: 10, left: 100, right: 100 }
    });
    searchControl.events.add('resultselect', onResultSelect);
    document.getElementById('search-input').addEventListener('keypress', onSearchEnter);

    // Спутниковый/обычный вид
    document.getElementById('satellite-btn').addEventListener('click', toggleSatelliteView);

    // Импорт данных (заместо экспорта)
    const importBtn = document.getElementById('import-btn');
    const fileInput = document.getElementById('file-input');
    importBtn.addEventListener('click', () => fileInput.click());
    fileInput.addEventListener('change', uploadImage);

    // Добавляем демонстрационные лесные массивы
    addForestAreas();
}

function onResultSelect(e) {
    const idx = e.get('index');
    const results = searchControl.getResultsArray();
    if (!results[idx]) return;

    if (currentPlacemark) {
        map.geoObjects.remove(currentPlacemark);
    }
    currentPlacemark = new ymaps.Placemark(
        results[idx].geometry.getCoordinates(),
        { iconContent: 'Лесной массив' },
        { preset: 'islands#greenForestIcon' }
    );
    map.geoObjects.add(currentPlacemark);
    map.setCenter(results[idx].geometry.getCoordinates(), 14);
}

function onSearchEnter(e) {
    if (e.key === 'Enter') {
        searchControl.search(e.target.value);
    }
}

function toggleSatelliteView() {
    isSatelliteView = !isSatelliteView;
    const btn = document.getElementById('satellite-btn');
    if (isSatelliteView) {
        map.setType('yandex#satellite');
        btn.innerHTML = '<i class="fas fa-map"></i> Обычная карта';
    } else {
        map.setType('yandex#map');
        btn.innerHTML = '<i class="fas fa-satellite"></i> Спутниковый вид';
    }
}

async function uploadImage(e) {
    const file = e.target.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);
    // При необходимости:
    // formData.append('legal_entity_id', 1);

    try {
        const resp = await fetch('http://localhost:8000/images/', {
            method: 'POST',
            body: formData
        });
        if (!resp.ok) throw new Error(`Ошибка ${resp.status}`);
        const data = await resp.json();
        alert(`Успех! ID=${data.id}, filename=${data.filename}`);
    } catch (err) {
        console.error(err);
        alert('Ошибка при загрузке изображения');
    } finally {
        e.target.value = '';
    }
}

function addForestAreas() {
    const forests = [
        { name: "Лосиный Остров", coords: [55.877, 37.784] },
        { name: "Битцевский лес", coords: [55.597, 37.552] },
        { name: "Серебряный бор", coords: [55.778, 37.443] },
        { name: "Кузьминский лесопарк", coords: [55.693, 37.786] },
        { name: "Тропарёвский лесопарк", coords: [55.645, 37.472] }
    ];
    forests.forEach(f => {
        const pm = new ymaps.Placemark(
            f.coords,
            {
                iconContent: f.name,
                hintContent: 'Лесной массив',
                balloonContent: `<b>${f.name}</b><br>Здоровье леса: 85%`
            },
            {
                preset: 'islands#greenForestIcon',
                iconColor: '#2ecc71'
            }
        );
        map.geoObjects.add(pm);
    });
}
