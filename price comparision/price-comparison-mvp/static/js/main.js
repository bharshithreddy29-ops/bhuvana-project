document.addEventListener('DOMContentLoaded', function() {
    // Flash message auto-hide
    const flashMessages = document.querySelectorAll('.flash-message');
    flashMessages.forEach(message => {
        setTimeout(() => {
            message.style.opacity = '0';
            setTimeout(() => message.remove(), 500);
        }, 5000);
    });

    // Search form validation and loading state
    const searchForm = document.querySelector('form[action*="search"]');
    if (searchForm) {
        searchForm.addEventListener('submit', function(e) {
            const queryInput = this.querySelector('input[name="query"]');
            if (!queryInput.value.trim()) {
                e.preventDefault();
                alert('Please enter a search term');
                return;
            }
            const submitBtn = this.querySelector('button[type="submit"]');
            submitBtn.textContent = 'Searching...';
            submitBtn.disabled = true;
            
            // Show loading indicator
            showLoadingIndicator();
        });
    }

    // Image upload validation and preview
    const uploadForm = document.querySelector('form[action*="upload"]');
    if (uploadForm) {
        const fileInput = uploadForm.querySelector('input[type="file"]');
        
        // File preview
        if (fileInput) {
            fileInput.addEventListener('change', function(e) {
                const file = e.target.files[0];
                if (file) {
                    const reader = new FileReader();
                    reader.onload = function(e) {
                        showImagePreview(e.target.result);
                    };
                    reader.readAsDataURL(file);
                }
            });
        }
        
        uploadForm.addEventListener('submit', function(e) {
            const fileInput = this.querySelector('input[type="file"]');
            if (!fileInput.files.length) {
                e.preventDefault();
                alert('Please select an image file');
                return;
            }
            
            // Validate file type
            const file = fileInput.files[0];
            const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif'];
            if (!allowedTypes.includes(file.type)) {
                e.preventDefault();
                alert('Please select a valid image file (JPG, PNG, GIF)');
                return;
            }
            
            // Validate file size (max 5MB)
            if (file.size > 5 * 1024 * 1024) {
                e.preventDefault();
                alert('File size must be less than 5MB');
                return;
            }
            
            const submitBtn = this.querySelector('button[type="submit"]');
            submitBtn.textContent = 'Uploading...';
            submitBtn.disabled = true;
            
            showLoadingIndicator();
        });
    }
    
    // Alert form validation
    const alertForm = document.querySelector('.alert-form');
    if (alertForm) {
        alertForm.addEventListener('submit', function(e) {
            const productName = this.querySelector('input[name="product_name"]').value.trim();
            const threshold = this.querySelector('input[name="threshold"]').value;
            
            if (!productName) {
                e.preventDefault();
                alert('Please enter a product name');
                return;
            }
            
            if (!threshold || parseFloat(threshold) <= 0) {
                e.preventDefault();
                alert('Please enter a valid price threshold');
                return;
            }
        });
    }
    
    // Product card hover effects
    const productCards = document.querySelectorAll('.product-card');
    productCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });
});

function showLoadingIndicator() {
    const loading = document.createElement('div');
    loading.id = 'loading-indicator';
    loading.innerHTML = `
        <div style="position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.5); z-index: 9999; display: flex; justify-content: center; align-items: center;">
            <div style="background: white; padding: 2rem; border-radius: 10px; text-align: center;">
                <div style="border: 4px solid #f3f3f3; border-top: 4px solid #667eea; border-radius: 50%; width: 40px; height: 40px; animation: spin 1s linear infinite; margin: 0 auto 1rem;"></div>
                <p>Processing your request...</p>
            </div>
        </div>
    `;
    document.body.appendChild(loading);
    
    // Add CSS animation
    const style = document.createElement('style');
    style.textContent = `
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
    `;
    document.head.appendChild(style);
}

function showImagePreview(src) {
    const preview = document.getElementById('image-preview') || document.createElement('div');
    preview.id = 'image-preview';
    preview.innerHTML = `
        <h4>Preview:</h4>
        <img src="${src}" alt="Preview" style="max-width: 200px; max-height: 200px; border-radius: 5px; margin-top: 10px;">
    `;
    
    const uploadSection = document.querySelector('.upload-section');
    if (uploadSection && !document.getElementById('image-preview')) {
        uploadSection.appendChild(preview);
    }
}
