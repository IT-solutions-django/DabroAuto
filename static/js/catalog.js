const orderingParams = [
    ['', 'Сортировка'],
    ["asc_mileage", "Пробег: по возрастанию"],
    ["desc_mileage", "Пробег: по убыванию"],
    ["asc_price", "Стоимость: по возрастанию"],
    ["desc_price", "Стоимость: по убыванию"],
    ["asc_eng_v", "Объем: по возрастанию"],
    ["desc_eng_v", "Объем: по убыванию"],
    ["asc_year", "Год: по возрастанию"],
    ["desc_year", "Год: по убыванию"],
    ["asc_auc_date", "Дата аукциона: по возрастанию"],
    ["desc_auc_date", "Дата аукциона: по убыванию"],
]

$(document).ready(function () {
    updateModels()

    updateClearButton()

    connectSelects()

    updateOrderingParam()

    $('#searchForm').submit(function (e) {
        e.preventDefault()
        const newParams = $('#searchForm').serialize().split('&').filter(e => e.split('=')[0] != 'csrfmiddlewaretoken');
        const url = new URL(window.location.href);
        newParams.forEach(e => url.searchParams.set(e.split('=')[0], e.split('=')[1]))

        url.searchParams.set('page', '1')

        window.history.pushState({}, '', url);
        window.location.reload();
    });

    function updateClearButton() {
        const newParams = $('#searchForm').serialize().split('&').filter(e => e.split('=')[0] != 'csrfmiddlewaretoken');
        const is_visible = newParams.some(e => e.split('=')[1])
        if (is_visible) {
            $(".search-form .form-buttons a").css("visibility", "visible");
        } else {
            $(".search-form .form-buttons a").css("visibility", "hidden");
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

const updateOrderingParam = () => {
    const dropdown = document.getElementById("ordering-dropdown");
    const button = dropdown.querySelector('.ordering__filter-select--btn');

    const params = new URLSearchParams(document.location.search);
    const currentText = orderingParams.find(e => e[0] ===  params.get("ordering"));

    if (currentText !== undefined) {
        button.textContent = currentText[1];
    } else {
        button.textContent = orderingParams[0][1];
    }

}

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
    input.value = value !== 'None' ? value : '';

    // Выбор кнопки для изменения текста
    let button = dropdown.querySelector('.catalog__filter-select--btn');

    if (value !== "" && value !== 'None') {
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


const mobileFormOpenClick = () => {
    const searchForm = document.querySelector(".search-form");

    searchForm.style.visibility = 'visible'
}

const mobileFormCloseClick = () => {
    const searchForm = document.querySelector(".search-form");

    searchForm.style.visibility = 'hidden'
}

function checkScreenSize() {
    const searchForm = document.querySelector(".search-form");
    if (window.innerWidth <= 992) {
        searchForm.style.visibility = 'hidden';
    } else {
        searchForm.style.visibility = 'visible';
    }
}

checkScreenSize();

window.addEventListener('resize', checkScreenSize);