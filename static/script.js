$(window).on('scroll', function() {
  console.log("b")
  if ($(window).scrollTop()) {
    $('header').addClass('nav-show');

  }
  else {
    $('header').removeClass('nav-show');
  }

})

const navSlide = () => {
  const nav_display = document.querySelector(".nav-display");
  const navbar = document.querySelector(".nav-bar");
  const navLinks = document.querySelectorAll(".nav-bar li");

  nav_display.onclick = () => {
    navbar.classList.toggle("nav-active");
    navLinks.forEach((link, index) => {
      if(link.style.animation){
        link.style.animation = "";  
      }else{
        link.style.animation = `navLinkFade 0.5s ease forwards ${index / 7 + 1}s`;
      }
      
    });

    nav_display.classList.toggle("toggle");
  }

}



window.onload = () => navSlide();

/*
DISCLAIMER:
I did not code this entire website, I just modified this template: https://replit.com/@templates/Portfolio-Site-Template
*/