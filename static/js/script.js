document.addEventListener("DOMContentLoaded", () => {
    const nav = document.querySelector(".nav");
    const links = nav.querySelectorAll(".nav-link");
    const indicator = nav.querySelector(".active-indicator");
    
    function setIndicator(el) {
        if (!el) return;
        indicator.style.width = el.offsetWidth + "px";
        indicator.style.transform = `translateX(${el.offsetLeft}px)`;
    }
    
    const currentPath = window.location.pathname;
    let currentPage = '';
    
    if (currentPath.endsWith('index.html') || currentPath.endsWith('/')) {
        currentPage = 'index.html';
    } else if (currentPath.includes('random_play.html')) {
        currentPage = 'random_play.html';
    } else if (currentPath.includes('watch_stariy.html')) {
        currentPage = 'watch_stariy.html';
    } else if (currentPath.includes('learn_how_to_play.html')) {
        currentPage = 'learn_how_to_play.html';
    } else {
        currentPage = currentPath.split('/').pop() || 'index.html';
    }
    
    console.log('Current page:', currentPage);
    
    indicator.style.transition = 'none';
    
    links.forEach(link => {
        const linkHref = link.getAttribute('href');
        link.classList.remove('active');
        
        if (linkHref === currentPage) {
            link.classList.add('active');
            console.log('Active link set:', link.textContent);
        }
        
        link.addEventListener("click", (e) => {
            links.forEach(l => l.classList.remove("active"));
            link.classList.add("active");
            setIndicator(link);
        });
        
        link.addEventListener("mouseenter", () => {
            setIndicator(link);
        });
    });
    
    const activeLink = nav.querySelector(".nav-link.active");
    if (activeLink) {
        setIndicator(activeLink);
    }
    
    setTimeout(() => {
        indicator.style.transition = 'transform 0.4s ease, width 0.4s ease';
    }, 50);
    
    nav.addEventListener("mouseleave", () => {
        const activeLink = nav.querySelector(".nav-link.active");
        if (activeLink) {
            setIndicator(activeLink);
        }
    });
    
    window.addEventListener("resize", () => {
        const activeLink = nav.querySelector(".nav-link.active");
        if (activeLink) {
            setIndicator(activeLink);
        }
    });
});







