// let loginForm =document.getElementById("loginForm")
// if(loginForm){
//     loginForm.addEventListener("submit",function(e){
//  e.preventDefault();

//      let submit=document.querySelector(".submit")
//      submit.classList.add("disabled")

//      let hasError=false
//     let username=document.getElementById("username").value.trim()
//     let password=document.getElementById("password").value.trim()

//     let usernameError=document.getElementById("usernameError")
//     let passwordError=document.getElementById("passwordError")

//     usernameError.innerHTML = " ";
//     passwordError.innerHTML = " ";
    

//     if (username===''){
//         usernameError.innerHTML="Username is required"
//         hasError=true
//     }
//      if(password===''){
//         passwordError.innerHTML="Password is required"
//         hasError=true

//     }


// if(!hasError){
//     loginForm.submit()
// }else{
//     submit.classList.remove("disabled");
// }

// })
// }

// // validation of signup
// let signupForm =document.getElementById("signupForm")
// if (signupForm){
//     signupForm.addEventListener("submit",function(e){
//         //  e.preventDefault()    
//     let submit=document.querySelector(".submit")
//     submit.classList.add("disabled")
//     let username=document.getElementById("username").value.trim()
//     let password=document.getElementById("password").value.trim()
//     let confirmPassword=document.getElementById("confirmPassword").value.trim()
//     let country=document.getElementById("country").value.trim()

//     let usernameError=document.getElementById("usernameError")
//     let passwordError=document.getElementById("passwordError")
//     let confirmPasswordError=document.getElementById("confirmPasswordError")
//     let countryError=document.getElementById('countryError')
  
    
//     usernameError.innerHTML= " ";
//     passwordError.innerHTML= " ";
//     countryError.innerHTML=" ";
//     confirmPasswordError.innerHTML = " ";

//     let isValid=true

//     if ( username ===''||username.length<=1){
//         usernameError.innerHTML="Invalid Name"
//         isValid=false
//     }
//      if(password===''||password.length<=6){
//         passwordError.innerHTML="Invalid password"
//         isValid=false
//     }
//     if(country===''){
//        countryError.innerHTML="please Enter your country"
//         isValid=false
// }
// if (confirmPassword!==password){
// confirmPasswordError.innerHTML="password  does not match" 
// isValid=false
// }
// if (isValid){
//     localStorage.setItem("username",username)
//     localStorage.setItem("password",password)
//     localStorage.setItem("country",country)
//     alert("data saved successfuly")
     
   
// }
// else {
//             e.preventDefault();
//             submit.classList.remove("disabled");
//         }

// })
// }

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