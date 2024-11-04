document.querySelectorAll('.delivery__form-select-menu > li >.dropdown-item--region').forEach(item => {
    item.addEventListener('click', () => {
        // document.querySelector('.delivery__form-select--map > .delivery__btn-text').style.color = "rgb(0,0,0) !important"
        document.querySelector('.delivery__form-select--map > .delivery__btn-text').setAttribute('style', `color:rgb(0,0,0) !important`)
        document.querySelector('.delivery__form-select--map > .delivery__btn-text').innerHTML = item.dataset.value
        Click(item)
    })
})

document.querySelectorAll('.delivery__form-select-menu > li > .dropdown-item--cars').forEach(item => {
    item.addEventListener('click', () => {
        document.querySelector('.delivery__form-select--auto > .delivery__btn-text').setAttribute('style', `color:rgb(0,0,0) !important`)
        document.querySelector('.delivery__form-select--auto > .delivery__btn-text').innerHTML = item.dataset.value
        Click(item)
    })
})

let valuesDelivery = {}

let Click = (elem) => {
    elem.dataset.name
    elem.dataset.value
    valuesDelivery[elem.dataset.name] = elem.dataset.value
    console.log(valuesDelivery);
    let car = valuesDelivery.car
    let region = valuesDelivery.region
    if (valuesDelivery.car != undefined & valuesDelivery.region != undefined) {
        console.log('start');
        document.querySelector('.delivery--count').innerHTML = dataDelivery.data[region][car]
        document.querySelector('.delivery--date').innerHTML = dataDelivery.data[region].delivery_time
        od.update(dataDelivery[region][car])

    }
}

od = new Odometer({
    el: document.querySelector('.delivery--count'),
    value: 0,

    // Остальные опции передаются в этом же объекте
    format: '( ddd)',
    // theme: 'digital'
});

let Scroll = (mainRegion, mainCar) => {
    if (mainRegion != null & mainCar != null) {

        const element = document.querySelector('.delivery');
        const s = 250; // Добавляется отступ для оптимизации прокрутки!
        const elementPosition = element.getBoundingClientRect().top;
        const offsetPosition = elementPosition + window.pageYOffset - s;

        window.scrollTo({
            top: offsetPosition,
            behavior: 'smooth'
        });

        document.querySelector('.delivery__form-select--auto > .delivery__btn-text').innerHTML = mainCar
        document.querySelector('.delivery__form-select--map > .delivery__btn-text').innerHTML = mainRegion
        document.querySelector('.delivery--count').innerHTML = dataDelivery.data[mainRegion][mainCar]
        od.update(dataDelivery[mainRegion][mainCar])
    }
}

let mainRegion = null
let mainCar = null

document.querySelectorAll('.main__form-select--menu--auto > li > .dropdown-item--cars').forEach(item => {
    item.addEventListener('click', () => {
        document.querySelector('.main__form-select--auto > .main__form-select--button > .main__dropdown-text').setAttribute('style', `color:rgb(0,0,0) !important`)
        document.querySelector('.main__form-select--auto > .main__form-select--button > .main__dropdown-text').innerHTML = item.dataset.value
        mainCar = item.dataset.value
    })
})

document.querySelectorAll('.main__form-select--menu--region > li > .dropdown-item--region').forEach(item => {
    item.addEventListener('click', () => {
        document.querySelector('.main__form-select--region > .main__form-select--button > .main__dropdown-text').setAttribute('style', `color:rgb(0,0,0) !important`)
        document.querySelector('.main__form-select--region > .main__form-select--button > .main__dropdown-text').innerHTML = item.dataset.value
        mainRegion = item.dataset.value
    })
})

document.querySelector('.main__form-button').addEventListener('click', () => {
    Scroll(mainRegion, mainCar)
})