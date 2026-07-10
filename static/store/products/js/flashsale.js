        // Simple filter function for categories


function filterProducts(category) {
    const items = document.querySelectorAll('.product-item');
    const buttons = document.querySelectorAll('.btn-group .btn, .d-flex.flex-wrap.gap-2 .btn');
    
    // Update active button
    buttons.forEach(btn => {
        btn.classList.remove('btn-danger');
        btn.classList.add('btn-outline-secondary');
        if (btn.textContent.trim() === 'Tất cả' && category === 'all') {
            btn.classList.add('btn-danger');
            btn.classList.remove('btn-outline-secondary');
        }
    });
    
    // Find and highlight the clicked category button
    document.querySelectorAll('.d-flex.flex-wrap.gap-2 .btn').forEach(btn => {
        const btnText = btn.textContent.trim().toLowerCase();
        let btnCategory = '';
        if (btnText === 'tất cả') btnCategory = 'all';
        else if (btnText === 'điện thoại') btnCategory = 'phone';
        else if (btnText === 'apple') btnCategory = 'apple';
        else if (btnText === 'laptop') btnCategory = 'laptop';
        else if (btnText === 'phụ kiện') btnCategory = 'accessory';
        else if (btnText === 'đồng hồ') btnCategory = 'watch';
        else if (btnText === 'pc, máy in') btnCategory = 'pc';
        
        if (btnCategory === category) {
            btn.classList.remove('btn-outline-secondary');
            btn.classList.add('btn-danger');
        } else {
            btn.classList.remove('btn-danger');
            btn.classList.add('btn-outline-secondary');
        }
    });
    
    // Filter products
    items.forEach(item => {
        if (category === 'all' || item.dataset.category === category) {
            item.style.display = 'block';
        } else {
            item.style.display = 'none';
        }
    });
}

// Countdown timer
function startTimer() {
    let totalSeconds = 37 * 60 + 58; // 37:58
    
    setInterval(() => {
        if (totalSeconds <= 0) {
            totalSeconds = 24 * 60 * 60; // Reset to 24h
        }
        totalSeconds--;
        
        const hours = Math.floor(totalSeconds / 3600);
        const minutes = Math.floor((totalSeconds % 3600) / 60);
        const seconds = totalSeconds % 60;
        
        document.getElementById('hours').textContent = String(hours).padStart(2, '0');
        document.getElementById('minutes').textContent = String(minutes).padStart(2, '0');
        document.getElementById('seconds').textContent = String(seconds).padStart(2, '0');
    }, 1000);
}

// Initialize timer
document.addEventListener('DOMContentLoaded', startTimer);
// Optional: Click handler for search tags
document.addEventListener('DOMContentLoaded', function() {
    const tags = document.querySelectorAll('.search-tag');
    tags.forEach(tag => {
        tag.addEventListener('click', function() {
            const keyword = this.textContent.trim();
            // Simulate search - you can replace with actual search logic
            alert(`Tìm kiếm: "${keyword}"`);
            // Or redirect to search page:
            // window.location.href = `/tim-kiem?q=${encodeURIComponent(keyword)}`;
        });
    });
});