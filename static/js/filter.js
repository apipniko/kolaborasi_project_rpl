// Store all products data
let allProducts = [];
let currentSort = 'relevant';
let currentFilters = {
    availability: [],
    sub_category: [],
    category: []
};

function normalizeFilterValue(value) {
    return String(value || '')
        .trim()
        .toLowerCase()
        .replace(/\s+/g, '_');
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    // Load all products into array
    loadProducts();
    
    // Setup event listeners
    setupFilterListeners();
    setupSortListeners();
    setupSearchListener();
    setupResetListener();
});

// Load products from DOM into array
function loadProducts() {
    const productCards = document.querySelectorAll('.product-card');
    allProducts = Array.from(productCards).map(card => ({
        element: card,
        availability: normalizeFilterValue(card.dataset.availability),
        subCategory: normalizeFilterValue(card.dataset.subCategory),
        category: normalizeFilterValue(card.dataset.category),
        price: parseFloat(card.dataset.price) || 0,
        rating: parseFloat(card.dataset.rating) || 0,
        purchased: parseInt(card.dataset.purchased) || 0,
        name: card.querySelector('h3').textContent.toLowerCase()
    }));
}


// Setup filter checkbox listeners
function setupFilterListeners() {
    const checkboxes = document.querySelectorAll('.filter-checkbox');
    checkboxes.forEach(checkbox => {
        checkbox.addEventListener('change', function() {
            const filterType = this.dataset.filter;
            const value = normalizeFilterValue(this.value);
            
            if (this.checked) {
                if (!currentFilters[filterType].includes(value)) {
                    currentFilters[filterType].push(value);
                }
            } else {
                currentFilters[filterType] = currentFilters[filterType].filter(v => v !== value);
            }
            
            applyFiltersAndSort();
        });
    });
}

// Setup sort button listeners
function setupSortListeners() {
    const sortButtons = document.querySelectorAll('.sort-btn');
    sortButtons.forEach(button => {
        button.addEventListener('click', function() {
            // Reset semua tombol ke style tidak aktif
            sortButtons.forEach(btn => {
                btn.classList.remove('bg-blue-600', 'text-white', 'border-blue-600');
                btn.classList.add('bg-white', 'text-gray-700', 'border-gray-300');
            });
            
            // Tambahkan style aktif (BIRU) ke tombol yang diklik
            this.classList.remove('bg-white', 'text-gray-700', 'border-gray-300');
            this.classList.add('bg-blue-600', 'text-white', 'border-blue-600');
            
            currentSort = this.dataset.sort;
            applyFiltersAndSort();
        });
    });
}

// Setup search listener
function setupSearchListener() {
    const searchForm = document.getElementById('searchForm');
    const searchInput = document.getElementById('query');
    
    // Search on form submit
    searchForm.addEventListener('submit', function(e) {
        e.preventDefault();
        applyFiltersAndSort();
    });
    
    // Search on input (debounced)
    let searchTimeout;
    searchInput.addEventListener('input', function() {
        clearTimeout(searchTimeout);
        searchTimeout = setTimeout(() => {
            applyFiltersAndSort();
        }, 300);
    });
}

// Setup reset button
function setupResetListener() {
    const resetBtn = document.getElementById('resetFilters');
    resetBtn.addEventListener('click', function() {
        // Reset all checkboxes
        document.querySelectorAll('.filter-checkbox').forEach(cb => cb.checked = false);
        
        // Reset filters
        currentFilters = {
            availability: [],
            sub_category: [],
            category: []
        };
        
        // Reset search
        document.getElementById('query').value = '';
        
        // Reset sort to relevant
        currentSort = 'relevant';
        document.querySelectorAll('.sort-btn').forEach(btn => {
            if (btn.dataset.sort === 'relevant') {
                btn.classList.remove('bg-white', 'text-gray-700', 'border-gray-300');
                btn.classList.add('bg-blue-600', 'text-white', 'border-blue-600');
            } else {
                btn.classList.remove('bg-blue-600', 'text-white', 'border-blue-600');
                btn.classList.add('bg-white', 'text-gray-700', 'border-gray-300');
            }
        });
        
        applyFiltersAndSort();
    });
}

// Apply both filters and sort
function applyFiltersAndSort() {
    const searchTerm = document.getElementById('query').value.toLowerCase().trim();
    
    // Filter products
    let filteredProducts = allProducts.filter(product => {
        // Search filter
        const matchesSearch = product.name.includes(searchTerm);
        
        // Availability filter
        const matchesAvailability = currentFilters.availability.length === 0 || 
            currentFilters.availability.includes(product.availability);
        
        // Sub-category filter
        const matchesSubCategory = currentFilters.sub_category.length === 0 || 
            currentFilters.sub_category.includes(product.subCategory);
        
        // Category filter
        const matchesCategory = currentFilters.category.length === 0 || 
            currentFilters.category.includes(product.category);
        
        return matchesSearch && matchesAvailability && matchesSubCategory && matchesCategory;
    });
    
    // Sort products
    filteredProducts = sortProducts(filteredProducts);
    
    // Update display
    updateProductDisplay(filteredProducts);
}

// Sort products based on current sort option
function sortProducts(products) {
    const sorted = [...products];
    
    switch(currentSort) {
        case 'highest_rating':
            sorted.sort((a, b) => b.rating - a.rating);
            break;
        case 'most_purchased':
            sorted.sort((a, b) => b.purchased - a.purchased);
            break;
        case 'lowest':
            sorted.sort((a, b) => a.price - b.price);
            break;
        case 'relevant':
        default:
            // Default: urutkan berdasarkan total_purchased (terlaris)
            sorted.sort((a, b) => b.purchased - a.purchased);
            break;
    }
    
    return sorted;
}

// Update product display
function updateProductDisplay(products) {
    const grid = document.getElementById('productGrid');
    const noResults = document.getElementById('noResults');
    const countSpan = document.getElementById('productCount');
    
    // Hide all products first
    allProducts.forEach(product => {
        product.element.style.display = 'none';
    });
    
    // Show filtered products in sorted order
    products.forEach(product => {
        product.element.style.display = 'block';
        grid.appendChild(product.element); // Reorder in DOM
    });
    
    // Update count
    countSpan.textContent = products.length;
    
    // Show/hide no results message
    if (products.length === 0) {
        noResults.classList.remove('hidden');
        grid.classList.add('hidden');
    } else {
        noResults.classList.add('hidden');
        grid.classList.remove('hidden');
    }
}
