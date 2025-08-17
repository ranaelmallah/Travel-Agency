 document.getElementById('bookingForm').addEventListener('submit', function (event) {
     let valid = true;
     const name = this.querySelector('input[name="name"]').value.trim();
     const email = this.querySelector('input[name="email"]').value.trim();
     const phone = this.querySelector('input[name="phone"]').value.trim();
     const address = this.querySelector('input[name="address"]').value.trim();


     // Empty check
     if (!name || !email || !phone || !address) {
         alert("All fields are required!");
         valid = false;
     }

     // Name validation
     if (!/^[A-Za-z\s]{3,}$/.test(name)) {
         alert("Name must be at least 3 letters and contain only letters and spaces.");
         valid = false;
     }

     // Phone validation
     if (!/^\d{7,}$/.test(phone)) {
         alert("Phone number must be at least 7 digits and numbers only.");
         valid = false;
     }

     // Email validation
     if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
         alert("Please enter a valid email address.");
         valid = false;
     }

     // Address validation
     if (address.length < 5) {
         alert("Address must be at least 5 characters long.");
         valid = false;
     }

     if (!valid) {
         event.preventDefault();
     }
 });