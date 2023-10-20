// JavaScript to toggle the "active" class
const currentURL = window.location.pathname;
const menuItems = document.querySelectorAll('.menu li a');

menuItems.forEach((menuItem) => {
    if (menuItem.getAttribute('href') === currentURL) {
        menuItem.classList.add('active');
    }
});