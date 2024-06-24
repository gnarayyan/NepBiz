document.addEventListener('DOMContentLoaded', function () {
  const reviewSubmitForm = document.getElementById('reviewSubmitForm');
  const ratingStars = document.querySelectorAll('.rating .star');
  let rating = 0;

  ratingStars.forEach(function (star) {
    star.addEventListener('click', function () {
      unhighlightStars(ratingStars);
      highlightStars([...ratingStars].reverse(), star);

      const catlog = { 5: 1, 4: 2, 3: 3, 2: 4, 1: 5 };
      rating = catlog[star.dataset.value];
    });
  });

  reviewSubmitForm.addEventListener('submit', function (event) {
    event.preventDefault();
    const reviewText = document.getElementById('reviewText').value;
    const productId = document.getElementById('productId').value;

    // console.log('Text: ', reviewText, '  rating: ', rating);
    // API Call
    addReview(rating, reviewText, productId);
    reviewSubmitForm.style.display = 'none';
  });
});

function highlightStars(elems, currentElem) {
  for (let index = 0; index < elems.length; index++) {
    const star = elems[index];

    if (star == currentElem) {
      star.style.color = 'gold';
      return;
    }
    star.style.color = 'gold';
  }
}

function unhighlightStars(elems) {
  for (let index = 0; index < elems.length; index++) {
    const star = elems[index];
    star.style.color = '#d7d3e5';
  }
}

// JavaScript
function addReview(rating, review, productId) {
  fetch('/product/add_review/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      //   'X-CSRFToken': csrftoken, // assuming you have a variable csrftoken with the CSRF token
    },
    body: JSON.stringify({ rating, review, productId }),
  })
    .then((response) => response.json())
    .then((data) => {
      console.log(data.message);
      return true;
    })
    .catch((error) => {
      console.error('Error:', error);
      return false;
    });
}
