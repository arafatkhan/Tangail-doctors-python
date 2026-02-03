// AJAX Filter System for all pages

document.addEventListener('DOMContentLoaded', function() {
    // Get search form and input
    const searchForm = document.querySelector('.search-box form');
    const searchInput = searchForm ? searchForm.querySelector('input[name="search"]') : null;
    
    // Get category buttons
    const categoryButtons = document.querySelectorAll('.category-filter a');
    
    // Get main content area
    const contentArea = document.querySelector('.row');
    const loadingOverlay = document.getElementById('loadingOverlay');
    
    // Debounce function for search
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
    
    // Function to perform AJAX request
    function performFilter(url) {
        // Show loading indicator
        if (loadingOverlay) {
            loadingOverlay.classList.add('active');
        }
        if (contentArea) {
            contentArea.style.opacity = '0.7';
        }
        
        fetch(url, {
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(response => response.text())
        .then(html => {
            // Parse the HTML response
            const parser = new DOMParser();
            const doc = parser.parseFromString(html, 'text/html');
            
            // Get the new content
            const newContent = doc.querySelector('.row');
            const newPagination = doc.querySelector('.pagination');
            const newAlert = doc.querySelector('.alert-info');
            
            // Update content
            if (contentArea && newContent) {
                contentArea.innerHTML = newContent.innerHTML;
            }
            
            // Update pagination if exists
            const oldPagination = document.querySelector('.pagination');
            if (oldPagination && newPagination) {
                oldPagination.parentElement.innerHTML = newPagination.parentElement.innerHTML;
            } else if (oldPagination && !newPagination) {
                oldPagination.parentElement.remove();
            }
            
            // Update alert info
            const oldAlert = document.querySelector('.alert-info');
            if (oldAlert && newAlert) {
                oldAlert.innerHTML = newAlert.innerHTML;
            }
            
            // Update URL without reload
            window.history.pushState({}, '', url);
            
            // Re-attach pagination listeners
            attachPaginationListeners();
            
            // Scroll to top smoothly
            window.scrollTo({ top: 0, behavior: 'smooth' });
        })
        .catch(error => {
            console.error('Filter error:', error);
        })
        .finally(() => {
            if (loadingOverlay) {
                loadingOverlay.classList.remove('active');
            }
            if (contentArea) {
                contentArea.style.opacity = '1';
                contentArea.style.pointerEvents = 'auto';
            }
        });
    }
    
    // Handle search input
    if (searchInput) {
        // Function to perform search
        function performSearch() {
            const searchValue = searchInput.value.trim();
            const currentUrl = new URL(window.location);
            
            if (searchValue) {
                currentUrl.searchParams.set('search', searchValue);
            } else {
                currentUrl.searchParams.delete('search');
            }
            
            // Reset to page 1 when searching
            currentUrl.searchParams.delete('page');
            
            performFilter(currentUrl.toString());
        }
        
        // Debounced search for input typing
        const debouncedSearch = debounce(performSearch, 500);
        searchInput.addEventListener('input', debouncedSearch);
        
        // Handle form submission (search button click)
        if (searchForm) {
            searchForm.addEventListener('submit', function(e) {
                e.preventDefault();
                performSearch(); // Trigger search immediately on button click
            });
        }
    }
    
    // Handle category buttons
    categoryButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const url = this.getAttribute('href');
            performFilter(url);
            
            // Update active state
            categoryButtons.forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');
        });
    });
    
    // Handle pagination
    function attachPaginationListeners() {
        const paginationLinks = document.querySelectorAll('.pagination a');
        paginationLinks.forEach(link => {
            link.addEventListener('click', function(e) {
                e.preventDefault();
                const url = this.getAttribute('href');
                if (url) {
                    performFilter(url);
                }
            });
        });
    }
    
    // Initial attachment
    attachPaginationListeners();
    
    // Handle browser back/forward buttons
    window.addEventListener('popstate', function() {
        location.reload();
    });
});
