// // Mobile menu toggle
// document.addEventListener("DOMContentLoaded", function() {
//   const menuToggle = document.getElementById("menu-toggle");
//   const navLinks = document.getElementById("nav-links");

//   menuToggle.addEventListener("click", () => {
//     navLinks.classList.toggle("active");
//   });

//   // Optional: close menu when clicking outside
//   document.addEventListener("click", (e) => {
//     if (!menuToggle.contains(e.target) && !navLinks.contains(e.target)) {
//       navLinks.classList.remove("active");
//     }
//   });
// });
document.addEventListener("DOMContentLoaded", () => {
  const menuToggle = document.createElement("button");
  menuToggle.classList.add("menu-toggle");
  menuToggle.innerHTML = "☰";

  const header = document.querySelector(".header");
  const nav = document.querySelector(".nav");

  // Insert button only if .nav exists
  if (header && nav) {
    header.insertBefore(menuToggle, nav);

    menuToggle.addEventListener("click", () => {
      nav.classList.toggle("active");
    });

    // Close menu when clicking outside
    document.addEventListener("click", (e) => {
      if (!header.contains(e.target)) {
        nav.classList.remove("active");
      }
    });
  }
});
