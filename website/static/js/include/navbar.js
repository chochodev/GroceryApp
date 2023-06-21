const bgOverlay = document.getElementById('signing-background-overlay');


// REMOVE STYLES AT VIEWPORT
if (window.innerWidth > 768) {
    bgOverlay.classList.remove('show-signing-background-overlay');
}


// FOR THE TOGGLING TO MENUBAR TOGGLE MENU LIST

const menubarBtn = document.getElementById('menu-bar-btn');
const barsIcon = document.getElementById('bars-icon');
const closeIcon = document.getElementById('close-icon');
const menuList = document.getElementById('menu-list');
const menuLinks = document.querySelectorAll('.link');

window.addEventListener('DOMContentLoaded', function() { 
    myArray = [barsIcon, closeIcon, menuList];

    [menubarBtn, ...menuLinks, bgOverlay].forEach(clickItem => {
        clickItem.addEventListener('click', () => {
            myArray.forEach(item => {
                item.classList.toggle('close');
                bgOverlay.classList.toggle('show-signing-background-overlay');
                applyFunctionBasedOnWidth();
                // Closing the search bar on click 
                SearchBar.classList.remove('display-search-bar');
            });
        });
    });

    // FOR SHOWING THE BACKGROUND OVERLAY 
    function applyFunctionBasedOnWidth() {
      if (window.innerWidth > 768 && !menubarBtn.classList.contains('close')) {
        bgOverlay.classList.remove('show-signing-background-overlay');
        menuList.classList.add('close');
        barsIcon.classList.remove('close');
        closeIcon.classList.add('close');
      } else if (window.innerWidth < 768 && menubarBtn.classList.contains('close')) {
        bgOverlay.classList.add('show-signing-background-overlay');
      }
    }
  
    // Call the function when the page loads
    applyFunctionBasedOnWidth();
  
    // Call the function on window resize
    window.addEventListener('resize', applyFunctionBasedOnWidth);
});


// FOR TOGGLING SEARCH BAR ON SMALL SCREEN 
const toggleSearchBtn = document.getElementById('toggle-search-bar');
const SearchBar = document.getElementById('search-bar');

toggleSearchBtn.addEventListener('click', () => {
  SearchBar.classList.toggle('display-search-bar');
})
