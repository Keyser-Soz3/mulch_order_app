document.getElementById("quantity").addEventListener("input", updateTotalPrice);
document.getElementById("donation").addEventListener("input", updateTotalPrice);

function updateTotalPrice() {
    const quantity = parseInt(document.getElementById("quantity").value) || 0;
    const donation = parseFloat(document.getElementById("donation").value) || 0;
    const totalPrice = quantity * 6 + donation;
    document.getElementById("total_price").textContent = totalPrice.toFixed(2);
}

const quantityField = document.getElementById("quantity");
const donationField = document.getElementById("donation");
const totalPriceField = document.getElementById("total_price");
const submitButton = document.querySelector("button[type='submit']");

quantityField.addEventListener("input", validateFields);
donationField.addEventListener("input", validateFields);

function validateFields() {
    const quantity = parseInt(quantityField.value) || 0;
    const donation = parseFloat(donationField.value) || 0;
    const totalPrice = quantity * 6 + donation;

    // Highlight fields with negative values
    toggleError(quantityField, quantity < 0);
    toggleError(donationField, donation < 0);

    // Update total price
    totalPriceField.textContent = totalPrice.toFixed(2);

    // Enable or disable the submit button based on total price
    submitButton.disabled = totalPrice <= 0;
}

function toggleError(field, condition) {
    if (condition) {
        field.classList.add("error");
    } else {
        field.classList.remove("error");
    }
}


// this function enables the address autocomplete functionality when users start typing an address
function initAutocomplete() {
    // Create the autocomplete object
    var input = document.querySelector('input[name="address"]');
    var autocomplete = new google.maps.places.Autocomplete(input, { 
      types: ['geocode'],
      componentRestrictions: { country: 'us' }
    });
  
    // Add listener to capture the selected place
    autocomplete.addListener('place_changed', function() {
      var place = autocomplete.getPlace();
      // Optional: Do something with the selected place
      console.log(place);
    });
}

// JavaScript function to validate email format
function validateEmail(input) {
    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/; // Standard email regex
    if (input.value === "" || emailPattern.test(input.value)) {
        input.classList.remove("error");
    } else {
        input.classList.add("error");
    }
}

// JavaScript function to validate and format phone numbers
function formatPhoneNumber(input) {
    // Remove all non-numeric characters
    let digits = input.value.replace(/\D/g, "");

    // Apply formatting if the number has up to 10 digits
    if (digits.length > 0) {
        if (digits.length <= 3) {
            input.value = `(${digits}`;
        } else if (digits.length <= 6) {
            input.value = `(${digits.slice(0, 3)}) ${digits.slice(3)}`;
        } else {
            input.value = `(${digits.slice(0, 3)}) ${digits.slice(3, 6)}-${digits.slice(6, 10)}`;
        }
    }

    // Highlight the field as invalid if the number has fewer than 10 digits
    if (digits.length < 10 && digits.length > 0) {
        input.classList.add("error");
    } else {
        input.classList.remove("error");
    }
}

// Initial validation on page load
validateFields();

google.maps.event.addDomListener(window, 'load', initAutocomplete);
