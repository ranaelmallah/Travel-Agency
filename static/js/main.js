document.addEventListener('DOMContentLoaded', function() {
  const navbarToggler = document.querySelector('.navbar-toggler');
  const navbarCollapse = document.getElementById('navbarNav');

  navbarToggler.addEventListener('click', function() {
    const isExpanded = this.getAttribute('aria-expanded') === 'true';
    
    // Toggle icons
    const openIcon = this.querySelector('.navbar-toggler-icon-open');
    const closeIcon = this.querySelector('.navbar-toggler-icon-close');
    
    if (isExpanded) {
      openIcon.style.display = 'inline-block';
      closeIcon.style.display = 'none';
    } else {
      openIcon.style.display = 'none';
      closeIcon.style.display = 'inline-block';
    }
  });

  // Optional: Reset icon when collapsing via other means (e.g., clicking a link)
  navbarCollapse.addEventListener('hidden.bs.collapse', function() {
    const openIcon = navbarToggler.querySelector('.navbar-toggler-icon-open');
    const closeIcon = navbarToggler.querySelector('.navbar-toggler-icon-close');
    openIcon.style.display = 'inline-block';
    closeIcon.style.display = 'none';
  });
});

 document.addEventListener('DOMContentLoaded', function() {
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
            
            // Arrow click events
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
            
            // Pause on hover
            slider.addEventListener('mouseenter', pauseSlider);
            slider.addEventListener('mouseleave', startSlider);
            
            // Start the slider
            startSlider();
        });
//   document.querySelector('.close-btn').addEventListener('click', () => {
//   document.querySelector('.sidebar').style.display = 'none';
// });
    // window.addEventListener('scroll', function() {
    //     let navbar = document.querySelector('.custom-navbar');
    //     navbar.classList.toggle('scrolled', window.scrollY > 50);
    // });


     document.addEventListener('DOMContentLoaded', function() {
            // Animate stat boxes
            const statBoxes = document.querySelectorAll('.stat-box');
            statBoxes.forEach((box, index) => {
                setTimeout(() => {
                    box.classList.add('animate');
                }, 200 * index);
            });
            
           
            
            // Floating animation for stats
            setInterval(() => {
                statBoxes.forEach(box => {
                    box.classList.toggle('floating');
                });
            }, 3000);
        });
