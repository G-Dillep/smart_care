document.addEventListener('DOMContentLoaded', function() {
    // Form elements
    const form = document.getElementById('doctorRegistrationForm');
    const sections = document.querySelectorAll('.form-section');
    const steps = document.querySelectorAll('.step');
    let currentSection = 0;

    // Show first section
    showSection(currentSection);

    // Next button functionality
    document.querySelectorAll('.btn-next').forEach(button => {
        button.addEventListener('click', function() {
            if (validateCurrentSection()) {
                currentSection++;
                showSection(currentSection);
            }
        });
    });

    // Previous button functionality
    document.querySelectorAll('.btn-prev').forEach(button => {
        button.addEventListener('click', function() {
            currentSection--;
            showSection(currentSection);
        });
    });

    // File preview functionality
    const profilePhotoInput = document.getElementById('profile_photo');
    if (profilePhotoInput) {
        profilePhotoInput.addEventListener('change', function() {
            const file = this.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    const preview = document.getElementById('previewImage');
                    preview.src = e.target.result;
                    preview.style.display = 'block';
                    preview.classList.add('animate__animated', 'animate__fadeIn');
                }
                reader.readAsDataURL(file);
            }
        });
    }

    // Password confirmation validation
    const password = document.getElementById('password');
    const confirmPassword = document.getElementById('confirm_password');
    if (password && confirmPassword) {
        confirmPassword.addEventListener('input', function() {
            if (password.value !== confirmPassword.value) {
                this.setCustomValidity("Passwords don't match");
                this.classList.add('is-invalid');
            } else {
                this.setCustomValidity('');
                this.classList.remove('is-invalid');
            }
        });
    }

    // Form submission
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        if (validateForm()) {
            const submitBtn = document.querySelector('.btn-submit');
            submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span> Processing...';
            submitBtn.disabled = true;
            
            // Submit the form
            form.submit();
        }
    });

    // Helper functions
    function showSection(index) {
        // Hide all sections
        sections.forEach(section => {
            section.classList.remove('active', 'animate__fadeIn');
        });
        
        // Show current section
        sections[index].classList.add('active', 'animate__fadeIn');
        
        // Update steps
        updateSteps(index);
        
        // Scroll to top
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }

    function updateSteps(currentIndex) {
        steps.forEach((step, index) => {
            if (index <= currentIndex) {
                step.classList.add('active');
            } else {
                step.classList.remove('active');
            }
        });
    }

    function validateCurrentSection() {
        const currentSectionEl = sections[currentSection];
        const inputs = currentSectionEl.querySelectorAll('input, select, textarea, [required]');
        let isValid = true;
        
        inputs.forEach(input => {
            if (!input.checkValidity()) {
                input.classList.add('is-invalid');
                isValid = false;
                
                // Add shake animation
                input.classList.add('animate__animated', 'animate__shakeX');
                input.addEventListener('animationend', () => {
                    input.classList.remove('animate__animated', 'animate__shakeX');
                });
            } else {
                input.classList.remove('is-invalid');
            }
        });
        
        if (!isValid) {
            // Scroll to first invalid field
            const firstInvalid = currentSectionEl.querySelector('.is-invalid');
            firstInvalid.scrollIntoView({ behavior: 'smooth', block: 'center' });
            firstInvalid.focus();
        }
        
        return isValid;
    }

    function validateForm() {
        let isValid = true;
        const inputs = form.querySelectorAll('input, select, textarea, [required]');
        
        inputs.forEach(input => {
            if (!input.checkValidity()) {
                input.classList.add('is-invalid');
                isValid = false;
            } else {
                input.classList.remove('is-invalid');
            }
        });
        
        if (!isValid) {
            // Find and show the first invalid section
            const firstInvalid = form.querySelector('.is-invalid');
            const invalidSection = firstInvalid.closest('.form-section');
            const sectionIndex = Array.from(sections).indexOf(invalidSection);
            
            showSection(sectionIndex);
            firstInvalid.scrollIntoView({ behavior: 'smooth', block: 'center' });
            firstInvalid.focus();
        }
        
        return isValid;
    }

    // Add input validation on blur
    document.querySelectorAll('input, select, textarea').forEach(input => {
        input.addEventListener('blur', function() {
            if (!this.checkValidity()) {
                this.classList.add('is-invalid');
            } else {
                this.classList.remove('is-invalid');
            }
        });
    });
});