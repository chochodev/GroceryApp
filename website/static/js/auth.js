const bgOverlay = document.getElementById('signing-background-overlay');

const signup = document.getElementById('signup');
const signin = document.getElementById('signin');

const signupButton = document.querySelectorAll('.signup-button');
const signinButton = document.querySelectorAll('.signin-button');


// FOR TOGGLING THE FORMS

[...signupButton].forEach(clickItem => {
    clickItem.addEventListener('click', () => {
        signup.classList.add('un-signup');
        signin.classList.remove('un-signin');
        updateBackgroundOverlay();
    });
});

[...signinButton].forEach(clickItem => {
    clickItem.addEventListener('click', () => {
        signin.classList.add('un-signin');
        signup.classList.remove('un-signup');
        updateBackgroundOverlay();
    });
});

// REMOVE STYLES AT VIEWPORT
if (window.innerWidth > 768) {
    bgOverlay.classList.remove('show-signing-background-overlay');
    console.log('above viewport')
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
                console.log('works!!')
                item.classList.toggle('close');
                bgOverlay.classList.toggle('show-signing-background-overlay');
                applyFunctionBasedOnWidth();
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
        console.log('Above viewport');
      } else if (window.innerWidth < 768 && menubarBtn.classList.contains('close')) {
        bgOverlay.classList.add('show-signing-background-overlay');
      }
    }
  
    // Call the function when the page loads
    applyFunctionBasedOnWidth();
  
    // Call the function on window resize
    window.addEventListener('resize', applyFunctionBasedOnWidth);
});