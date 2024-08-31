/*!
* Start Bootstrap - Clean Blog v6.0.8 (https://startbootstrap.com/theme/clean-blog)
* Copyright 2013-2022 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-clean-blog/blob/master/LICENSE)
*/

const scriptElement = document.currentScript; // Get the current script element
const nav_bar_file = scriptElement.dataset.nav_bar_file;

document.addEventListener('DOMContentLoaded', (event) => {
  fetch(nav_bar_file)
    .then(response => response.text())
    .then(data => {
      document.getElementById('menu-container').innerHTML = data;

      let scrollPos = 0;
      const mainNav = document.getElementById('mainNav');
      const headerHeight = mainNav.clientHeight;
      window.addEventListener('scroll', function() {
        const currentTop = document.body.getBoundingClientRect().top * -1;
        if ( currentTop < scrollPos) {
          // Scrolling Up
          if (currentTop > 0 && mainNav.classList.contains('is-fixed')) {
            mainNav.classList.add('is-visible');
          } else {
            console.log(123);
            mainNav.classList.remove('is-visible', 'is-fixed');
          }
        } else {
          // Scrolling Down
          mainNav.classList.remove(['is-visible']);
          if (currentTop > headerHeight && !mainNav.classList.contains('is-fixed')) {
            mainNav.classList.add('is-fixed');
          }
        }
        scrollPos = currentTop;
      });
    });
});



