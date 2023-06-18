const closeMessagesBtn = document.getElementById('flashed-messages-close-btn');
const parentCloseMessagesBtn = closeMessagesBtn?.parentNode;

// Check if closeMessagesBtn exists before attaching event listeners and removing it
if (closeMessagesBtn && parentCloseMessagesBtn) {
    // Removes Flashed messages on click of the close button
    closeMessagesBtn.addEventListener('click', () => {
        parentCloseMessagesBtn.remove();
    });

    // Removes Flashed messages after 5 seconds (5000 milliseconds)
    setTimeout(() => {
        parentCloseMessagesBtn.remove();
    }, 5000);
}

//---------------------- FOR HANDLING MENU BAR TOGGLE ON SMALL SCREEN
const bgOverlay = document.getElementById('signing-background-overlay');

// REMOVE STYLES AT VIEWPORT
if (window.innerWidth > 680) {
    bgOverlay.classList.remove('show-signing-background-overlay');
}

// FOR THE TOGGLING TO MENUBAR TOGGLE MENU LIST

const menubarBtn = document.getElementById('menu-bar-btn');
const barsIcon = document.getElementById('bars-icon');
const closeIcon = document.getElementById('close-icon');
const menuContent = document.getElementById('nav-contents');
const menuLinks = document.querySelectorAll('.link');


window.addEventListener('DOMContentLoaded', function() { 
    myArray = [barsIcon, closeIcon, menuContent];

    [menubarBtn, ...menuLinks, bgOverlay].forEach(clickItem => {
        clickItem.addEventListener('click', () => {
            myArray.forEach(item => {
                console.log('works!!')
                item.classList.toggle('close');
                bgOverlay.classList.toggle('show-signing-background-overlay');
                applyFunctionBasedOnWidth();
            });
        });
    });

    // FOR SHOWING THE BACKGROUND OVERLAY 
    function applyFunctionBasedOnWidth() {
      if (window.innerWidth > 680 && !menubarBtn.classList.contains('close')) {
        bgOverlay.classList.remove('show-signing-background-overlay');
        menuContent.classList.add('close');
        barsIcon.classList.remove('close');
        closeIcon.classList.add('close');
      } else if (window.innerWidth < 680 && menubarBtn.classList.contains('close')) {
        bgOverlay.classList.add('show-signing-background-overlay');
      }
    }
  
    // Call the function when the page loads
    applyFunctionBasedOnWidth();
  
    // Call the function on window resize
    window.addEventListener('resize', applyFunctionBasedOnWidth);
});
