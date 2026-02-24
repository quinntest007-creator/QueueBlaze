/* ========================================
   QueueBlaze - Main JavaScript
   E-commerce Functionality
   ======================================== */

// Get products from DOM (rendered by Django)
function getProductsFromDOM() {
    const productCards = document.querySelectorAll('.product-card');
    const products = [];
    
    productCards.forEach(card => {
        products.push({
            id: parseInt(card.dataset.id || card.querySelector('.btn-add-cart').onclick.toString().match(/addToCart\((\d+)\)/)?.[1] || 0),
            name: card.querySelector('.product-name').textContent,
            category: card.dataset.category,
            strain: card.dataset.strain,
            thc: card.querySelector('.product-thc').textContent,
            price: parseFloat(card.querySelector('.product-price').textContent.replace('R', '')),
            icon: card.querySelector('.product-placeholder').textContent.trim(),
            description: ''
        });
    });
    
    return products;
}

// Cart State
let cart = JSON.parse(localStorage.getItem('queueblaze_cart')) || [];

// Current Filter State
let currentCategory = 'all';
let currentStrain = 'all';
let searchQuery = '';

// DOM Elements
const cartBtn = document.getElementById('cart-btn');
const cartSidebar = document.getElementById('cart-sidebar');
const cartOverlay = document.getElementById('cart-overlay');
const cartClose = document.getElementById('cart-close');
const cartItems = document.getElementById('cart-items');
const cartCount = document.getElementById('cart-count');
const cartTotal = document.getElementById('cart-total');
const checkoutBtn = document.getElementById('checkout-btn');
const menuToggle = document.getElementById('menu-toggle');
const nav = document.getElementById('nav');
const header = document.getElementById('header');
const ageModal = document.getElementById('age-modal');
const ageVerify = document.getElementById('age-verify');
const ageDeny = document.getElementById('age-deny');
const toast = document.getElementById('toast');
const filterBtns = document.querySelectorAll('.filter-btn');
const strainBtns = document.querySelectorAll('.strain-btn');
const searchInput = document.getElementById('search-input');
const contactForm = document.getElementById('contact-form');
const themeToggle = document.getElementById('theme-toggle');
const productsGrid = document.getElementById('products-grid');

// ========================================
// Initialize
// ========================================
document.addEventListener('DOMContentLoaded', () => {
    checkAgeVerification();
    initTheme();
    updateCartUI();
    setupEventListeners();
    initViewMore();
});

// ========================================
// Age Verification
// ========================================
function checkAgeVerification() {
    const isVerified = localStorage.getItem('queueblaze_age_verified');
    if (isVerified) {
        ageModal.classList.remove('active');
    } else {
        ageModal.classList.add('active');
    }
}

ageVerify.addEventListener('click', () => {
    localStorage.setItem('queueblaze_age_verified', 'true');
    ageModal.classList.remove('active');
});

ageDeny.addEventListener('click', () => {
    window.location.href = 'https://www.google.com';
});

// ========================================
// Render Products (for filtering)
// ========================================
function renderProducts(products) {
    if (products.length === 0) {
        productsGrid.innerHTML = `
            <div class="no-products" style="grid-column: 1/-1; text-align: center; padding: 60px 20px;">
                <i class="fas fa-search" style="font-size: 3rem; color: var(--text-muted); margin-bottom: 20px;"></i>
                <p style="color: var(--text-muted);">No products found matching your criteria</p>
            </div>
        `;
        return;
    }

    productsGrid.innerHTML = products.map(product => `
        <div class="product-card" data-category="${product.category}" data-strain="${product.strain}" data-id="${product.id}" data-image="${product.image || ''}">
            <div class="product-image">
                ${product.image ? `<img src="${product.image}" alt="${product.name}" class="product-img">` : `<div class="product-placeholder">${product.icon}</div>`}
                <span class="product-badge strain-${product.strain}">${capitalizeFirst(product.strain)}</span>
            </div>
            <div class="product-info">
                <h3 class="product-name">${product.name}</h3>
                <div class="product-meta">
                    <span class="product-thc">${product.thc || '--'}</span>
                    <span class="product-price">R${product.price}</span>
                </div>
                <button class="btn-add-cart" onclick="addToCart(${product.id})">
                    <i class="fas fa-shopping-cart"></i> Add to Cart
                </button>
            </div>
        </div>
    `).join('');
}

// ========================================
// Cart Functions
// ========================================
function addToCart(productId) {
    // Get product from DOM
    const productCard = document.querySelector(`.product-card[data-id="${productId}"]`);
    if (!productCard) return;
    
    const product = {
        id: productId,
        name: productCard.querySelector('.product-name').textContent,
        price: parseFloat(productCard.querySelector('.product-price').textContent.replace('R', '')),
        icon: productCard.querySelector('.product-placeholder') ? productCard.querySelector('.product-placeholder').textContent.trim() : '',
        image: productCard.dataset.image || '',
        quantity: 1
    };
    
    const existingItem = cart.find(item => item.id === productId);

    if (existingItem) {
        existingItem.quantity++;
    } else {
        cart.push(product);
    }

    saveCart();
    updateCartUI();
    showToast(`${product.name} added to cart!`);
}

function removeFromCart(productId) {
    cart = cart.filter(item => item.id !== productId);
    saveCart();
    updateCartUI();
}

function updateQuantity(productId, change) {
    const item = cart.find(item => item.id === productId);
    if (item) {
        item.quantity += change;
        if (item.quantity <= 0) {
            removeFromCart(productId);
        } else {
            saveCart();
            updateCartUI();
        }
    }
}

function saveCart() {
    localStorage.setItem('queueblaze_cart', JSON.stringify(cart));
}

function updateCartUI() {
    // Update cart count
    const totalItems = cart.reduce((sum, item) => sum + item.quantity, 0);
    cartCount.textContent = totalItems;

    // Update cart total
    const total = cart.reduce((sum, item) => sum + (item.price * item.quantity), 0);
    cartTotal.textContent = `R${total}`;

    // Render cart items
    if (cart.length === 0) {
        cartItems.innerHTML = `
            <div class="cart-empty">
                <i class="fas fa-shopping-basket"></i>
                <p>Your cart is empty</p>
            </div>
        `;
    } else {
        cartItems.innerHTML = cart.map(item => `
            <div class="cart-item">
                <div class="cart-item-image">${item.image ? `<img src="${item.image}" alt="${item.name}">` : item.icon}</div>
                <div class="cart-item-info">
                    <h4 class="cart-item-name">${item.name}</h4>
                    <span class="cart-item-price">R${item.price}</span>
                    <div class="cart-item-quantity">
                        <button class="quantity-btn" onclick="updateQuantity(${item.id}, -1)">-</button>
                        <span class="quantity-value">${item.quantity}</span>
                        <button class="quantity-btn" onclick="updateQuantity(${item.id}, 1)">+</button>
                    </div>
                </div>
                <i class="fas fa-trash cart-item-remove" onclick="removeFromCart(${item.id})"></i>
            </div>
        `).join('');
    }
}

function toggleCart() {
    cartSidebar.classList.toggle('active');
    cartOverlay.classList.toggle('active');
}

// ========================================
// Checkout
// ========================================
checkoutBtn.addEventListener('click', () => {
    if (cart.length === 0) {
        showToast('Your cart is empty!');
        return;
    }
    
    // Redirect to checkout page
    window.location.href = '/checkout/';
});

// ========================================
// Toast Notification
// ========================================
function showToast(message) {
    const toastMessage = toast.querySelector('.toast-message');
    toastMessage.textContent = message;
    toast.classList.add('active');
    
    setTimeout(() => {
        toast.classList.remove('active');
    }, 3000);
}

// ========================================
// Event Listeners
// ========================================
function setupEventListeners() {
    // Theme Toggle
    themeToggle.addEventListener('click', toggleTheme);
    
    // Cart
    cartBtn.addEventListener('click', toggleCart);
    cartClose.addEventListener('click', toggleCart);
    cartOverlay.addEventListener('click', toggleCart);

    // Mobile Menu
    menuToggle.addEventListener('click', () => {
        nav.classList.toggle('active');
        menuToggle.classList.toggle('active');
    });

    // Header Scroll
    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            header.classList.add('scrolled');
        } else {
            header.classList.remove('scrolled');
        }
    });

    // Category Filters
    filterBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            filterBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            currentCategory = btn.dataset.filter;
            filterProducts();
        });
    });

    // Strain Filters
    strainBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            strainBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            currentStrain = btn.dataset.strain;
            filterProducts();
        });
    });

    // Search
    searchInput.addEventListener('input', (e) => {
        searchQuery = e.target.value.toLowerCase();
        filterProducts();
    });

    // Contact Form
    contactForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const name = document.getElementById('name').value;
        const email = document.getElementById('email').value;
        const phone = document.getElementById('phone').value;
        const subject = document.getElementById('subject').value;
        const message = document.getElementById('message').value;
        
        // Save inquiry to database (admin panel)
        try {
            const response = await fetch('/api/save-inquiry/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify({
                    name, email, phone, subject, message
                })
            });
            
            if (response.ok) {
                showToast('Message sent successfully! We will contact you soon.');
                contactForm.reset();
            } else {
                showToast('Failed to send message. Please try again.');
            }
        } catch (e) {
            console.log('Inquiry save failed:', e);
            showToast('Failed to send message. Please try again.');
        }
    });

    // Smooth Scroll for Navigation
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
                // Close mobile menu if open
                nav.classList.remove('active');
                menuToggle.classList.remove('active');
            }
        });
    });

    // Active nav link on scroll
    const sections = document.querySelectorAll('section[id]');
    
    window.addEventListener('scroll', () => {
        let current = '';
        
        sections.forEach(section => {
            const sectionTop = section.offsetTop;
            const sectionHeight = section.clientHeight;
            
            if (scrollY >= sectionTop - 200) {
                current = section.getAttribute('id');
            }
        });
        
        document.querySelectorAll('.nav-link').forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href') === `#${current}`) {
                link.classList.add('active');
            }
        });
    });
}

// ========================================
// Filter Products
// ========================================

// View More Products
let productsShown = 4;
const productsPerLoad = 8;
const mobileProductsShown = 2;

function initViewMore() {
    const viewMoreContainer = document.getElementById('view-more-container');
    const productCards = document.querySelectorAll('.product-card');
    
    // Check if mobile
    const isMobile = window.innerWidth < 768;
    
    if (isMobile) {
        // On mobile, show only 2 products initially
        productCards.forEach((card, index) => {
            if (index < mobileProductsShown) {
                card.style.display = 'block';
            } else {
                card.style.display = 'none';
            }
        });
        
        // Show view more button if there are more than 2 products
        if (productCards.length > mobileProductsShown && viewMoreContainer) {
            viewMoreContainer.style.display = 'block';
        }
        
        productsShown = mobileProductsShown;
    } else {
        // On desktop, show only first 4 products initially
        productCards.forEach((card, index) => {
            if (index < 4) {
                card.style.display = 'block';
            } else {
                card.style.display = 'none';
            }
        });
        
        // Show view more button if there are more than 4 products
        if (productCards.length > 4 && viewMoreContainer) {
            viewMoreContainer.style.display = 'block';
        }
        
        productsShown = 4;
    }
}

function viewMoreProducts() {
    const productCards = Array.from(document.querySelectorAll('.product-card'));
    const isMobile = window.innerWidth < 768;
    const loadCount = isMobile ? 4 : 8;
    
    let shown = 0;
    for (let i = 0; i < productCards.length; i++) {
        if (productCards[i].style.display === 'none') {
            productCards[i].style.display = 'block';
            shown++;
            if (shown >= loadCount) {
                break;
            }
        }
    }
    
    // Toggle buttons based on visibility
    const viewMoreBtn = document.getElementById('btn-view-more');
    const viewLessBtn = document.getElementById('btn-view-less');
    const newVisibleCount = productCards.filter(card => card.style.display !== 'none').length;
    
    if (newVisibleCount >= productCards.length && viewMoreBtn) {
        viewMoreBtn.classList.add('hidden');
    }
    if (viewLessBtn) {
        viewLessBtn.classList.remove('hidden');
    }
    
    // Apply current filters to newly shown products
    filterProducts();
}

function viewLessProducts() {
    const productCards = Array.from(document.querySelectorAll('.product-card'));
    const isMobile = window.innerWidth < 768;
    const initialCount = isMobile ? 2 : 4;
    
    // First, reset all cards to visible, then hide the ones beyond initial count
    productCards.forEach(card => {
        card.style.display = 'block';
    });
    
    // Hide products beyond initial count
    for (let i = initialCount; i < productCards.length; i++) {
        productCards[i].style.display = 'none';
    }
    
    // Toggle buttons - show View More, hide View Less
    const viewMoreBtn = document.getElementById('btn-view-more');
    const viewLessBtn = document.getElementById('btn-view-less');
    
    if (viewMoreBtn) {
        viewMoreBtn.classList.remove('hidden');
    }
    if (viewLessBtn) {
        viewLessBtn.classList.add('hidden');
    }
    
    // IMPORTANT: Do NOT call filterProducts() here as it will override the view less functionality
}

function filterProducts() {
    const productCards = document.querySelectorAll('.product-card');
    
    productCards.forEach(card => {
        const category = card.dataset.category;
        const strain = card.dataset.strain;
        const name = card.querySelector('.product-name').textContent.toLowerCase();
        
        const categoryMatch = currentCategory === 'all' || category === currentCategory;
        const strainMatch = currentStrain === 'all' || strain === currentStrain || strain === 'all';
        const searchMatch = name.includes(searchQuery);
        
        if (categoryMatch && strainMatch && searchMatch) {
            card.style.display = 'block';
        } else {
            card.style.display = 'none';
        }
    });
    
    // Check if any products are visible
    const visibleProducts = document.querySelectorAll('.product-card[style="display: block;"], .product-card:not([style*="display"])');
    const hasVisibleProducts = Array.from(productCards).some(card => card.style.display !== 'none');
    
    if (!hasVisibleProducts && productCards.length > 0) {
        productsGrid.innerHTML = `
            <div class="no-products" style="grid-column: 1/-1; text-align: center; padding: 60px 20px;">
                <i class="fas fa-search" style="font-size: 3rem; color: var(--text-muted); margin-bottom: 20px;"></i>
                <p style="color: var(--text-muted);">No products found matching your criteria</p>
            </div>
        `;
    } else if (hasVisibleProducts) {
        // Restore original content if it was replaced
        if (productsGrid.querySelector('.no-products')) {
            filterProducts();
        }
    }
}

// ========================================
// Theme Functions
// ========================================
function initTheme() {
    const savedTheme = localStorage.getItem('queueblaze_theme');
    if (savedTheme === 'light') {
        document.body.classList.add('light-theme');
        updateThemeIcon('light');
    }
}

function toggleTheme() {
    const isLight = document.body.classList.toggle('light-theme');
    const theme = isLight ? 'light' : 'dark';
    localStorage.setItem('queueblaze_theme', theme);
    updateThemeIcon(theme);
}

function updateThemeIcon(theme) {
    const icon = themeToggle.querySelector('i');
    if (theme === 'light') {
        icon.classList.remove('fa-moon');
        icon.classList.add('fa-sun');
    } else {
        icon.classList.remove('fa-sun');
        icon.classList.add('fa-moon');
    }
}

// ========================================
// Utility Functions
// ========================================
function capitalizeFirst(str) {
    if (!str) return '';
    return str.charAt(0).toUpperCase() + str.slice(1);
}

// Get CSRF token for AJAX requests
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Make functions globally available
window.addToCart = addToCart;
window.removeFromCart = removeFromCart;
window.updateQuantity = updateQuantity;
