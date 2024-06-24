// document.addEventListener('DOMContentLoaded', function () {
//   const showFormBtn = document.getElementById('showFormBtn');
//   const reviewForm = document.getElementById('reviewForm');
//   const reviewSubmitForm = document.getElementById('reviewSubmitForm');
//   const reviewsContainer = document.getElementById('reviews');
//   const ratingStars = document.querySelectorAll('.rating .star');

//   showFormBtn.addEventListener('click', function () {
//     reviewForm.style.display = 'block';
//   });

//   ratingStars.forEach(function (star) {
//     star.addEventListener('click', function () {
//       const ratingValue = this.getAttribute('data-value');
//       document.getElementById('rating').value = ratingValue;
//     });
//   });

//   reviewSubmitForm.addEventListener('submit', function (event) {
//     event.preventDefault();

//     const fullName = document.getElementById('fullName').value;
//     const reviewDate = document.getElementById('reviewDate').value;
//     const reviewText = document.getElementById('reviewText').value;
//     const rating = document.getElementById('rating').value;

//     const reviewHTML = `
//           <div class="review">
//               <h3>${fullName}</h3>
//               <p>Date: ${reviewDate}</p>
//               <p>${reviewText}</p>
//               <p>Rating: ${generateStars(parseInt(rating))}</p>
//           </div>
//       `;

//     reviewsContainer.innerHTML += reviewHTML;
//     reviewForm.reset();
//     reviewForm.style.display = 'none';
//   });

//   function generateStars(rating) {
//     let stars = '';
//     for (let i = 0; i < rating; i++) {
//       stars += '★';
//     }
//     return stars;
//   }
// });
document.addEventListener('DOMContentLoaded', function () {
  const showFormBtn = document.getElementById('showFormBtn');
  const reviewForm = document.getElementById('reviewForm');
  const reviewSubmitForm = document.getElementById('reviewSubmitForm');
  const reviewsContainer = document.getElementById('reviews');
  const ratingStars = document.querySelectorAll('.rating .star');
  let currentRating = 0;

  showFormBtn.addEventListener('click', function () {
    reviewForm.style.display = 'block';
  });

  ratingStars.forEach(function (star) {
    // star.addEventListener('mouseover', function () {
    //   console.log('Mouseover');

    //   const ratingValue = parseInt(this.getAttribute('data-value'));
    //   highlightStars(ratingValue);
    // });

    star.addEventListener('click', function () {
      unhighlightStars(ratingStars);
      highlightStars([...ratingStars].reverse(), star);
      // console.log('Clicked......');
      // star.style.color = 'gold';

      // currentRating = parseInt(this.getAttribute('data-value'));
      // document.getElementById('rating').value = currentRating;
    });

    // star.addEventListener('mouseout', function () {
    //   highlightStars(currentRating);
    //   console.log('Mouse out');
    // });
  });

  reviewSubmitForm.addEventListener('submit', function (event) {
    event.preventDefault();

    const fullName = document.getElementById('fullName').value;
    const reviewDate = document.getElementById('reviewDate').value;
    const reviewText = document.getElementById('reviewText').value;
    const rating = document.getElementById('rating').value;

    const reviewHTML = `
          <div class="review">
              <h3>${fullName}</h3>
              <p>Date: ${reviewDate}</p>
              <p>${reviewText}</p>
              <p>Rating: ${generateStars(parseInt(rating))}</p>
          </div>
      `;

    reviewsContainer.innerHTML += reviewHTML;
    document.getElementById('reviewSubmitForm').reset();
    reviewForm.style.display = 'none';
  });

  function generateStars(rating) {
    let stars = '';
    for (let i = 0; i < rating; i++) {
      stars += '★';
    }
    return stars;
  }

  // function highlightStars(rating) {
  //   ratingStars.forEach(function (star) {
  //     const starValue = parseInt(star.getAttribute('data-value'));
  //     if (starValue <= rating) {
  //       star.classList.add('highlight');
  //     }
  //     // else {
  //     //   star.classList.remove('highlight');
  //     // }
  //   });
  // }
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
