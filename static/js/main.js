document.addEventListener('DOMContentLoaded', function () {
    const navbarToggler = document.querySelector('.navbar-toggler');
    const navbarCollapse = document.getElementById('navbarNav');


    if (navbarToggler && navbarCollapse) {
        navbarToggler.addEventListener('click', function () {
            const isExpanded = this.getAttribute('aria-expanded') === 'true';
            console.log('Navbar toggled', isExpanded);
        });

        navbarCollapse.addEventListener('hidden.bs.collapse', function () {
            console.log('Navbar collapsed');
        });
    }
});
// slider logic
document.addEventListener('DOMContentLoaded', function () {
    const slider = document.querySelector('.slider');
    const slides = document.querySelectorAll('.slide');
    const leftArrow = document.querySelector('.arrow-left');
    const rightArrow = document.querySelector('.arrow-right');
    let currentSlide = 0;
    let slideInterval;

    function goToSlide(n) {
        slider.style.transform = `translateX(-${n * 33.333}%)`;
        currentSlide = n;
    }

    function nextSlide() {
        currentSlide = (currentSlide + 1) % slides.length;
        goToSlide(currentSlide);
    }

    function prevSlide() {
        currentSlide = (currentSlide - 1 + slides.length) % slides.length;
        goToSlide(currentSlide);
    }

    function startSlider() {
        slideInterval = setInterval(nextSlide, 5000);
    }

    function pauseSlider() {
        clearInterval(slideInterval);
    }

    rightArrow.addEventListener('click', () => {
        pauseSlider();
        nextSlide();
        startSlider();
    });

    leftArrow.addEventListener('click', () => {
        pauseSlider();
        prevSlide();
        startSlider();
    });

    slider.addEventListener('mouseenter', pauseSlider);
    slider.addEventListener('mouseleave', startSlider);

    startSlider();
});

// number counter
document.addEventListener('DOMContentLoaded', function () {
    const statBoxes = document.querySelectorAll('.stat-box');

    function animateCount(el, target) {
        let count = 0;
        const increment = Math.ceil(target / 100);
        const interval = setInterval(() => {
            count += increment;
            if (count >= target) {
                count = target;
                clearInterval(interval);
            }
            el.textContent = count;
        }, 20);
    }

    const observer = new IntersectionObserver(entries => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const box = entry.target;
                const numberElement = box.querySelector('.stat-number');
                const targetValue = parseInt(numberElement.dataset.target);
                box.classList.add('animate');
                animateCount(numberElement, targetValue);
                observer.unobserve(box);
            }
        });
    }, {
        threshold: 0.5
    });

    statBoxes.forEach(box => observer.observe(box));
});
// footer toster 
document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("subscribeForm");
    const emailInput = document.getElementById("email");
    const toast = document.getElementById("toast");

    if (form && emailInput && toast) {
        form.addEventListener("submit", function (e) {
            e.preventDefault();

            const email = emailInput.value.trim();

            if (!email) return;
            localStorage.setItem("subscribedEmail", email);
            toast.style.display = "block";
            setTimeout(() => {
                toast.style.display = "none";
            }, 3000);
            emailInput.value = "";
        });
    }
});