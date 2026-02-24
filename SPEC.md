# QueueBlaze - Weed Dispensary Website

## Project Overview
- **Project Name**: QueueBlaze
- **Type**: E-commerce Website (Cannabis/Weed Dispensary)
- **Core Functionality**: Product showcase, online ordering, service bookings
- **Target Users**: Adult cannabis consumers in South Africa (21+)
- **Platform**: Netlify (static hosting)

## UI/UX Specification

### Layout Structure
- **Header**: Fixed navigation with logo, menu links, cart icon
- **Hero Section**: Full-width banner with CTA buttons
- **Features Section**: Service highlights with icons
- **Products Section**: Grid of cannabis products with categories
- **About Section**: Company information
- **Contact Section**: Contact form and business hours
- **Footer**: Links, social media, legal disclaimers

### Responsive Breakpoints
- Mobile: < 768px (single column)
- Tablet: 768px - 1024px (2 columns)
- Desktop: > 1024px (3-4 columns)

### Visual Design

#### Color Palette
- Primary: `#1a1a2e` (Deep Navy)
- Secondary: `#16213e` (Dark Blue)
- Accent: `#e94560` (Vibrant Red/Pink)
- Success: `#00d9a5` (Green)
- Text Light: `#ffffff`
- Text Muted: `#a0a0a0`
- Background: `#0f0f1a`

#### Typography
- Headings: 'Poppins', sans-serif (bold, modern)
- Body: 'Open Sans', sans-serif
- Hero Title: 3.5rem (desktop), 2rem (mobile)
- Section Titles: 2.5rem
- Body Text: 1rem

#### Spacing System
- Section Padding: 80px vertical (desktop), 40px (mobile)
- Container Max Width: 1200px
- Card Gap: 30px
- Element Margin: 20px

#### Visual Effects
- Card hover: translateY(-10px), box-shadow
- Button hover: background color shift, scale(1.05)
- Smooth scroll behavior
- Fade-in animations on scroll
- Glassmorphism effects on cards

### Components

#### Navigation
- Logo (left)
- Menu links: Home, Products, About, Contact
- Cart icon with item count badge
- Mobile hamburger menu

#### Hero Banner
- Background image with overlay
- Main headline
- Subheadline
- Two CTA buttons: "Shop Now" (primary), "Contact Us" (secondary)

#### Product Cards
- Product image
- Product name
- Strain type badge (Sativa/Indica/Hybrid)
- THC level
- Price
- "Add to Cart" button

#### Shopping Cart
- Slide-out drawer
- Product list with quantity controls
- Subtotal calculation
- Checkout button

#### Contact Form
- Name field
- Email field
- Phone field
- Message textarea
- Submit button

## Functionality Specification

### Core Features
1. **Product Catalog**
   - Display products in grid layout
   - Filter by category (Flower, Edibles, Concentrates, Accessories)
   - Filter by strain type (Sativa, Indica, Hybrid)
   - Search functionality

2. **Shopping Cart**
   - Add/remove items
   - Update quantities
   - Calculate totals
   - Persist cart in localStorage

3. **Service Booking**
   - Contact form for inquiries
   - Form validation
   - Success message on submission

4. **SEO Optimization**
   - Semantic HTML5
   - Meta tags (title, description, keywords)
   - Open Graph tags
   - Alt tags on images
   - Fast loading (minimal dependencies)

5. **Mobile Experience**
   - Responsive design
   - Touch-friendly buttons
   - Optimized images
   - Fast load times

### User Interactions
- Click product card → Add to cart
- Click cart icon → Open cart drawer
- Click category filter → Filter products
- Scroll → Trigger animations
- Submit form → Show success message

## Acceptance Criteria

1. ✓ Website loads in under 3 seconds
2. ✓ Fully responsive on all devices
3. ✓ Cart functionality works correctly
4. ✓ All links and buttons are clickable
5. ✓ SEO meta tags are present
6. ✓ Netlify deployment works
7. ✓ Professional, modern appearance
8. ✓ Age verification on first visit (21+)
