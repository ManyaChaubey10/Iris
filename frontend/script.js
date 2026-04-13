document.addEventListener('DOMContentLoaded', () => {
    // DOM Elements
    const video = document.getElementById('webcam');
    const placeholder = document.getElementById('placeholder');
    const statusIndicator = document.getElementById('statusIndicator');
    const toggleBtn = document.getElementById('toggleCamera');
    const toggleIcon = toggleBtn ? toggleBtn.querySelector('i') : null;
    const toggleText = toggleBtn ? toggleBtn.querySelector('span') : null;
    const translationBox = document.getElementById('translationBox');
    const outputText = document.getElementById('outputText');
    const wavelengthBox = document.getElementById('wavelengthBox');

    // State
    let stream = null;
    let isCameraRunning = false;

    // Toggle Camera function
    async function toggleCamera() {
        if (!isCameraRunning) {
            // Start Camera
            try {
                stream = await navigator.mediaDevices.getUserMedia({ 
                    video: { 
                        width: { ideal: 1280 },
                        height: { ideal: 720 },
                        facingMode: "user" 
                    } 
                });
                
                video.srcObject = stream;
                
                video.onloadedmetadata = () => {
                    video.play();
                    
                    placeholder.classList.add('hidden');
                    video.style.display = 'block';
                    statusIndicator.classList.remove('hidden');
                    translationBox.classList.remove('hidden');
                    if (wavelengthBox) wavelengthBox.classList.remove('hidden');
                    
                    toggleBtn.classList.remove('primary-btn');
                    toggleBtn.classList.add('danger-btn');
                    if (toggleIcon) {
                        toggleIcon.classList.remove('fa-camera');
                        toggleIcon.classList.add('fa-video-slash');
                    }
                    if (toggleText) toggleText.textContent = 'Stop Camera';
                    
                    isCameraRunning = true;
                };
            } catch (err) {
                console.error("Error accessing webcam: ", err);
                alert("Could not access the webcam. Please ensure you have granted permission and that no other application is using it.");
            }
        } else {
            // Stop Camera
            if (stream) {
                const tracks = stream.getTracks();
                tracks.forEach(track => track.stop());
                video.srcObject = null;
                
                video.style.display = 'none';
                placeholder.classList.remove('hidden');
                statusIndicator.classList.add('hidden');
                translationBox.classList.add('hidden');
                if (wavelengthBox) wavelengthBox.classList.add('hidden');
                
                toggleBtn.classList.remove('danger-btn');
                toggleBtn.classList.add('primary-btn');
                if (toggleIcon) {
                    toggleIcon.classList.remove('fa-video-slash');
                    toggleIcon.classList.add('fa-camera');
                }
                if (toggleText) toggleText.textContent = 'Start Camera';
                
                isCameraRunning = false;
            }
        }
    }

    // Event Listeners for Camera
    if (toggleBtn) {
        toggleBtn.addEventListener('click', toggleCamera);
    }

    // --- UI Logic: Intersection Observer for Fade-In Animations ---
    const observerOptions = {
        root: null,
        rootMargin: '0px',
        threshold: 0.15
    };

    const fadeInObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                observer.unobserve(entry.target); // Only animate once
            }
        });
    }, observerOptions);

    document.querySelectorAll('.fade-in-up').forEach(el => {
        fadeInObserver.observe(el);
    });

    // --- Dynamic Navbar Styling on Scroll ---
    const navbar = document.querySelector('.navbar');
    window.addEventListener('scroll', () => {
        if (navbar) {
            if (window.scrollY > 50) {
                navbar.style.background = 'rgba(20, 22, 30, 0.85)';
                navbar.style.boxShadow = '0 4px 20px rgba(0, 0, 0, 0.5)';
                navbar.style.padding = '0.5rem 1.5rem';
                navbar.style.backdropFilter = 'blur(20px)';
            } else {
                navbar.style.background = 'var(--glass-bg)';
                navbar.style.boxShadow = 'none';
                navbar.style.padding = '0.75rem 1.5rem';
            }
        }
    });

    // --- Mobile Menu Toggle logic (placeholder) ---
    const mobileToggle = document.querySelector('.mobile-toggle');
    const navLinks = document.querySelector('.nav-links');
    
    if (mobileToggle && navLinks) {
        mobileToggle.addEventListener('click', () => {
            navLinks.style.display = navLinks.style.display === 'flex' ? 'none' : 'flex';
            navLinks.style.flexDirection = 'column';
            navLinks.style.position = 'absolute';
            navLinks.style.top = '100%';
            navLinks.style.right = '0';
            navLinks.style.background = 'var(--surface)';
            navLinks.style.padding = '1rem';
            navLinks.style.borderRadius = '12px';
            navLinks.style.gap = '1rem';
        });
    }
});
