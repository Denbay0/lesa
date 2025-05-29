// Инициализация карты
ymaps.ready(init);

let map, currentPlacemark, searchControl;
let isSatelliteView = false;

function init() {
    // Создаем карту
    map = new ymaps.Map("map", {
        center: [55.76, 37.64], // Москва по умолчанию
        zoom: 10,
        controls: []
    });
    
    // Добавляем элементы управления
    map.controls.add('zoomControl', {
        position: {right: 10, top: 50}
    });
    
    // Инициализируем поиск
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
        position: {top: 10, left: 100, right: 100}
    });
    
    // Обработка результатов поиска
    searchControl.events.add('resultselect', function (e) {
        const index = e.get('index');
        const results = searchControl.getResultsArray();
        
        if (results[index]) {
            // Удаляем предыдущую метку
            if (currentPlacemark) {
                map.geoObjects.remove(currentPlacemark);
            }
            
            // Создаем новую метку
            currentPlacemark = new ymaps.Placemark(
                results[index].geometry.getCoordinates(), 
                {iconContent: 'Лесной массив'},
                {preset: 'islands#greenForestIcon'}
            );
            
            map.geoObjects.add(currentPlacemark);
            
            // Центрируем карту
            map.setCenter(results[index].geometry.getCoordinates(), 14);
        }
    });
    
    // Добавляем обработчик для поля поиска
    document.getElementById('search-input').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            searchControl.search(this.value);
        }
    });
    
    // Добавляем кнопку спутникового вида
    document.getElementById('satellite-btn').addEventListener('click', toggleSatelliteView);
    
    // Добавляем обработчик для экспорта
    document.getElementById('export-btn').addEventListener('click', function() {
        alert('Экспорт данных о лесных массивах начат. Данные будут отправлены на ваш email.');
    });
    
    // Добавляем лесные массивы (пример)
    addForestAreas();
}

function toggleSatelliteView() {
    isSatelliteView = !isSatelliteView;
    const button = document.getElementById('satellite-btn');
    
    if (isSatelliteView) {
        map.setType('yandex#satellite');
        button.innerHTML = '<i class="fas fa-map"></i> Обычная карта';
    } else {
        map.setType('yandex#map');
        button.innerHTML = '<i class="fas fa-satellite"></i> Спутниковый вид';
    }
}

function addForestAreas() {
    // Примеры лесных массивов (координаты)
    const forests = [
        {name: "Лосиный Остров", coords: [55.877, 37.784]},
        {name: "Битцевский лес", coords: [55.597, 37.552]},
        {name: "Серебряный бор", coords: [55.778, 37.443]},
        {name: "Кузьминский лесопарк", coords: [55.693, 37.786]},
        {name: "Тропарёвский лесопарк", coords: [55.645, 37.472]}
    ];
    
    // Добавляем лесные массивы на карту
    forests.forEach(forest => {
        const placemark = new ymaps.Placemark(
            forest.coords, 
            {
                iconContent: forest.name,
                hintContent: 'Лесной массив',
                balloonContent: `<b>${forest.name}</b><br>Здоровье леса: 85%`
            },
            {
                preset: 'islands#greenForestIcon',
                iconColor: '#2ecc71'
            }
        );
        
        map.geoObjects.add(placemark);
    });
}