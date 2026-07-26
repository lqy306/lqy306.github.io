/**
 * LEO LEE — Personal Site
 * Minimal interactions: header scroll, mobile nav, reveal animations
 */
(function () {
  'use strict';

  const header = document.querySelector('.header');
  const menuToggle = document.querySelector('.menu-toggle');
  const navList = document.querySelector('.nav-list');
  const navLinks = document.querySelectorAll('.nav-link');

  // ---------- Header solid on scroll ----------
  let ticking = false;
  window.addEventListener('scroll', function () {
    if (!ticking) {
      requestAnimationFrame(function () {
        header.classList.toggle('header--solid', window.scrollY > 30);
        ticking = false;
      });
      ticking = true;
    }
  }, { passive: true });

  // ---------- Mobile menu ----------
  function openMenu() {
    navList.classList.add('nav-list--open');
    menuToggle.classList.add('menu-toggle--open');
    document.body.style.overflow = 'hidden';
  }

  function closeMenu() {
    navList.classList.remove('nav-list--open');
    menuToggle.classList.remove('menu-toggle--open');
    document.body.style.overflow = '';
  }

  menuToggle.addEventListener('click', function () {
    navList.classList.contains('nav-list--open') ? closeMenu() : openMenu();
  });

  navLinks.forEach(function (link) {
    link.addEventListener('click', closeMenu);
  });

  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && navList.classList.contains('nav-list--open')) {
      closeMenu();
    }
  });

  // ---------- Reveal on scroll ----------
  var revealEls = document.querySelectorAll('.series, .about-text p, .about-links, .footer-quote');
  revealEls.forEach(function (el) { el.classList.add('reveal'); });

  var observer = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (entry.isIntersecting) {
        entry.target.classList.add('reveal--shown');
        observer.unobserve(entry.target);
      }
    });
  }, { rootMargin: '0px 0px -8% 0px', threshold: 0.1 });

  revealEls.forEach(function (el) { observer.observe(el); });

  // ---------- Gallery parallax on hover ----------
  var galleryItems = document.querySelectorAll('.gallery-item');
  galleryItems.forEach(function (item) {
    item.addEventListener('mousemove', function (e) {
      var rect = item.getBoundingClientRect();
      var x = (e.clientX - rect.left) / rect.width - 0.5;
      var y = (e.clientY - rect.top) / rect.height - 0.5;
      var img = item.querySelector('img');
      if (img) {
        img.style.transform = 'scale(1.04) translate(' + (x * 10) + 'px, ' + (y * 10) + 'px)';
      }
    });
    item.addEventListener('mouseleave', function () {
      var img = item.querySelector('img');
      if (img) img.style.transform = '';
    });
  });

})();
