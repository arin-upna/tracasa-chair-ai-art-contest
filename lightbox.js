// Lightbox functionality
document.addEventListener('DOMContentLoaded', function() {
    // Create lightbox element
    const lightbox = document.createElement('div');
    lightbox.className = 'lightbox';
    lightbox.innerHTML = `
        <span class="lightbox-close">&times;</span>
        <img class="lightbox-content" alt="">
        <div class="lightbox-caption"></div>
    `;
    document.body.appendChild(lightbox);

    const lightboxImg = lightbox.querySelector('.lightbox-content');
    const lightboxCaption = lightbox.querySelector('.lightbox-caption');
    const closeBtn = lightbox.querySelector('.lightbox-close');

    // Function to open lightbox
    function openLightbox(img) {
        lightboxImg.src = img.src;
        lightboxCaption.textContent = img.alt;
        lightbox.classList.add('active');
        document.body.style.overflow = 'hidden'; // Prevent scrolling
    }

    // Function to close lightbox
    function closeLightbox() {
        lightbox.classList.remove('active');
        document.body.style.overflow = ''; // Restore scrolling
    }

    // Add click event to all images
    const images = document.querySelectorAll('.prize-image, .gallery-image');
    images.forEach(img => {
        img.addEventListener('click', () => openLightbox(img));
    });

    // Close lightbox when clicking the X button
    closeBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        closeLightbox();
    });

    // Close lightbox when clicking outside the image
    lightbox.addEventListener('click', closeLightbox);

    // Prevent closing when clicking the image itself
    lightboxImg.addEventListener('click', (e) => {
        e.stopPropagation();
    });

    // Close lightbox with Escape key
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && lightbox.classList.contains('active')) {
            closeLightbox();
        }
    });
});
