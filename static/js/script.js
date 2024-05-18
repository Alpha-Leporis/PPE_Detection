document.addEventListener('DOMContentLoaded', function () {
    const form = document.querySelector('form');
    const loadingDiv = document.getElementById('loading');

    if (form) {
        form.addEventListener('submit', function () {
            loadingDiv.style.display = 'block';
        });
    }
});

function deleteImageAndRedirect(filename) {
    fetch(`/delete/${filename}`, {
        method: 'POST'
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            window.location.href = "/";
        } else {
            alert("Failed to delete the image: " + data.error);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert("An error occurred while deleting the image.");
    });
}
