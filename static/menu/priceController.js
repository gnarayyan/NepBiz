//Global Variables
var selectedGenders = [];
var selectedBrands = [];

// Price Filter
let minPrice = document.getElementById('minField');
let maxPrice = document.getElementById('maxField');

document
  .getElementById('priceRangeSelector')
  .addEventListener('click', function () {
    getDataFromServer();
  });

// Category Filter
let selectProductCategory = document.getElementById('categorySelect');

selectProductCategory.addEventListener('change', function () {
  // Get the selected category
  let selectedCategory = this.value;

  // Call the API
  getDataFromServer();
});

// Filter Brands
// Get all the checkboxes
var brandCheckboxes = document.querySelectorAll('input[name="brand"]');

// Function to get selected brands
function getSelectedBrands() {
  selectedBrands = [];
  for (var i = 0; i < brandCheckboxes.length; i++) {
    if (brandCheckboxes[i].checked) {
      // If the checkbox is checked, get the corresponding label text
      //   var label = document.querySelector(
      //     'label[for="' + brandCheckboxes[i].id + '"]'
      //   ).textContent; //textContent
      let label = brandCheckboxes[i].value;
      selectedBrands.push(parseInt(label));
    }
  }
  //   console.log(selectedBrands);
  getDataFromServer();
  //TODO: API call
}

// Add an event listener to each brandcheckbox
for (var i = 0; i < brandCheckboxes.length; i++) {
  brandCheckboxes[i].addEventListener('change', getSelectedBrands);
}

// Filter Gender
var genderCheckboxes = document.querySelectorAll('input[name="gender"]');

// Function to get selected brands
function getSelectedGenders() {
  selectedGenders = [];
  for (var i = 0; i < genderCheckboxes.length; i++) {
    if (genderCheckboxes[i].checked) {
      // If the checkbox is checked, get the corresponding label text
      //   var label = document.querySelector(
      //     'label[for="' + genderCheckboxes[i].id + '"]'
      //   ).textContent;
      // If the checkbox is checked, get its value
      let label = genderCheckboxes[i].value;
      selectedGenders.push(parseInt(label));
    }
  }
  //   console.log(selectedGenders);
  getDataFromServer();
  //TODO: API call
}

// Add an event listener to each checkbox
for (var i = 0; i < genderCheckboxes.length; i++) {
  genderCheckboxes[i].addEventListener('change', getSelectedGenders);
}

// //
function getDataFromServer() {
  // Get CSRF token
  // var csrfToken = document.cookie
  //   .split('; ')
  //   .find((row) => row.startsWith('csrftoken'))
  //   .split('=')[1];

  // Construct URL with filter parameters
  var url = '/products/filter/';
  let data = {
    min_price: minPrice.value || 0,
    max_price: maxPrice.value || 99999999,
    category: parseInt(selectProductCategory.value) || -1,
    brands: selectedBrands || [],
    genders: selectedGenders || [],
    // page: currentPageNumber + 1,
  };

  // console.log('Data: ', data);
  // let response;

  fetch(url, {
    method: 'POST',
    headers: {
      // 'X-CSRFToken': csrfToken,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  })
    .then((response) => {
      // response = response;
      return response.json();
    })
    .then((data) => {
      // console.log('received: ', data);
      updateUI(JSON.parse(data));
      removePaginationButtons();
      // updatePagination(currentPageNumber, response);
    })
    .catch((error) => {
      console.error('Error:', error);
    });
}

function updateUI(array) {
  // Get the product grid element
  var productGrid = document.querySelector('.product-grid');

  //Remove all products there
  productGrid.innerHTML = '';

  if (array.length == 0) {
    productGrid.innerHTML =
      '<p id="fallback-text"> No Product for Your Choice </p>';
  }

  // Loop through the data
  for (let index = 0; index < array.length; index++) {
    const product = array[index];

    // console.log('Product: ', product);

    // Create a new product element
    var productElement = document.createElement('div');
    productElement.className = 'product';

    // Calculate the discounted price
    var discountedPrice =
      product.fields.price -
      (product.fields.price * product.fields.discount) / 100;

    // Generate the HTML for the product
    productElement.innerHTML =
      `
        <a href="/product/${product.pk}"><img src="/media/${product.fields.image}" alt="${product.fields.name}" /></a>
        <h3>${product.fields.name}</h3>` +
      (product.fields.discount > 0
        ? `<div class="price-section">
            <div class="price">
                <p class="original-price">Rs ${parseFloat(
                  product.fields.price
                ).toFixed(2)}</p>
                <p class="discounted-price">Rs ${discountedPrice.toFixed(2)}</p>
            </div>
            <p class="discount-percent">${parseFloat(
              product.fields.discount
            ).toFixed(0)}% OFF</p>
        </div>`
        : `<div class="price-section">

        <div class="price">
          <p>Rs ${product.fields.price.toLocaleString('en', {
            useGrouping: true,
          })}</p>
          <p class="hidden">Hidden</p>
        </div>
      </div>`) +
      `<button class="btn">Add to Cart</button>
    `;

    // Add the product element to the product grid
    productGrid.appendChild(productElement);
  }
}

function removePaginationButtons() {
  document.getElementById('pagination').innerHTML = '';
}

function updatePagination(pageNumber, response) {
  var currentPageNumber = Number(
    document.querySelector('.pagination .current').textContent
  );
  // Update the pagination controls
  var previousLink = document.querySelector('.pagination .previous');
  var nextLink = document.querySelector('.pagination .next');
  var currentPageNumber = document.querySelector('.pagination .current');

  if (response.has_previous) {
    previousLink.href = '?page=' + (pageNumber - 1);
    previousLink.style.display = '';
  } else {
    previousLink.style.display = 'none';
  }

  if (response.has_next) {
    nextLink.href = '?page=' + (pageNumber + 1);
    nextLink.style.display = '';
  } else {
    nextLink.style.display = 'none';
  }

  currentPageNumber.textContent = pageNumber;
}
