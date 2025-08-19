const form = document.getElementById('bookingForm');
const nameInput = form.querySelector('input[name="name"]');
const emailInput = form.querySelector('input[name="email"]');
const phoneInput = form.querySelector('input[name="phone"]');
const addressInput = form.querySelector('input[name="address"]');

//  showError 
function showError(input, message) {
    input.classList.add('is-invalid');
    input.nextElementSibling.textContent = message;
}

function clearError(input) {
    input.classList.remove('is-invalid');
    input.nextElementSibling.textContent = '';
}

nameInput.addEventListener('input', () => {
    const value = nameInput.value.trim();
    if (!/^[A-Za-z\s]{3,}$/.test(value)) {
        showError(nameInput, "Name must be at least 3 letters and contain only letters and spaces.");
    } else {
        clearError(nameInput);
    }
});

emailInput.addEventListener('input', () => {
    const value = emailInput.value.trim();
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value)) {
        showError(emailInput, "Please enter a valid email address.");
    } else {
        clearError(emailInput);
    }
});

phoneInput.addEventListener('input', () => {
    const value = phoneInput.value.trim();
    if (!/^\d{7,}$/.test(value)) {
        showError(phoneInput, "Phone number must be at least 7 digits.");
    } else {
        clearError(phoneInput);
    }
});

addressInput.addEventListener('input', () => {
    const value = addressInput.value.trim();

    if (value.length < 5) {
        showError(addressInput, "Address must be at least 5 characters long.");
    } else if (!/[A-Za-z]/.test(value)) {
        showError(addressInput, "Address must contain at least one letter and cannot be numbers only.");
    } else {
        clearError(addressInput);
    }
});

// flash timer 
const flashes = document.querySelectorAll('.flash-message');

flashes.forEach(flash => {
    setTimeout(() => {
        flash.style.transition = "opacity 0.5s";
        flash.style.opacity = "0";
        setTimeout(() => flash.remove(), 500);
    }, 2000);
});