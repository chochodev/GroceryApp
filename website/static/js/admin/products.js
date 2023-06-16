function redirectToEditProduct(productId) {
    fetch(`/admin_panel/edit-product/${productId}`, {
        method: 'GET'
    })
    .then(response => {
        if (response.ok) {
            window.location.href = `/admin_panel/edit-product/${productId}`;
        } else {
            // Handle the error case
            console.error('Error:', response.status);
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}