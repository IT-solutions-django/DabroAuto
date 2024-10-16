window.onload = (function () {


    let mainSlides = document.querySelectorAll(".main-slides > .gallery-slide");
    let thumbnailSlidesParent = document.querySelector(".thumbnail-slides");
    let mainSlidesCount = mainSlides.length;
    let actionButtons = document.querySelectorAll(
      ".main-slides > .slider-controller-button"
    );
    let slidesCount = document.querySelector(".all-slides-count");
    let slideCountCurr = document.querySelector(".curr-slide-count");
    let previousSlideButton = document.querySelector(".previous-slide-button");
    let nextSlideButton = document.querySelector(".next-slide-button");

    let countTumbaiSlides = 6

    let remains = mainSlidesCount - countTumbaiSlides

    // ### Initializing the slider ###
    // (function () {
      if (mainSlidesCount >= 2) {
        slideCountCurr.innerText = 1;
        slidesCount.innerText = mainSlidesCount;
        if (mainSlidesCount >= countTumbaiSlides) {
          initializeThumbnailSlidesStart();
        } else {
          initializeThumbnailSlides()
        }

        actionButtons.forEach(function (currButton) {
          currButton.style.display = "block";
        });
      }
    // })();

    // Creates and attaches bottom thumbnail images for main slides
    function initializeThumbnailSlidesStart() {
      for (let i = 0; i < countTumbaiSlides ; i++) {
        var createImage = document.createElement("img");
        createImage.src = mainSlides[i].src;
        createImage.classList = mainSlides[i].classList;
        createImage.classList.remove("gallery-slide");
        createImage.classList += " gallery-slide-thumbnail";
        createImage.width = 96;
        createImage.height = 90;
        if (i === countTumbaiSlides - 1) {
          var createWrapper = document.createElement("div");
          createWrapper.classList += " ACTIVE gallery-slide-wrapper"
          createWrapper.appendChild(createImage)
          if (remains >= 1) {
            createWrapper.innerHTML += `<p class="remains">+${remains}</p>`
          }
          thumbnailSlidesParent.appendChild(createWrapper)
        } else {
          thumbnailSlidesParent.appendChild(createImage);
        }
      }
    }

    function initializeThumbnailSlidesEnd() {
      document.querySelector('.thumbnail-slides').innerHTML = " "
      let currentSliderImage = currSliderImagePos();
      hideSlide(currentSliderImage)
      showSlide(countTumbaiSlides - 1)
      for (let i = 0; i < mainSlidesCount; i++) {
        var createImage = document.createElement("img");
        createImage.src = mainSlides[i].src;
        createImage.classList = mainSlides[i].classList;
        createImage.classList.remove("gallery-slide");
        createImage.classList.remove("ACTIVE");
        createImage.classList += " gallery-slide-thumbnail";
        createImage.width = 96;
        createImage.height = 90;
        thumbnailSlidesParent.appendChild(createImage);
      }
    }

    function initializeThumbnailSlides() {
      document.querySelector('.thumbnail-slides').innerHTML = " "
      for (let i = 0; i < mainSlidesCount; i++) {
        var createImage = document.createElement("img");
        createImage.src = mainSlides[i].src;
        createImage.classList = mainSlides[i].classList;
        createImage.classList.remove("gallery-slide");
        createImage.classList.remove("ACTIVE");
        createImage.classList += " gallery-slide-thumbnail";
        createImage.width = 96;
        createImage.height = 90;
        thumbnailSlidesParent.appendChild(createImage);
      }
    }
    // ### THE END OF ### Initializing the slider

    // Determining current displaying image position in `mainSlides` array
    function currSliderImagePos() {
      for (let i = 0; i < document.querySelectorAll('.main-slides > .CORRECT').length; i++) {
        if (
          window.getComputedStyle(document.querySelectorAll('.main-slides > .CORRECT')[i]).display !== "none" &&
          typeof document.querySelectorAll('.main-slides > .CORRECT')[i] !== "undefined"
        ) {
          return i;
        }
      }
      return false;
    }

    // Determining previous displaying image position in `mainSlides` array
    function prevSliderImagePos(pos) {
      if (pos >= 0 && typeof mainSlides[pos - 1] !== "undefined") {
        return pos - 1;
      }
      return false;
    }

    // Determining next displaying image position in `mainSlides` array
    function nextSliderImagePos(pos) {
      if (pos >= 0 && typeof mainSlides[pos + 1] !== "undefined") {
        return pos + 1;
      }
      return false;
    }

    function hideSlide(currSlide, duration) {
      // thumbnailSlides[currSlide].style.border = "none";
      // mainSlides[currSlide].style.opacity = 0;
      document.querySelectorAll('.main-slides > .CORRECT')[currSlide].style.display = "none";
      setTimeout(function () {}, duration);
    }

    function showSlide(nextSlide, duration) {
      // mainSlides[nextSlide].style.opacity = 1;
      document.querySelectorAll('.main-slides > .CORRECT')[nextSlide].style.display = "block";
      setTimeout(function () {}, duration);
    }

    let thumbnailSlides = document.querySelectorAll(
      ".thumbnail-slides > .gallery-slide-thumbnail"
    );

    nextSlideButton.addEventListener("click", function () {
      let currentSliderImage = currSliderImagePos();
      let nextSliderImage = nextSliderImagePos(currentSliderImage);
      let imageTransitionDuration =
        window
          .getComputedStyle(mainSlides[currentSliderImage])
          .transitionDuration.replace("s", "") * 1000;

      if (currentSliderImage !== false && nextSliderImage !== false) {
        hideSlide(currentSliderImage, imageTransitionDuration);
      }

      if (nextSliderImage !== false) {
        slideCountCurr.innerText =
          nextSliderImage <= mainSlides.length
            ? nextSliderImage + 1
            : mainSlides.length;
        showSlide(nextSliderImage, imageTransitionDuration);
      }
    });

    previousSlideButton.addEventListener("click", function () {
      let currentSliderImage = currSliderImagePos();
      let prevSliderImage = prevSliderImagePos(currentSliderImage);
      let imageTransitionDuration =
        window
          .getComputedStyle(mainSlides[currentSliderImage])
          .transitionDuration.replace("s", "") * 1000;

      if (currentSliderImage !== false && prevSliderImage !== false) {
        hideSlide(currentSliderImage, imageTransitionDuration);
      }

      if (prevSliderImage !== false) {
        slideCountCurr.innerText =
          prevSliderImage <= mainSlides.length
            ? currentSliderImage
            : mainSlides.length;
        showSlide(prevSliderImage, imageTransitionDuration);
      }
    });

    let changeSlide = document.querySelector(".thumbnail-slides");

    changeSlide.addEventListener("click", function (e) {
      if (e.target.tagName === "IMG") {
        let clickedImagePos = Array.prototype.indexOf.call(
          e.currentTarget.children,
          e.target
        );
        let currentSliderImage = currSliderImagePos();
        let imageTransitionDuration =
          window
            .getComputedStyle(mainSlides[0])
            .transitionDuration.replace("s", "") * 1000;

        if (currentSliderImage !== false) {
          hideSlide(currentSliderImage, imageTransitionDuration);
          console.log(currentSliderImage);
        }

        if (clickedImagePos >= 0) {
          slideCountCurr.innerText =
            currentSliderImage <= mainSlides.length
              ? clickedImagePos + 1
              : mainSlides.length;
          showSlide(clickedImagePos, imageTransitionDuration);
        }
        // console.log(clickedImagePos);
      }

    });

    let clickSlide = document.querySelectorAll(".main-slides > .gallery-slide")
    let correctSlide = document.querySelectorAll(".main-slides > .CORRECT")
    let modalGallery = document.querySelector(".modal-gallery")
    let modalGallerySlider = document.querySelector(".modal-gallery > .modal-gallery-main > .modal-gallery-slider")
    let modalThumbnail = document.querySelector('.modal-thumbnail')

    for (let i = 0; i < correctSlide.length; i++) {
      let createImg = document.createElement('img')
      createImg.src = correctSlide[i].src
      createImg.classList = `modal-gallery-slide modal-slide-${i}`
      modalGallerySlider.appendChild(createImg)
    }

    if (correctSlide.length >= 2) {
        for (let i = 0; i < correctSlide.length; i++) {
        let createImg = document.createElement('img')
        createImg.src = correctSlide[i].src
        createImg.setAttribute('data-number', `${i}`)
        createImg.classList = `modal-thumbnail-slide thumbnail-slide-${i}`
        modalThumbnail.appendChild(createImg)
      }
    }

    function hideModalSlide(currSlide, duration) {
      document.querySelector(`.modal-slide-${currSlide}`).style.display = 'none'
      setTimeout(function () {}, duration);
    }

    function showModalSlide(nextSlide, duration) {
      document.querySelector(`.modal-slide-${nextSlide}`).style.display = 'block'
      setTimeout(function () {}, duration);
    }

    function prevModalSliderImagePos(pos) {
      console.log(typeof document.querySelectorAll('.modal-gallery-slider > .modal-gallery-slide')[pos - 1]);
      if (pos >= 0 && typeof document.querySelectorAll('.modal-gallery-slider > .modal-gallery-slide')[pos - 1] !== "undefined") {
        return pos - 1;
      }
      return false;
    }

    // Determining next displaying image position in `mainSlides` array
    function nextModalSliderImagePos(pos) {
      if (pos >= 0 && typeof document.querySelectorAll('.modal-gallery-slider > .modal-gallery-slide')[pos + 1] !== "undefined") {
        return pos + 1;
      }
      return false;
    }


    function currModalSliderImagePos() {
      for (let i = 0; i < document.querySelectorAll('.modal-gallery-slider > .modal-gallery-slide').length; i++) {
        if (
          window.getComputedStyle(document.querySelectorAll('.modal-gallery-slider > .modal-gallery-slide')[i]).display !== "none" &&
          typeof document.querySelectorAll('.modal-gallery-slider > .modal-gallery-slide')[i] !== "undefined"
        ) {
          return i;
        }
      }
      return false;
    }

    document.querySelector('.modal-gallery-btn--close').addEventListener('click', () => {
      let currentSliderImage = currModalSliderImagePos ()
      hideModalSlide(currentSliderImage)
      modalGallery.style.display = 'none'
      document.querySelectorAll('.modal-thumbnail-slide').forEach((item) => {
          item.classList.remove('modal-thumbnail-slide--active')
      })
    })

    clickSlide.forEach(item => {
      item.addEventListener('click', () => {
        let currentSliderImage = currSliderImagePos();
        document.querySelectorAll('.modal-thumbnail-slide')[currentSliderImage].classList.add('modal-thumbnail-slide--active')
        modalGallery.style.display = 'block'
        showModalSlide(currentSliderImage)
    })})

    document.querySelectorAll('.modal-thumbnail-slide').forEach((item) => {
      item.addEventListener('click', (e) => {
        let currentSliderImage = currModalSliderImagePos();
        document.querySelectorAll('.modal-thumbnail-slide').forEach((item) => {
          item.classList.remove('modal-thumbnail-slide--active')
        })
        e.target.classList.add('modal-thumbnail-slide--active')
        let clickedImagePos = parseInt(e.target.dataset.number)
        hideModalSlide(currentSliderImage)
        showModalSlide(clickedImagePos)
      })
    })

    document.querySelector('.modal-gallery-btn--next').addEventListener('click', () => {
      let currentSliderImage = currModalSliderImagePos();
      let nextSlide = nextModalSliderImagePos(currentSliderImage)
      document.querySelectorAll('.modal-thumbnail-slide').forEach((item) => {
          item.classList.remove('modal-thumbnail-slide--active')
      })
      document.querySelectorAll('.modal-thumbnail-slide')[nextSlide].classList.add('modal-thumbnail-slide--active')
      showModalSlide(nextSlide)
      hideModalSlide(currentSliderImage)

    })

    document.querySelector('.modal-gallery-btn--prev').addEventListener('click', () => {
      let currentSliderImage = currModalSliderImagePos();
      let prevSlide = prevModalSliderImagePos(currentSliderImage)
      document.querySelectorAll('.modal-thumbnail-slide').forEach((item) => {
          item.classList.remove('modal-thumbnail-slide--active')
      })
      document.querySelectorAll('.modal-thumbnail-slide')[prevSlide].classList.add('modal-thumbnail-slide--active')
      showModalSlide(prevSlide)
      hideModalSlide(currentSliderImage)

    })

    console.log(typeof document.querySelector('.thumbnail-slides > .ACTIVE') != 'undefind');

    if (typeof document.querySelector('.thumbnail-slides > .ACTIVE') != 'undefind') {
      document.querySelector('.thumbnail-slides > .ACTIVE').addEventListener('click', () => {
        initializeThumbnailSlidesEnd()
      })
    }
})