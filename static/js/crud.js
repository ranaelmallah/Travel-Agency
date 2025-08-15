(function() {
    'use strict';
    const forms = document.querySelectorAll('.needs-validation');
    
    Array.from(forms).forEach(form => {
        form.addEventListener('submit', event => {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });
})();

document.addEventListener("DOMContentLoaded", () => {
    const adminName = localStorage.getItem("adminName");

    if (adminName) {
        document.getElementById("welcome-message").innerText = `Welcome ${adminName}`;
    } else {
        // If not logged in, send back to login page
        window.location.href = "/login";
    }
});
