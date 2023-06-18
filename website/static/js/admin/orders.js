const allOrders = document.getElementById('all-orders');
const approvedOrders = document.getElementById('approved-orders');
const unApprovedOrders = document.getElementById('unapproved-orders');

const allButton = document.getElementById('all-orders-button');
const approvedButton = document.getElementById('approved-orders-button');
const unApprovedButton = document.getElementById('unapproved-orders-button');

allButton.addEventListener('click', () => {
  allOrders.style.display = 'flex';  // Show all orders
  approvedOrders.style.display = 'none';  // Hide approved orders
  unApprovedOrders.style.display = 'none';  // Hide unapproved orders

  allButton.classList.add('active');
  approvedButton.classList.remove('active');
  unApprovedButton.classList.remove('active');
});

approvedButton.addEventListener('click', () => {
  allOrders.style.display = 'none';  // Hide all orders
  approvedOrders.style.display = 'flex';  // Show approved orders
  unApprovedOrders.style.display = 'none';  // Hide unapproved orders
  
  allButton.classList.remove('active');
  approvedButton.classList.add('active');
  unApprovedButton.classList.remove('active');
});

unApprovedButton.addEventListener('click', () => {
  allOrders.style.display = 'none';  // Hide all orders
  approvedOrders.style.display = 'none';  // Hide approved orders
  unApprovedOrders.style.display = 'flex';  // Show unapproved orders
  
  allButton.classList.remove('active');
  approvedButton.classList.remove('active');
  unApprovedButton.classList.add('active');
});