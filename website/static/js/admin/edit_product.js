// Get the form element
const editProductForm = document.getElementById('edit-product-form');

// Add an event listener for form submission
editProductForm.addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent the default form submission

    // Extract the product ID from the form data attribute
    const productId = editProductForm.dataset.productId;

    // Create a new FormData object to capture the form data
    const formData = new FormData(editProductForm);
    console.log(formData)
    // Make a fetch request to perform the PUT request
    fetch(`/admin_panel/edit-product/${productId}`, {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (response.ok) {
            // Handle the success case
            console.log('UPDATE request successful');
            window.location.href = '/admin_panel/products'
            // Redirect to the desired page or perform any other action
        } else {
            // Handle the error case
            console.log('UPDATE request failed');
            // Display an error message or perform any other action
        }
    })
    .catch(error => {
        // Handle any network or other errors
        console.error('Error:', error);
    });
});

