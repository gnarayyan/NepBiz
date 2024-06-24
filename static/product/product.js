function changeImage(imageSrc) {
  var productImage = document.getElementById('product-image');
  var thumbnailImages = document.querySelectorAll('.thumbnail-images img');

  thumbnailImages.forEach(function (img) {
    img.classList.remove('active');
  });

  productImage.src = imageSrc;
  productImage.classList.add('zoomIn');

  setTimeout(function () {
    productImage.classList.remove('zoomIn');
  }, 300);
}
