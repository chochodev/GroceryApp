// FOR DELETE FUNCTION
const delButton = document.getElementById('del-button');

delButton.addEventListener('click', (e) => {
    // Prevents the form default function from happening
    e.preventDefault();

    // Extract the product ID from the form data attribute
    const productId = editProductForm.dataset.productId;

    // Make a fetch request to perform the PUT request
    fetch(`/admin_panel/delete-product/${productId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ delete: 'delete' })
    })
    .then(response => {
        if (response.ok) {
            // Handle the success case
            console.log('POST request successful');
            // Redirect to the desired page
            window.location.href = '/admin_panel/products'
        } else {
            // Handle the error case
            console.log('PUT request failed');
        }
    })
    .catch(error => {
        // Handle any network or other errors
        console.error('Error:', error);
    });
})