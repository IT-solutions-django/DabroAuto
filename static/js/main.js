var swiper = new Swiper(".cars1 .mySwiperl", {
    slidesPerView: 'auto',
    spaceBetween: 16,
    pagination: {
      clickable: true,
    },
    navigation: {
      nextEl: ".cars1 .swiper_next",
      prevEl: ".cars1 .swiper_prev",
    },
    breakpoints: {
      0: {
        spaceBetween: 12,
      },
      768: {
        spaceBetween: 16,
      }
    },
});
var swiper = new Swiper(".cars3 .mySwiperl", {
    slidesPerView: 'auto',
    spaceBetween: 16,
    pagination: {
      clickable: true,
    },
    navigation: {
      nextEl: ".cars3 .swiper_next",
      prevEl: ".cars3 .swiper_prev",
    },
    breakpoints: {
      0: {
        spaceBetween: 12,
      },
      768: {
        spaceBetween: 16,
      }
    },
});

  var swiper = new Swiper(".cars2 .mySwipert", {
    slidesPerView: 'auto',
    spaceBetween: 16,
    pagination: {
      clickable: true,
    },
    navigation: {
      nextEl: ".cars2 .swiper_next",
      prevEl: ".cars2 .swiper_prev",
    },
  });


var swiper = new Swiper(".mySwiper", {
    pagination: {
      el: ".swiper-pagination",
      clickable: true,
    },
  });

$(function() {
  $('.marquee').marquee({
    duration: 20000,
    gap: 0,
    startVisible: true,
    duplicated: true
  });
});


const track = document.querySelector('.logo-track');
const logos = document.querySelectorAll('.logo-track img');

// Duplicating logos for seamless scrolling
if (track?.innerHTML) {
    track.innerHTML += track.innerHTML;
    track.style.width = `${logos.length * 200}px`
}


const track2 = document.querySelector('.logo-track');
const logos2 = document.querySelectorAll('.logo-track img');

// Duplicating logos for seamless scrolling
if (track2?.innerHTML) {
    track2.innerHTML += track2.innerHTML;
    track2.style.width = `${logos2.length * 200}px`
}


const swiper1 = new Swiper('.clips_swiper', {
  slidesPerView: 'auto',
  spaceBetween: 16,
  loop: true,
  centeredSlides: true,
  centeredSlidesBounds: true,
  breakpoints: {
    0: {
      spaceBetween: 8,
    },
    768: {
      spaceBetween: 16,
    }
  },
});

function addClassOnClick(clickableSelector, targetSelector, className) {
  const clickableElements = document.querySelectorAll(clickableSelector);
  const targetElement = document.querySelector(targetSelector);

  clickableElements.forEach(element => {
    element.addEventListener('click', function(e) {
      e.preventDefault()
      targetElement.classList.add(className);
    });
  });
}

function removeClassOnClick(clickableSelector, targetSelector, className) {
  const clickableElements = document.querySelectorAll(clickableSelector);
  const targetElement = document.querySelector(targetSelector);

  clickableElements.forEach(element => {
    element.addEventListener('click', function() {
      targetElement.classList.remove(className);
    });
  });
}


addClassOnClick('.card_discoint a', '.modal_', 'show');
addClassOnClick('.save_discount a ', '.modal_', 'show');
removeClassOnClick('.modal_back', '.modal_', 'show');
removeClassOnClick('.modal_ .close_modal', '.modal_', 'show');

var swiper = new Swiper(".comment_swiper", {
  slidesPerView: 'auto',
  grid: {
    rows: 2,
  },
  spaceBetween: 16,
  pagination: {
    el: ".swiper-pagination",
    clickable: true,
  },
  breakpoints: {
    0: {
      spaceBetween: 12,
    },
    768: {
      spaceBetween: 16,
    }
  },
});

document.querySelector('.hamburger').addEventListener('click', function(){
  document.querySelector('.header_menu').classList.toggle('open')
})

var telInputs = document.querySelectorAll('input[type=tel]');

if (telInputs.length > 0) {
    telInputs.forEach(function(input) {
        var phoneMask = IMask(input, {
            mask: "+{7} 000 000 00 00",
        });
    });
}

var swiper_main_card = new Swiper(".mySwiper-main-card", {
    pagination: {
      el: ".swiper-pagination-main-card",
      clickable: true,
    },
  });

var swiper_test = new Swiper(".cars-test .mySwiperl", {
    slidesPerView: 'auto',
    spaceBetween: 16,
    centeredSlides: true,
    pagination: {
      clickable: true,
    },
    navigation: {
      nextEl: ".cars-test .swiper_next",
      prevEl: ".cars-test .swiper_prev",
    },
    breakpoints: {
      0: {
        spaceBetween: 12,
      },
      768: {
        spaceBetween: 16,
      }
    },
    on: {
        slideChange: function () {
            swiper_main_card.forEach(e => e.slideTo(0))
            const currentIndex = swiper_test.activeIndex
            swiper_main_card[currentIndex].slides.slice(1).forEach(e => {
                e.style.visibility = 'hidden'
                setTimeout(() => {
                    e.style.visibility = 'visible'
                }, 800);
            })
        },
      }
});
