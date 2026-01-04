// AR/VR Product Preview - Unique Feature
class ARProductPreview {
    constructor() {
        this.isARSupported = this.checkARSupport();
        this.init();
    }

    checkARSupport() {
        return 'xr' in navigator && 'isSessionSupported' in navigator.xr;
    }

    init() {
        this.createARModal();
        this.attachEventListeners();
    }

    createARModal() {
        const modal = document.createElement('div');
        modal.id = 'ar-modal';
        modal.innerHTML = `
            <div class="ar-modal-content">
                <div class="ar-header">
                    <h3>🥽 3D Product Preview</h3>
                    <button class="ar-close">&times;</button>
                </div>
                <div class="ar-viewer">
                    <div class="ar-product-3d" id="ar-product-3d">
                        <div class="product-3d-container">
                            <div class="product-3d-item">
                                <img id="ar-product-image" src="" alt="Product">
                            </div>
                        </div>
                    </div>
                    <div class="ar-controls">
                        <button class="ar-btn" onclick="arPreview.rotate('left')">↺ Rotate Left</button>
                        <button class="ar-btn" onclick="arPreview.rotate('right')">↻ Rotate Right</button>
                        <button class="ar-btn" onclick="arPreview.zoom('in')">🔍 Zoom In</button>
                        <button class="ar-btn" onclick="arPreview.zoom('out')">🔍 Zoom Out</button>
                    </div>
                    <div class="ar-info">
                        <h4 id="ar-product-name">Product Name</h4>
                        <p id="ar-product-price">₹0.00</p>
                        <p id="ar-product-platform">Platform</p>
                    </div>
                    ${this.isARSupported ? 
                        '<button class="ar-btn ar-launch" onclick="arPreview.launchAR()">🚀 Launch AR View</button>' : 
                        '<p class="ar-not-supported">AR not supported on this device</p>'
                    }
                </div>
            </div>
        `;

        // Add CSS for AR Modal
        const style = document.createElement('style');
        style.textContent = `
            #ar-modal {
                display: none;
                position: fixed;
                z-index: 10000;
                left: 0;
                top: 0;
                width: 100%;
                height: 100%;
                background: rgba(0,0,0,0.8);
                backdrop-filter: blur(10px);
            }

            .ar-modal-content {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                margin: 5% auto;
                padding: 0;
                border-radius: 20px;
                width: 90%;
                max-width: 600px;
                box-shadow: 0 25px 50px rgba(0,0,0,0.3);
                transform: perspective(1000px) rotateX(5deg);
                animation: modalSlideIn 0.5s ease;
            }

            @keyframes modalSlideIn {
                from { 
                    transform: perspective(1000px) rotateX(45deg) translateY(-100px);
                    opacity: 0;
                }
                to { 
                    transform: perspective(1000px) rotateX(5deg) translateY(0);
                    opacity: 1;
                }
            }

            .ar-header {
                background: rgba(255,255,255,0.1);
                padding: 1rem 2rem;
                border-radius: 20px 20px 0 0;
                display: flex;
                justify-content: space-between;
                align-items: center;
                color: white;
            }

            .ar-close {
                background: none;
                border: none;
                color: white;
                font-size: 2rem;
                cursor: pointer;
                padding: 0;
                width: 40px;
                height: 40px;
                border-radius: 50%;
                transition: all 0.3s;
            }

            .ar-close:hover {
                background: rgba(255,255,255,0.2);
                transform: rotate(90deg);
            }

            .ar-viewer {
                padding: 2rem;
                color: white;
                text-align: center;
            }

            .ar-product-3d {
                background: rgba(255,255,255,0.1);
                border-radius: 15px;
                padding: 2rem;
                margin-bottom: 2rem;
                backdrop-filter: blur(10px);
                min-height: 300px;
                display: flex;
                align-items: center;
                justify-content: center;
                position: relative;
                overflow: hidden;
            }

            .product-3d-container {
                perspective: 1000px;
                width: 250px;
                height: 250px;
            }

            .product-3d-item {
                width: 100%;
                height: 100%;
                position: relative;
                transform-style: preserve-3d;
                transition: transform 0.5s;
                animation: rotate3d 10s linear infinite;
            }

            @keyframes rotate3d {
                0% { transform: rotateY(0deg) rotateX(10deg); }
                100% { transform: rotateY(360deg) rotateX(10deg); }
            }

            .product-3d-item img {
                width: 100%;
                height: 100%;
                object-fit: contain;
                border-radius: 15px;
                box-shadow: 0 15px 35px rgba(0,0,0,0.3);
                filter: drop-shadow(0 0 20px rgba(255,255,255,0.3));
            }

            .ar-controls {
                display: grid;
                grid-template-columns: repeat(2, 1fr);
                gap: 1rem;
                margin-bottom: 2rem;
            }

            .ar-btn {
                background: rgba(255,255,255,0.2);
                border: 1px solid rgba(255,255,255,0.3);
                color: white;
                padding: 0.8rem 1.5rem;
                border-radius: 25px;
                cursor: pointer;
                transition: all 0.3s;
                font-weight: 600;
                backdrop-filter: blur(10px);
            }

            .ar-btn:hover {
                background: rgba(255,255,255,0.3);
                transform: translateY(-2px);
                box-shadow: 0 8px 25px rgba(255,255,255,0.2);
            }

            .ar-launch {
                background: linear-gradient(45deg, #ff6b6b, #ee5a24) !important;
                grid-column: 1 / -1;
                font-size: 1.1rem;
                padding: 1rem 2rem;
            }

            .ar-info {
                background: rgba(255,255,255,0.1);
                padding: 1.5rem;
                border-radius: 15px;
                margin-bottom: 1rem;
                backdrop-filter: blur(10px);
            }

            .ar-not-supported {
                color: #ffeb3b;
                font-style: italic;
                margin-top: 1rem;
            }

            @media (max-width: 768px) {
                .ar-modal-content {
                    width: 95%;
                    margin: 2% auto;
                }
                
                .ar-controls {
                    grid-template-columns: 1fr;
                }
            }
        `;

        document.head.appendChild(style);
        document.body.appendChild(modal);
    }

    attachEventListeners() {
        // Add AR preview buttons to product cards
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('ar-preview-btn')) {
                e.preventDefault();
                const productCard = e.target.closest('.product-card');
                this.showARPreview(productCard);
            }
        });

        // Close modal
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('ar-close') || e.target.id === 'ar-modal') {
                this.closeARModal();
            }
        });

        // Keyboard controls
        document.addEventListener('keydown', (e) => {
            if (document.getElementById('ar-modal').style.display === 'block') {
                switch(e.key) {
                    case 'Escape':
                        this.closeARModal();
                        break;
                    case 'ArrowLeft':
                        this.rotate('left');
                        break;
                    case 'ArrowRight':
                        this.rotate('right');
                        break;
                    case '+':
                        this.zoom('in');
                        break;
                    case '-':
                        this.zoom('out');
                        break;
                }
            }
        });
    }

    showARPreview(productCard) {
        const modal = document.getElementById('ar-modal');
        const productImage = productCard.querySelector('.product-image');
        const productName = productCard.querySelector('.product-name');
        const productPrice = productCard.querySelector('.product-price');
        const platformBadge = productCard.querySelector('.platform-badge');

        // Update modal content
        document.getElementById('ar-product-image').src = productImage.src;
        document.getElementById('ar-product-name').textContent = productName.textContent;
        document.getElementById('ar-product-price').textContent = productPrice.textContent;
        document.getElementById('ar-product-platform').textContent = `Available on ${platformBadge.textContent}`;

        modal.style.display = 'block';
        document.body.style.overflow = 'hidden';

        // Add entrance animation
        setTimeout(() => {
            modal.querySelector('.ar-modal-content').style.transform = 'perspective(1000px) rotateX(0deg)';
        }, 100);
    }

    closeARModal() {
        const modal = document.getElementById('ar-modal');
        modal.style.display = 'none';
        document.body.style.overflow = 'auto';
    }

    rotate(direction) {
        const product3D = document.querySelector('.product-3d-item');
        const currentTransform = product3D.style.transform || 'rotateY(0deg) rotateX(10deg)';
        const currentY = parseInt(currentTransform.match(/rotateY\((-?\d+)deg\)/)?.[1] || 0);
        const newY = direction === 'left' ? currentY - 45 : currentY + 45;
        
        product3D.style.animation = 'none';
        product3D.style.transform = `rotateY(${newY}deg) rotateX(10deg)`;
        
        // Restart animation after 2 seconds
        setTimeout(() => {
            product3D.style.animation = 'rotate3d 10s linear infinite';
        }, 2000);
    }

    zoom(direction) {
        const container = document.querySelector('.product-3d-container');
        const currentScale = parseFloat(container.style.transform?.match(/scale\(([^)]+)\)/)?.[1] || 1);
        const newScale = direction === 'in' ? 
            Math.min(currentScale * 1.2, 3) : 
            Math.max(currentScale * 0.8, 0.5);
        
        container.style.transform = `scale(${newScale})`;
    }

    async launchAR() {
        if (!this.isARSupported) {
            alert('AR is not supported on this device');
            return;
        }

        try {
            // This would integrate with WebXR API in a real implementation
            const session = await navigator.xr.requestSession('immersive-ar');
            
            // Show AR instructions
            this.showARInstructions();
            
        } catch (error) {
            console.error('AR session failed:', error);
            alert('Could not start AR session. Please try again.');
        }
    }

    showARInstructions() {
        const instructions = document.createElement('div');
        instructions.innerHTML = `
            <div style="position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%); 
                        background: rgba(0,0,0,0.9); color: white; padding: 2rem; 
                        border-radius: 15px; text-align: center; z-index: 10001;">
                <h3>🥽 AR Mode Active</h3>
                <p>Point your camera at a flat surface</p>
                <p>Tap to place the product in your space</p>
                <button onclick="this.parentElement.remove()" 
                        style="background: #3498db; color: white; border: none; 
                               padding: 0.5rem 1rem; border-radius: 5px; margin-top: 1rem;">
                    Got it!
                </button>
            </div>
        `;
        document.body.appendChild(instructions);
        
        setTimeout(() => {
            if (instructions.parentElement) {
                instructions.remove();
            }
        }, 5000);
    }
}

// Initialize AR Preview
const arPreview = new ARProductPreview();

// Add AR buttons to existing product cards
document.addEventListener('DOMContentLoaded', function() {
    const productCards = document.querySelectorAll('.product-card');
    
    productCards.forEach(card => {
        const actionsDiv = card.querySelector('.product-actions');
        if (actionsDiv) {
            const arButton = document.createElement('button');
            arButton.className = 'ar-preview-btn';
            arButton.innerHTML = '3D Preview';
            arButton.title = 'View product in 3D/AR';
            actionsDiv.appendChild(arButton);
        }
    });
});

// Enhanced 3D interactions
document.addEventListener('DOMContentLoaded', function() {
    // Add parallax background elements
    const bgElements = `
        <div class="bg-element bg-element-1"></div>
        <div class="bg-element bg-element-2"></div>
        <div class="bg-element bg-element-3"></div>
    `;
    document.body.insertAdjacentHTML('beforeend', bgElements);

    // Mouse parallax effect
    document.addEventListener('mousemove', (e) => {
        const elements = document.querySelectorAll('.bg-element');
        const x = e.clientX / window.innerWidth;
        const y = e.clientY / window.innerHeight;

        elements.forEach((el, index) => {
            const speed = (index + 1) * 0.5;
            const xPos = (x - 0.5) * speed * 50;
            const yPos = (y - 0.5) * speed * 50;
            el.style.transform = `translate(${xPos}px, ${yPos}px)`;
        });
    });

    // 3D tilt effect for cards
    const cards = document.querySelectorAll('.product-card, .category-card');
    
    cards.forEach(card => {
        card.addEventListener('mousemove', (e) => {
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            
            const centerX = rect.width / 2;
            const centerY = rect.height / 2;
            
            const rotateX = (y - centerY) / 10;
            const rotateY = (centerX - x) / 10;
            
            card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateZ(10px)`;
        });
        
        card.addEventListener('mouseleave', () => {
            card.style.transform = 'perspective(1000px) rotateX(5deg) rotateY(2deg)';
        });
    });

    // Smooth scroll with 3D effect
    const links = document.querySelectorAll('a[href^="#"]');
    links.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const target = document.querySelector(link.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
});