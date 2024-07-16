// static/script.js
document.addEventListener('DOMContentLoaded', function () {
    const imageInput = document.getElementById('image-input');
    const processButton = document.getElementById('process-button');
    const resultContainer = document.getElementById('result-container');
    const resultName = document.getElementById('result-name');
    const resultEmail = document.getElementById('result-email');
    const resultPhone = document.getElementById('result-phone');

    processButton.addEventListener('click', function () {
        if (imageInput.files.length === 0) {
            alert('Please select an image to process.');
            return;
        }

        const formData = new FormData();
        formData.append('image', imageInput.files[0]);

        fetch('/process_image', {
            method: 'POST',
            body: formData,
        })
        .then(response => response.json())  // Expect JSON response
        .then(data => {
            resultName.textContent = data.name;
            resultEmail.textContent = data.email;
            resultPhone.textContent = data['phone number'];
            resultContainer.style.display = 'block';  // Show the result
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred.');
        });
    });
});
