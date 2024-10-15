$(document).ready(function () {
    updateModels()

    updateClearButton()

    connectSelects()

    $('#searchForm').submit(function () {

        $.ajax({
            data: $(this).serialize(),
            type: $(this).attr('method'),
            url: $(location).attr('href'),
            success: function (response) {
                const newParams = $('#searchForm').serialize().split('&').filter(e => e.split('=')[0] != 'csrfmiddlewaretoken');
                const url = new URL(window.location.href);
                newParams.forEach(e => url.searchParams.set(e.split('=')[0], e.split('=')[1]))
                url.searchParams.set('page', '1')

                window.history.pushState({}, '', url);

                const cars = response.cars_info; // Получаем массив автомобилей
                let carsHtml = ''; // Переменная для хранения HTML-кода

                // Генерируем HTML-код для каждого автомобиля
                cars.forEach(car => {

                    carsHtml += `
                        <div class="swiper-slide">
                            <a href="${ window.location.pathname }${car.id}" class="items2">
                                <div class="top_items">
                                    <h3>${car.mark} ${car.model}</h3>
                                    <p>${car.year} • ${Number(car.mileage).toLocaleString('ru-RU')} км  • ${car.eng_v} л.</p>
                                </div>
                                <div class="img_items">
                                    <img class="main_card_img" src="${car.images[0]}" alt="">
                                </div>
                                <div class="bottoms_als">
                                    <h4>${car.price.toLocaleString('ru-RU')} ₽</h4>
                                    <div class="red_btn">Оставить заявку</div>
                                </div>
                            </a>
                        </div>
                    `;
                });

                // Обновляем контейнер с автомобилями
                $('#carContainer').html(carsHtml);

                const pageRange = response.page_range; // Новый диапазон страниц
                const currentPage = 1; // Текущая страница
                console.log(pageRange)

                // Генерируем HTML-код для пагинации
                let paginationHtml = '';
                for (const page of pageRange) {
                    if (page === "...") {
                        paginationHtml += `<span>...</span>`;
                    } else if (page === currentPage) {
                        paginationHtml += `<span class="current-page">${page}</span>`; // Выделяем текущую страницу
                    } else {
                        url.searchParams.set('page', `${page}`)
                        paginationHtml += `<a href="?${url.searchParams.toString()}">${page}</a>`;
                    }
                }

                // Обновляем контейнер с пагинацией
                $('.pagination').html(paginationHtml);

                updateClearButton();
            },
            error: function (response) {
                const errors = JSON.parse(response.responseJSON.errors)
                console.log(errors)
            }
        });
        return false;
    });

    function updateClearButton() {
        const newParams = $('#searchForm').serialize().split('&').filter(e => e.split('=')[0] != 'csrfmiddlewaretoken');
        const is_visible = newParams.some(e => e.split('=')[1])
        if (is_visible) {
            $(".search-form a").css("visibility", "visible");
        } else {
            $(".search-form a").css("visibility", "hidden");
        }
    }

    const images = Array.from(document.getElementsByClassName("check_img"))
    const placeholderImage = '/static/img/no_photo.jpg'

    images.forEach(img => {
        // Проверяем, загружено ли изображение
        if (img.complete) {
            checkImageSize(img);
        } else {
            img.addEventListener('load', () => checkImageSize(img));
            img.addEventListener('error', () => {
                img.src = placeholderImage; // Заменяем на изображение заглушку
            });
        }
    });

    function checkImageSize(img) {
        if (img.naturalWidth <= 1 || img.naturalHeight <= 1) {
            img.src = placeholderImage; // Заменяем на изображение заглушку
        }
    }
})

const connectSelects = () => {
    const selects = Array.from(document.querySelectorAll(".search-form select"));

    selects.forEach(select => {
        const dropdown = document.getElementById(`${select.name}-dropdown`);
        const button = dropdown.querySelector('.catalog__filter-select--btn');
        const value = select.value
        button.textContent = select.options[select.selectedIndex].text;
        if (value !== "") {
            button.style.color = '#FFFFFF'
        } else {
            button.style.color = '#FFFFFF80'
        }
    })
};

const setField = (field, value, text) => {
    let dropdown = document.getElementById(`${field}-dropdown`);
    var input = document.querySelector(`[name=${field}]`);
    input.value = value;

    // Выбор кнопки для изменения текста
    let button = dropdown.querySelector('.catalog__filter-select--btn');

    console.log(button)

    if (value !== "") {
        button.style.color = '#FFFFFF'
    } else {
        button.style.color = '#FFFFFF80'
    }

    if (field === "mark") {
        updateModels();
    }

    // Обновление текста кнопки
    button.textContent = text;
};

function updateModels() {
    const markId = $("[name='mark']").val();
    $.ajax({
        url: `/models/?mark_id=${markId || -1}`,
        type: 'GET',
        success: function (data) {

            const selectedModel = $('#id_model').val();
            console.log(selectedModel)

            // Очищаем текущий список моделей и добавляем первую опцию
            $('#id_model').empty().append('<option value="" selected="">Модель авто</option>');

            // Добавляем новые опции из данных
            $.each(data, function (index, item) {
                $('#id_model').append('<option value="' + item.id + '">' + item.name + '</option>');
            });

            $('#model-dropdown .dropdown-menu').empty().append('<li><button type="button" onclick="setField(\'model\', \'None\', \'Модель авто\')" class="dropdown-item" href="#">Модель авто</button></li>');

            // Добавляем новые опции из данных
            $.each(data, function (index, item) {
                $('#model-dropdown .dropdown-menu').append(`<li><button type="button" onclick="setField('model', '${item.id}', '${item.name}')" class="dropdown-item" href="#">${item.name}</button></li>`);
            });

            // Устанавливаем выбранную модель, если она присутствует в обновленных данных
            if (data.some(item => Number(item.id) === Number(selectedModel))) {
                $('#id_model').val(selectedModel);
            } else {
                $('#id_model').val(''); // Если модели нет, выбираем "Модель авто"
            }

            const select = document.querySelector("#id_model");

            const dropdown = document.getElementById(`model-dropdown`);
            const button = dropdown.querySelector('.catalog__filter-select--btn');
            button.textContent = select.options[select.selectedIndex].text;

        },
        error: function (xhr, status, error) {
            console.error('Ошибка AJAX:', error);
        }
    });
}