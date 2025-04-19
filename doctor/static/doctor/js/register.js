document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('doctorRegistrationForm');
    const sections = document.querySelectorAll('.form-section');
    const submitBtn = document.querySelector('.btn-primary');
    
    // Add animations to form sections
    sections.forEach((section, index) => {
        section.style.animationDelay = `${index * 0.1}s`;
    });
    
    // Form validation with animations
    form.addEventListener('submit', function(event) {
        if (!form.checkValidity()) {
            event.preventDefault();
            event.stopPropagation();
            
            // Add shake animation to invalid fields
            const invalidFields = form.querySelectorAll(':invalid');
            invalidFields.forEach(field => {
                field.classList.add('animate__animated', 'animate__shakeX');
                field.addEventListener('animationend', () => {
                    field.classList.remove('animate__animated', 'animate__shakeX');
                });
            });
        }
        
        form.classList.add('was-validated');
    }, false);
    
    // Password confirmation validation
    const password = document.getElementById('id_password');
    const confirmPassword = document.getElementById('id_confirm_password');
    
    if (password && confirmPassword) {
        confirmPassword.addEventListener('input', function() {
            if (password.value !== confirmPassword.value) {
                confirmPassword.setCustomValidity("Passwords don't match");
                confirmPassword.classList.add('is-invalid');
            } else {
                confirmPassword.setCustomValidity('');
                confirmPassword.classList.remove('is-invalid');
            }
        });
    }
    
    // Profile photo preview with animation
    const profilePhotoInput = document.getElementById('id_profile_photo');
    if (profilePhotoInput) {
        profilePhotoInput.addEventListener('change', function(event) {
            const file = event.target.files[0];
            if (file) {
                // Remove existing preview if any
                let preview = document.getElementById('profilePhotoPreview');
                if (preview) {
                    preview.classList.add('animate__animated', 'animate__fadeOut');
                    preview.addEventListener('animationend', () => {
                        preview.remove();
                    });
                }
                
                // Create new preview
                const reader = new FileReader();
                reader.onload = function(e) {
                    preview = document.createElement('img');
                    preview.id = 'profilePhotoPreview';
                    preview.src = e.target.result;
                    preview.classList.add('animate__animated', 'animate__fadeIn');
                    preview.style.maxWidth = '200px';
                    preview.style.maxHeight = '200px';
                    preview.style.marginTop = '10px';
                    preview.style.display = 'block';
                    preview.style.borderRadius = '8px';
                    profilePhotoInput.parentNode.appendChild(preview);
                };
                reader.readAsDataURL(file);
            }
        });
    }
    
    // Add floating label effect to all inputs
    const floatLabels = document.querySelectorAll('.form-floating');
    floatLabels.forEach(label => {
        const input = label.querySelector('.form-control');
        input.addEventListener('focus', () => {
            label.classList.add('active');
        });
        input.addEventListener('blur', () => {
            if (!input.value) {
                label.classList.remove('active');
            }
        });
        
        // Initialize if already has value
        if (input.value) {
            label.classList.add('active');
        }
    });
    
    // Button hover effect
    if (submitBtn) {
        submitBtn.addEventListener('mouseenter', () => {
            submitBtn.classList.add('animate__animated', 'animate__pulse');
        });
        submitBtn.addEventListener('mouseleave', () => {
            submitBtn.classList.remove('animate__animated', 'animate__pulse');
        });
    }
    
    // Add smooth scrolling to invalid fields
   