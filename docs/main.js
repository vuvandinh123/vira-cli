// Fade in animation on scroll
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('visible');
        }
    });
}, observerOptions);

document.querySelectorAll('.fade-in').forEach(el => {
    observer.observe(el);
});

// Smooth scroll for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Add parallax effect to hero section
window.addEventListener('scroll', () => {
    const scrolled = window.pageYOffset;
    const parallax = document.querySelector('.float-animation');
    if (parallax) {
        parallax.style.transform = `translateY(${scrolled * 0.3}px)`;
    }
});

document.addEventListener('DOMContentLoaded', () => {
  // Mobile menu
  const btn = document.getElementById('mobile-menu-button');
  const menu = document.getElementById('mobile-menu');
  if (btn && menu) {
    btn.addEventListener('click', () => {
      const opened = !menu.classList.toggle('hidden');
      btn.setAttribute('aria-expanded', String(opened));
    });

    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && !menu.classList.contains('hidden')) {
        menu.classList.add('hidden');
        btn.setAttribute('aria-expanded', 'false');
      }
    });

    document.addEventListener('click', (e) => {
      if (!menu.contains(e.target) && !btn.contains(e.target) && !menu.classList.contains('hidden')) {
        menu.classList.add('hidden');
        btn.setAttribute('aria-expanded', 'false');
      }
    });
  }

  // Demo video modal
  const playBtn = document.getElementById('demo-play-button');
  const modal = document.getElementById('demo-modal');
  const modalContent = document.getElementById('demo-modal-content');
  const closeBtn = document.getElementById('demo-close-button');
  const video = document.getElementById('demo-video');

  function openModal() {
    if (!modal || !video || !playBtn) return;
    modal.classList.remove('hidden');
    modal.setAttribute('aria-hidden', 'false');
    playBtn.setAttribute('aria-expanded', 'true');
    // reset to start and play
    try { video.currentTime = 0; } catch (e) {}
    video.play().catch(() => {});
  }

  function closeModal() {
    if (!modal || !video || !playBtn) return;
    video.pause();
    try { video.currentTime = 0; } catch (e) {}
    modal.classList.add('hidden');
    modal.setAttribute('aria-hidden', 'true');
    playBtn.setAttribute('aria-expanded', 'false');
  }

  if (playBtn && modal && video) {
    playBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      openModal();
    });

    closeBtn?.addEventListener('click', (e) => {
      e.stopPropagation();
      closeModal();
    });

    // click outside content closes
    modal.addEventListener('click', (e) => {
      if (!modalContent.contains(e.target)) closeModal();
    });

    // Escape closes
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && modal && !modal.classList.contains('hidden')) {
        closeModal();
      }
    });

    // when video ends, close modal (optional)
    video.addEventListener('ended', () => {
      closeModal();
    });
  }
});