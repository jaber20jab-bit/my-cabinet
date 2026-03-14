// 🗄️ Cabinet - Main JS

// Language Toggle
function toggleLang() {
    const url = new URL(window.location.href);
    const lang = url.searchParams.get('lang') || 'ar';
    url.searchParams.set('lang', lang === 'ar' ? 'en' : 'ar');
    window.location.href = url.href;
}

// Search Overlay
function toggleSearch() {
    const overlay = document.getElementById('searchOverlay');
    overlay.classList.toggle('active');
    if (overlay.classList.contains('active')) {
        overlay.querySelector('input').focus();
    }
}

// Keyboard Shortcuts
document.addEventListener('keydown', function(e) {
    // Ctrl/Cmd + K = Search
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        toggleSearch();
    }
    // Escape = Close search
    if (e.key === 'Escape') {
        document.getElementById('searchOverlay').classList.remove('active');
    }
});

// Confirm delete
document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.delete-form').forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!confirm('هل أنت متأكد من الحذف؟')) {
                e.preventDefault();
            }
        });
    });
});
