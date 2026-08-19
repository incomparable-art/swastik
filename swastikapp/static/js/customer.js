
// Get & Set all the Customers
function loadCustomers() {
    // 1. Define a function to load table rows
    $.ajax({
        url: '/api/get-customers',
        type: 'GET',
        success: function (response) {
            // 1. Target the array inside the response object
            let customerArray = response.customers || [];

            // 2. Clear existing table body rows (optional)
            $('#customerTableBody').empty();

            // 3. Now loop through the array safely
            customerArray.forEach(function (customer) {
                let row = `
               <tr id="customer-row-${customer.id}">
                <td class="p-2 align-middle bg-transparent border-b dark:border-white/40 whitespace-nowrap shadow-transparent">
                  <div class="flex px-2 py-1">
                    <div>
                      <img src="static/img/team-2.jpg" class="inline-flex items-center justify-center mr-4 text-sm text-white transition-all duration-200 ease-in-out h-9 w-9 rounded-xl" alt="user1" />
                    </div>
                    <div class="flex flex-col justify-center">
                      <h6 class="mb-0 text-sm leading-normal dark:text-white">${customer.name}</h6>
                      <p class="mb-0 text-xs leading-tight dark:text-white dark:opacity-80 text-slate-400">${customer.address}</p>
                      <p class="mb-0 text-xs font-semibold leading-tight dark:text-white dark:opacity-80">${customer.tin} | ${customer.contact}</p>
                    </div>
                  </div>
                </td>
                <td>
                  <button class="btn-delete relative z-10 inline-block px-4 py-2.5 mb-0 font-bold text-center text-transparent align-middle transition-all border-0 rounded-lg shadow-none cursor-pointer leading-normal text-sm ease-in bg-150 bg-gradient-to-tl from-red-600 to-orange-600 hover:-translate-y-px active:opacity-85 bg-x-25 bg-clip-text"
                          data-id=${customer.id} data-name=${customer.name}>
                          <i class="mr-2 far fa-trash-alt bg-150 bg-gradient-to-tl from-red-600 to-orange-600 bg-x-25 bg-clip-text" aria-hidden="true"></i>
                    Delete
                  </button>

                  <button class="btn-edit1 inline-block dark:text-white px-4 py-2.5 mb-0 font-bold text-center align-middle transition-all bg-transparent border-0 rounded-lg shadow-none cursor-pointer leading-normal text-sm ease-in bg-150 hover:-translate-y-px active:opacity-85 bg-x-25 text-slate-700"
                          data-id=${customer.id}>
                          <i class="mr-2 fas fa-pencil-alt text-slate-700" aria-hidden="true"></i>
                    Edit
                  </button>
                </td>
              </tr>
            `;

                // 3. Append directly to the tbody ID
                $('#customerTableBody').append(row);
            });
        }
    });
}

// Customer delete functionality
$(document).on('click', '.btn-delete', function() {

    let customerId = $(this).data('id');
    let customerName = $(this).data('name');

    // Set values inside the delete modal
    $('#deleteCustomerId').val(customerId);
    $('#deleteCustomerName').text(customerName);

    // Show delete modal
    $('#deleteModalOverlay').addClass('active'); // Or use $('#deleteModalOverlay').fadeIn()
});

// 2. CLOSE MODAL HANDLERS
function hideDeleteModal() {
    $('#deleteModalOverlay').removeClass('active'); // Or use $('#deleteModalOverlay').fadeOut()
}

$('#closeDeleteModal, #cancelDeleteBtn').on('click', hideDeleteModal);

$('#deleteModalOverlay').on('click', function(e) {
    if ($(e.target).is('#deleteModalOverlay')) {
        hideDeleteModal();
    }
});

// 3. EXECUTE DELETE AJAX ON CONFIRMATION BUTTON CLICK
$('#confirmDeleteBtn').on('click', function() {
    let customerId = $('#deleteCustomerId').val();
    let $row = $('#customer-row-' + customerId); // Target the dynamic table row

    $.ajax({
        url: '/api/delete-customer/' + customerId,
        type: 'DELETE',
        success: function(response) {
            // Hide modal
            hideDeleteModal();

            // Smoothly fade out and remove row from DOM
            $row.fadeOut(400, function() {
                $(this).remove();
            });
        },
        error: function(xhr) {
            let err = xhr.responseJSON ? xhr.responseJSON.message : "Error deleting user.";
            alert("Delete failed: " + err);
        }
    });
});

// Open Add Modal Function
$('#addopenModal').on('click', function() {
    $('#addmodalOverlay').addClass('active');
});

// Close Add Modal Function
function hideModal() {
    $('#addmodalOverlay').removeClass('active');
    $('#statusMessage').hide().text('');
    $('#addCustomerForm')[0].reset();
}

// Call the hideModal, on button click
$('#closeModal').on('click', hideModal);

// Close on background click
$('#addmodalOverlay').on('click', function(e) {
    if ($(e.target).is('#addmodalOverlay')) {
        hideModal();
    }
});

// AJAX Form Submission to Python
$('#addCustomerForm').on('submit', function(e) {
    e.preventDefault();
    $.ajax({
        url: '/api/add-customer',
        type: 'POST',
        data: $(this).serialize(),
        success: function(response) {
            $('#statusMessage')
                .css('color', '#10b981')
                .text(response.message)
                .fadeIn();

            loadCustomers();

            setTimeout(function() {
                hideModal();
            }, 1500);
        },
        error: function(error) {

            $('#statusMessage')
                .css('color', '#ef4444')
                .text(error.responseJSON.message)
                .fadeIn();
        }
    });
});

// Update functionality
$(document).on('click', '.btn-edit1', function() {

    // 1. Get only the User ID from the button
    let customerId = $(this).data('id');

    // 2. Fetch full user object from Python backend
    $.ajax({
        url: '/api/get-customer/' + customerId,
        type: 'GET',
        success: function (customer) {
            // 3. Fill modal with complete, un-truncated data
            $('#editCustomerId').val(customer.id);
            $('#editName').val(customer.name);
            $('#editAddress').val(customer.address);
            $('#editTin').val(customer.tin);
            $('#editContact').val(customer.contact);

            // 4. Open Modal
            $('#editModalOverlay').addClass('active');
        },
        error: function () {
            alert('Could not fetch user details.');
        }
    });
});

function hideModal_1() {
    $('#editModalOverlay').removeClass('active');
    $('#statusMsg').hide().text('');
}

$('#closeModal_1').on('click', hideModal_1);

$('#editCustomerForm').on('submit', function(e) {
    e.preventDefault();

    $.ajax({
        url: '/api/update-customer',
        type: 'POST',
        data: $(this).serialize(),
        success: function(response) {
            // Show status message
            $('#statusMsg')
                .css('color', '#10b981')
                .text(response.message)
                .fadeIn();

            // 1. Refresh table data
            loadCustomers();

            // 2. Hide modal after delay
            setTimeout(function() {
                hideModal_1();
            }, 1000);
        },
        error: function(xhr) {
            alert('Failed to update customer');
        }
    });
});

// Load All customer
$(document).ready(function() {
    loadCustomers()
});
