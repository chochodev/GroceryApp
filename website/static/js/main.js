const closeMessagesBtn = document.getElementById('flashed-messages-close-btn');
const parentCloseMessagesBtn = closeMessagesBtn.parentNode;

// Removes Flashed messages on click of the close button
closeMessagesBtn.addEventListener('click', () => {
    parentCloseMessagesBtn.remove();
});

// Removes Flashed messages after 5 seconds (5000 milliseconds)
setTimeout(() => {
    parentCloseMessagesBtn.remove();
}, 5000);