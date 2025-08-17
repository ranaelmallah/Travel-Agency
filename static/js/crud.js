(function () {
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
// read data from localstorage 
document.addEventListener("DOMContentLoaded", () => {
    const adminName = localStorage.getItem("adminName");

    if (adminName) {
        document.getElementById("welcome-message").innerText = `Welcome ${adminName}`;
    } else {

        window.location.href = "/login";
    }
});
document.addEventListener("DOMContentLoaded", () => {
    const flashMessages = document.querySelectorAll('.alert');
    if (flashMessages.length) {
        setTimeout(() => {
            flashMessages.forEach(msg => {
                msg.style.transition = "opacity 0.5s";
                msg.style.opacity = "0";
                setTimeout(() => msg.remove(), 500);
            });
        }, 10000);
    }
});

document.addEventListener("DOMContentLoaded", () => {
    const flashContainer = document.getElementById("flash-messages");

    document.querySelectorAll(".delete-btn").forEach(button => {
        button.addEventListener("click", () => {
            const tripId = button.getAttribute("data-id");

            if (!confirm("Are you sure you want to delete this trip?")) return;

            fetch(`/delete/${tripId}`, {
                    method: "DELETE"
                })
                .then(res => res.json())
                .then(data => {
                    // show flash message
                    const alert = document.createElement("div");
                    alert.className = `alert alert-${data.status === "success" ? "success" : "danger"}`;
                    alert.innerText = data.message;
                    flashContainer.appendChild(alert);

                    setTimeout(() => alert.remove(), 3000);

                    if (data.status === "success") {
                        button.closest(".trip-card").remove();
                    }
                })
                .catch(err => {
                    console.error("Delete error:", err);
                });
        });
    });
});