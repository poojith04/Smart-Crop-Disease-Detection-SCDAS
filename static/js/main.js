// Mobile-optimized file input handling
const fileInput = document.getElementById('fileInput');
const fileLabel = document.getElementById('fileLabel');
const submitBtn = document.getElementById('submitBtn');
const imagePreview = document.getElementById('imagePreview');
const locationStatus = document.getElementById('locationStatus');

// Ensure file input triggers on mobile devices
fileLabel.addEventListener('click', function(e) {
    // For mobile devices, explicitly trigger the file input
    if ('ontouchstart' in window) {
        e.preventDefault();
        fileInput.click();
    }
});

// Also handle touch events
fileLabel.addEventListener('touchend', function(e) {
    e.preventDefault();
    fileInput.click();
});

// Image preview and button enable
fileInput.addEventListener('change', function(e) {
    const file = e.target.files[0];
    if (file) {
        // Enable submit button
        submitBtn.disabled = false;
        
        // Show preview
        const reader = new FileReader();
        reader.onload = function(event) {
            imagePreview.innerHTML = `<img src="${event.target.result}" alt="Preview">`;
        };
        reader.readAsDataURL(file);
        
        // Update label text
        fileLabel.querySelector('.upload-text').textContent = '✓ Image selected';
    }
});

// GPS Location with better error handling
if (navigator.geolocation) {
    // Set a timeout for location request
    const locationTimeout = setTimeout(function() {
        locationStatus.innerHTML = '<p style="color: orange;">⚠️ Location timeout. Continuing without location data.</p>';
    }, 5000);
    
    navigator.geolocation.getCurrentPosition(
        function(position) {
            clearTimeout(locationTimeout);
            document.getElementById('latitude').value = position.coords.latitude;
            document.getElementById('longitude').value = position.coords.longitude;
            locationStatus.innerHTML = '<p style="color: green;">✅ Location detected successfully!</p>';
        },
        function(error) {
            clearTimeout(locationTimeout);
            console.log('Location error:', error);
            
            let errorMessage = '';
            switch(error.code) {
                case error.PERMISSION_DENIED:
                    errorMessage = '⚠️ Location access denied. Continuing without location-based advice.';
                    break;
                case error.POSITION_UNAVAILABLE:
                    errorMessage = '⚠️ Location information unavailable. Continuing without location data.';
                    break;
                case error.TIMEOUT:
                    errorMessage = '⚠️ Location request timeout. Continuing without location data.';
                    break;
                default:
                    errorMessage = '⚠️ Location error. Continuing without location data.';
            }
            
            locationStatus.innerHTML = `<p style="color: orange;">${errorMessage}</p>`;
        },
        {
            enableHighAccuracy: false,
            timeout: 5000,
            maximumAge: 0
        }
    );
} else {
    locationStatus.innerHTML = '<p style="color: red;">❌ Geolocation not supported by browser.</p>';
}

// Form submission handling
document.getElementById('uploadForm').addEventListener('submit', function(e) {
    submitBtn.innerHTML = '⏳ Analyzing rice disease...';
    submitBtn.disabled = true;
});

// Prevent double-tap zoom on buttons (mobile)
document.querySelectorAll('.btn, .file-label').forEach(function(element) {
    element.addEventListener('touchend', function(e) {
        e.preventDefault();
        element.click();
    }, { passive: false });
});
