document.addEventListener('DOMContentLoaded', function() {
    // Initialize the application
    initializeApp();
    
    // Flash message auto-hide with animation
    handleFlashMessages();
    
    // Search functionality
    initializeSearch();
    
    // Form validations
    initializeFormValidations();
    
    // Interactive elements
    initializeInteractiveElements();
    
    // Analytics tracking
    initializeAnalytics();
});

function initializeApp() {
    // Add loading states to buttons
    document.querySelectorAll('form').forEach(form => {
        form.addEventListener('submit', function(e) {
            const submitBtn = this.querySelector('button[type="submit"]');
            if (submitBtn && !submitBtn.disabled) {
                const originalText = submitBtn.innerHTML;
                submitBtn.innerHTML = '<span class="loading"></span> ' + getLoadingText(submitBtn);
                submitBtn.disabled = true;
                
                // Re-enable after 10 seconds as fallback
                setTimeout(() => {
                    submitBtn.innerHTML = originalText;
                    submitBtn.disabled = false;
                }, 10000);
            }
        });
    });
}

function getLoadingText(button) {
    const text = button.textContent.toLowerCase();
    if (text.includes('search')) return 'Searching...';
    if (text.includes('login') || text.includes('sign in')) return 'Signing in...';
    if (text.includes('register') || text.includes('sign up')) return 'Creating account...';
    if (text.includes('upload')) return 'Uploading...';
    if (text.includes('save')) return 'Saving...';
    return 'Processing...';
}

function handleFlashMessages() {
    const flashMessages = document.querySelectorAll('.flash-message');
    flashMessages.forEach((message, index) => {
        // Animate in
        message.style.transform = 'translateX(100%)';
        message.style.opacity = '0';
        
        setTimeout(() => {
            message.style.transform = 'translateX(0)';
            message.style.opacity = '1';
        }, index * 200);
        
        // Auto-hide after 5 seconds
        setTimeout(() => {
            message.style.transform = 'translateX(100%)';
            message.style.opacity = '0';
            setTimeout(() => message.remove(), 300);
        }, 5000 + (index * 200));
        
        // Click to dismiss
        message.addEventListener('click', function() {
            this.style.transform = 'translateX(100%)';
            this.style.opacity = '0';
            setTimeout(() => this.remove(), 300);
        });
    });
}

function initializeSearch() {
    // Search suggestions
    const searchInputs = document.querySelectorAll('input[name="query"]');
    searchInputs.forEach(input => {
        let suggestionTimeout;
        
        input.addEventListener('input', function() {
            clearTimeout(suggestionTimeout);
            suggestionTimeout = setTimeout(() => {
                showSearchSuggestions(this);
            }, 300);
        });
        
        input.addEventListener('focus', function() {
            if (this.value.length > 2) {
                showSearchSuggestions(this);
            }
        });
        
        input.addEventListener('blur', function() {
            setTimeout(() => hideSuggestions(this), 200);
        });
    });
    
    // Search history
    loadSearchHistory();
}

function showSearchSuggestions(input) {
    const query = input.value.toLowerCase();
    if (query.length < 2) return;
    
    const suggestions = [
        'iPhone 15', 'Samsung Galaxy', 'Nike shoes', 'Adidas sneakers',
        'Laptop Dell', 'MacBook Pro', 'Milk Amul', 'Bread Britannia',
        'Jeans Levi\'s', 'T-shirt Nike', 'Headphones Sony', 'Watch Apple'
    ].filter(item => item.toLowerCase().includes(query));
    
    if (suggestions.length === 0) return;
    
    // Remove existing suggestions
    const existingSuggestions = input.parentNode.querySelector('.search-suggestions');
    if (existingSuggestions) {
        existingSuggestions.remove();
    }
    
    // Create suggestions dropdown
    const suggestionsDiv = document.createElement('div');
    suggestionsDiv.className = 'search-suggestions';
    suggestionsDiv.style.cssText = `
        position: absolute;
        top: 100%;
        left: 0;
        right: 0;
        background: white;
        border: 1px solid #e1e8ed;
        border-top: none;
        border-radius: 0 0 8px 8px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        z-index: 1000;
        max-height: 200px;
        overflow-y: auto;
    `;
    
    suggestions.slice(0, 5).forEach(suggestion => {
        const suggestionItem = document.createElement('div');
        suggestionItem.textContent = suggestion;
        suggestionItem.style.cssText = `
            padding: 0.75rem 1rem;
            cursor: pointer;
            border-bottom: 1px solid #f8f9fa;
            transition: background 0.2s;
        `;
        
        suggestionItem.addEventListener('mouseenter', function() {
            this.style.background = '#f8f9fa';
        });
        
        suggestionItem.addEventListener('mouseleave', function() {
            this.style.background = 'white';
        });
        
        suggestionItem.addEventListener('click', function() {
            input.value = suggestion;
            input.form.submit();
        });
        
        suggestionsDiv.appendChild(suggestionItem);
    });
    
    input.parentNode.style.position = 'relative';
    input.parentNode.appendChild(suggestionsDiv);
}

function hideSuggestions(input) {
    const suggestions = input.parentNode.querySelector('.search-suggestions');
    if (suggestions) {
        suggestions.remove();
    }
}

function loadSearchHistory() {
    // Load from localStorage
    const history = JSON.parse(localStorage.getItem('searchHistory') || '[]');
    // Display recent searches if needed
}

function saveSearchHistory(query) {
    let history = JSON.parse(localStorage.getItem('searchHistory') || '[]');
    history = history.filter(item => item !== query); // Remove duplicates
    history.unshift(query); // Add to beginning
    history = history.slice(0, 10); // Keep only 10 items
    localStorage.setItem('searchHistory', JSON.stringify(history));
}

function initializeFormValidations() {
    // Password strength indicator
    const passwordInputs = document.querySelectorAll('input[type="password"]');
    passwordInputs.forEach(input => {
        if (input.name === 'password') {
            input.addEventListener('input', function() {
                showPasswordStrength(this);
            });
        }
    });
    
    // Email validation
    const emailInputs = document.querySelectorAll('input[type="email"]');
    emailInputs.forEach(input => {
        input.addEventListener('blur', function() {
            validateEmail(this);
        });
    });
    
    // Real-time form validation
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        const inputs = form.querySelectorAll('input[required]');
        inputs.forEach(input => {
            input.addEventListener('blur', function() {
                validateField(this);
            });
        });
    });
}

function showPasswordStrength(input) {
    const password = input.value;
    let strength = 0;
    let feedback = [];
    
    if (password.length >= 8) strength++;
    else feedback.push('At least 8 characters');
    
    if (/[A-Z]/.test(password)) strength++;
    else feedback.push('One uppercase letter');
    
    if (/[a-z]/.test(password)) strength++;
    else feedback.push('One lowercase letter');
    
    if (/[0-9]/.test(password)) strength++;
    else feedback.push('One number');
    
    if (/[^A-Za-z0-9]/.test(password)) strength++;
    else feedback.push('One special character');
    
    // Remove existing indicator
    const existing = input.parentNode.querySelector('.password-strength');
    if (existing) existing.remove();
    
    if (password.length > 0) {
        const indicator = document.createElement('div');
        indicator.className = 'password-strength';
        indicator.style.cssText = `
            margin-top: 0.5rem;
            font-size: 0.8rem;
        `;
        
        const strengthLevels = ['Very Weak', 'Weak', 'Fair', 'Good', 'Strong'];
        const strengthColors = ['#e74c3c', '#e67e22', '#f39c12', '#f1c40f', '#27ae60'];
        
        indicator.innerHTML = `
            <div style="display: flex; gap: 2px; margin-bottom: 0.25rem;">
                ${Array(5).fill(0).map((_, i) => 
                    `<div style="height: 4px; flex: 1; background: ${i < strength ? strengthColors[strength-1] : '#e1e8ed'}; border-radius: 2px;"></div>`
                ).join('')}
            </div>
            <div style="color: ${strengthColors[strength-1] || '#7f8c8d'};">
                ${strengthLevels[strength-1] || 'Enter password'}
                ${feedback.length > 0 ? ' - Need: ' + feedback.join(', ') : ''}
            </div>
        `;
        
        input.parentNode.appendChild(indicator);
    }
}

function validateEmail(input) {
    const email = input.value;
    const isValid = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
    
    if (email && !isValid) {
        showFieldError(input, 'Please enter a valid email address');
    } else {
        clearFieldError(input);
    }
}

function validateField(input) {
    if (input.hasAttribute('required') && !input.value.trim()) {
        showFieldError(input, 'This field is required');
    } else {
        clearFieldError(input);
    }
}

function showFieldError(input, message) {
    clearFieldError(input);
    
    const error = document.createElement('div');
    error.className = 'field-error';
    error.textContent = message;
    error.style.cssText = `
        color: #e74c3c;
        font-size: 0.8rem;
        margin-top: 0.25rem;
    `;
    
    input.style.borderColor = '#e74c3c';
    input.parentNode.appendChild(error);
}

function clearFieldError(input) {
    const error = input.parentNode.querySelector('.field-error');
    if (error) error.remove();
    input.style.borderColor = '';
}

function initializeInteractiveElements() {
    // Smooth scrolling for anchor links
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
    
    // Image lazy loading
    const images = document.querySelectorAll('img[data-src]');
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.removeAttribute('data-src');
                observer.unobserve(img);
            }
        });
    });
    
    images.forEach(img => imageObserver.observe(img));
    
    // Tooltip functionality
    document.querySelectorAll('[data-tooltip]').forEach(element => {
        element.addEventListener('mouseenter', showTooltip);
        element.addEventListener('mouseleave', hideTooltip);
    });
    
    // Copy to clipboard functionality
    document.querySelectorAll('[data-copy]').forEach(element => {
        element.addEventListener('click', function() {
            navigator.clipboard.writeText(this.dataset.copy).then(() => {
                showToast('Copied to clipboard!', 'success');
            });
        });
    });
}

function showTooltip(e) {
    const tooltip = document.createElement('div');
    tooltip.className = 'tooltip';
    tooltip.textContent = e.target.dataset.tooltip;
    tooltip.style.cssText = `
        position: absolute;
        background: #2c3e50;
        color: white;
        padding: 0.5rem;
        border-radius: 4px;
        font-size: 0.8rem;
        z-index: 1000;
        pointer-events: none;
        white-space: nowrap;
    `;
    
    document.body.appendChild(tooltip);
    
    const rect = e.target.getBoundingClientRect();
    tooltip.style.left = rect.left + (rect.width / 2) - (tooltip.offsetWidth / 2) + 'px';
    tooltip.style.top = rect.top - tooltip.offsetHeight - 5 + 'px';
}

function hideTooltip() {
    const tooltip = document.querySelector('.tooltip');
    if (tooltip) tooltip.remove();
}

function showToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.textContent = message;
    toast.style.cssText = `
        position: fixed;
        bottom: 20px;
        right: 20px;
        background: ${type === 'success' ? '#27ae60' : type === 'error' ? '#e74c3c' : '#3498db'};
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 8px;
        z-index: 1000;
        animation: slideInUp 0.3s ease;
    `;
    
    document.body.appendChild(toast);
    
    setTimeout(() => {
        toast.style.animation = 'slideOutDown 0.3s ease';
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

function initializeAnalytics() {
    // Track page views
    trackPageView();
    
    // Track user interactions
    document.addEventListener('click', function(e) {
        if (e.target.matches('a, button')) {
            trackEvent('click', e.target.textContent.trim(), e.target.href || e.target.type);
        }
    });
    
    // Track search queries
    document.querySelectorAll('form').forEach(form => {
        if (form.action.includes('search')) {
            form.addEventListener('submit', function() {
                const query = this.querySelector('input[name="query"]')?.value;
                if (query) {
                    trackEvent('search', query);
                    saveSearchHistory(query);
                }
            });
        }
    });
}

function trackPageView() {
    // In real implementation, send to analytics service
    console.log('Page view:', window.location.pathname);
}

function trackEvent(action, label, value) {
    // In real implementation, send to analytics service
    console.log('Event:', { action, label, value });
}

// Utility functions
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

function throttle(func, limit) {
    let inThrottle;
    return function() {
        const args = arguments;
        const context = this;
        if (!inThrottle) {
            func.apply(context, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    }
}

// Add CSS animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideInUp {
        from { transform: translateY(100%); opacity: 0; }
        to { transform: translateY(0); opacity: 1; }
    }
    
    @keyframes slideOutDown {
        from { transform: translateY(0); opacity: 1; }
        to { transform: translateY(100%); opacity: 0; }
    }
    
    .loading {
        display: inline-block;
        width: 16px;
        height: 16px;
        border: 2px solid #f3f3f3;
        border-top: 2px solid currentColor;
        border-radius: 50%;
        animation: spin 1s linear infinite;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
`;
document.head.appendChild(style);