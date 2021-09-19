// Карусель кнопок категорий
const customCategoryList = document.querySelector('.customTextCategoryList'),
   categoryListWrap = document.querySelector('.categoryListWrap').offsetWidth,
   customCategoryItem = customCategoryList.querySelectorAll('.customTextCategoryItem');

let initialPosition = null,
   movingNow = null,
   movingBefore = null,
   scrollWidthList = null;

// Касание пальцем
customCategoryList.addEventListener('touchstart', (e) => {
   initialPosition = e.changedTouches[0].clientX;
   
})

//Движение пальцем по экрану
customCategoryList.addEventListener("touchmove", function (e) {
   movingNow = (movingBefore + initialPosition - e.changedTouches[0].clientX);
   scrollWidthList = customCategoryList.scrollWidth - categoryListWrap
   
   if (movingNow < scrollWidthList && movingNow > 0) {
      customCategoryList.style.left = -(movingNow) + "px";
   }
   if (movingNow <= -5) {
      customCategoryList.style.left = 0 + "px";
      movingNow = 0;
   }
   if (movingNow >= scrollWidthList) {
      customCategoryList.style.left = -(scrollWidthList) + "px";
      movingNow = scrollWidthList;
   }
});

// Отпусая палец
customCategoryList.addEventListener("touchend", function (e) {
   movingBefore = movingNow;
}); 



