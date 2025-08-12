// Custom JS for Expense Tracker
// Placeholder for future enhancements
// Example: Smooth scroll to top
document.addEventListener('DOMContentLoaded', function() {
	const toTopBtn = document.getElementById('toTopBtn');
	if (toTopBtn) {
		toTopBtn.addEventListener('click', function() {
			window.scrollTo({ top: 0, behavior: 'smooth' });
		});
	}
});
