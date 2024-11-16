

const changeCurrency = (event) => {
    const prices = Array.from(document.querySelectorAll(".car-info .price div"));

    if (event.currentTarget.checked) {
        prices[0].style.display = 'none'
        prices[1].style.display = 'block'
    } else {
        prices[0].style.display = 'block'
        prices[1].style.display = 'none'
    }
}

const openPriceModal = (event, text) => {
    event?.stopPropagation();
    event?.preventDefault();
    const modal = document.querySelector('.modal_price_back')
    modal.style.visibility = 'visible';
    modal.classList.add('show');
}

const closePriceModal = () => {
    const modal = document.querySelector('.modal_price_back')
    modal.classList.remove('show');

    setTimeout(() => {
        modal.style.visibility = 'hidden';
    }, 500);
}
