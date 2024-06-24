// document.getElementById('apply-filter').addEventListener('click', function () {
//   // Fetch filter values
//   var category = document.getElementById('category').value;
//   var brand = document.getElementById('brand').value;
//   var gender = document.getElementById('gender').value;
//   var priceRange = document.getElementById('price-range').value;

//   // Construct URL with filter parameters
//   var url =
//     '/filter/?category=' +
//     category +
//     '&brand=' +
//     brand +
//     '&gender=' +
//     gender +
//     '&price_range=' +
//     priceRange;

//   // Fetch filtered products and update UI
//   fetch(url)
//     .then((response) => response.text())
//     .then((data) => {
//       document.querySelector('.products').innerHTML = data;
//     });
// });
