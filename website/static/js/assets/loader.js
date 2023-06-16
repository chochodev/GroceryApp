document.addEventListener("DOMContentLoaded", function() {
    const loader = document.querySelector(".custom-loader-bg");
    loader.style.display = "none"; // Hide the loader initially
    
    window.addEventListener("load", function() {
      loader.style.display = "none"; // Hide the loader when the page is fully loaded
    });
});
  