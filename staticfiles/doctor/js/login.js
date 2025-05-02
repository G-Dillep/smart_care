document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('doctorLoginForm');
    const username = document.getElementById('username');
    const password = document.getElementById('password');

    // Real-time validation
    [username, password].forEach(input => {
        input.addEventListener('input', function() {
            if (this.checkValidity()) {
                this.classList.remove('is-invalid');
            }
        });
    });

    // Form submission
    form.addEventListener('submit', function(e) {
        if (!validateForm()) {
            e.preventDefault();
        } else {
            const submitBtn = form.querySelector('button[type="submit"]');
            submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i> Logging in...';
            submitBtn.disabled = true;
        }
    });

    function validateForm() {
        let isValid = true;
        
        if (!username.value.trim()) {
            username.classList.add('is-invalid');
            isValid = false;
        }
        
        if (!password.value.trim()) {
            password.classList.add('is-invalid');
            isValid = false;
        }
        
        if (!isValid) {
            const firstInvalid = form.querySelector('.is-invalid');
            firstInvalid.scrollIntoView({ behavior: 'smooth', block: 'center' });
            firstInvalid.focus();
        }
        
        return isValid;
    }
});