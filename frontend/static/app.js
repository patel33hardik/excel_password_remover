// JavaScript to toggle the "active" class
const menuItems = document.querySelectorAll('.menu-item');

menuItems.forEach(item => {
    item.addEventListener('click', () => {
        // Remove "active" class from all menu items
        menuItems.forEach(otherItem => {
            otherItem.classList.remove('active');
        });

        // Add "active" class to the clicked menu item
        item.classList.add('active');
    });
});