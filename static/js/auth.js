   function login() {
       const username = document.getElementById("username").value;
       const password = document.getElementById("password").value;
       const msg = document.getElementById("message");
       fetch("/login", {
               method: "POST",
               headers: {
                   "Content-Type": "application/json"
               },
               body: JSON.stringify({
                   username,
                   password
               }),
               credentials: "include"
           })
           .then(res => {
               if (!res.ok) {
                   throw new Error("Network response was not ok");
               }
               return res.json();
           })
           .then(data => {
               msg.innerText = data.message;
               if (data.success) {
                   msg.style.color = "green";
                   localStorage.setItem("adminLoggedIn", "true");
                   localStorage.setItem("adminName", username);
                   window.location.href = data.redirect || "/dashboard";
               } else {
                   msg.style.color = "red";
               }
           })
           .catch(error => {
               msg.innerText = "Login failed. Please try again.";
               msg.style.color = "red";
               console.error("Error:", error);
           });
   }
   localStorage.clear();