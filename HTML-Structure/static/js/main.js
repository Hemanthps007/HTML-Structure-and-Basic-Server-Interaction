/**
 * Progressive Enhancement & Semantic Tag Inspector for HTML Structure Demonstration
 */
document.addEventListener('DOMContentLoaded', () => {

    // 1. Semantic Tag Inspector Toggle
    const inspectorBtn = document.getElementById('toggle-semantic-inspector');
    if (inspectorBtn) {
        const inspectorText = inspectorBtn.querySelector('.inspector-text');
        
        // Restore saved preference if any
        if (localStorage.getItem('cognify_semantic_debug') === 'true') {
            document.body.classList.add('semantic-debug-active');
            if (inspectorText) inspectorText.textContent = 'Hide Semantic Tags';
            inspectorBtn.classList.add('active');
        }

        inspectorBtn.addEventListener('click', () => {
            const isActive = document.body.classList.toggle('semantic-debug-active');
            localStorage.setItem('cognify_semantic_debug', isActive);
            if (inspectorText) {
                inspectorText.textContent = isActive ? 'Hide Semantic Tags' : 'Show Semantic Tags';
            }
            inspectorBtn.classList.toggle('active', isActive);
        });
    }

    // 2. Password Visibility Toggle
    document.querySelectorAll('.btn-toggle-password').forEach(button => {
        button.addEventListener('click', () => {
            const targetId = button.getAttribute('data-target');
            const targetInput = document.getElementById(targetId);
            if (targetInput) {
                if (targetInput.type === 'password') {
                    targetInput.type = 'text';
                    button.textContent = '🙈';
                    button.setAttribute('aria-label', 'Hide password');
                } else {
                    targetInput.type = 'password';
                    button.textContent = '👁️';
                    button.setAttribute('aria-label', 'Show password');
                }
            }
        });
    });

    // 3. Quick Demo Login Credentials Auto-Fill
    document.querySelectorAll('.btn-quick-fill').forEach(button => {
        button.addEventListener('click', () => {
            const user = button.getAttribute('data-user');
            const pass = button.getAttribute('data-pass');
            const identInput = document.getElementById('identifier');
            const passInput = document.getElementById('password');

            if (identInput && passInput) {
                identInput.value = user;
                passInput.value = pass;
                identInput.focus();
                // Visual pulse effect
                identInput.style.backgroundColor = '#eff6ff';
                passInput.style.backgroundColor = '#eff6ff';
                setTimeout(() => {
                    identInput.style.backgroundColor = '';
                    passInput.style.backgroundColor = '';
                }, 500);
            }
        });
    });

    // 4. Auto-dismiss Flash Alerts
    document.querySelectorAll('.alert').forEach(alert => {
        setTimeout(() => {
            alert.style.transition = 'opacity 0.4s ease, transform 0.4s ease';
            alert.style.opacity = '0';
            alert.style.transform = 'translateY(-6px)';
            setTimeout(() => alert.remove(), 400);
        }, 7000);
    });

    // 5. Terms of Service Modal / Alert Trigger
    document.querySelectorAll('.modal-trigger').forEach(trigger => {
        trigger.addEventListener('click', (e) => {
            e.preventDefault();
            alert("Cognify Terms of Service (Educational Project):\n\n1. All submitted data is maintained in a local SQLite database for demonstration purposes.\n2. Password hashes utilize secure scrypt/pbkdf2 algorithms.\n3. Semantic HTML5 standards and accessibility guidelines are strictly observed.");
        });
    });

});
