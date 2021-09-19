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
   customCategoryList.style.transition = "none";
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
   customCategoryList.style.transition = "all 0.5s ease";
   let speedEnd = initialPosition - e.changedTouches[0].clientX
   console.log("movingNow "+movingNow)
   console.log("speedEnd "+speedEnd)
   if (movingBefore > movingNow) {
      if (movingNow + speedEnd < scrollWidthList && movingNow > 0) {
         customCategoryList.style.left = -(movingNow + speedEnd) + "px";
         movingBefore = movingNow + speedEnd;
      }
      if (movingNow + speedEnd <= 0) {
         customCategoryList.style.left = 0 + "px";
         movingNow = 0;
         movingBefore = movingNow;
      }
   } else {
      if (movingNow + speedEnd < scrollWidthList && movingNow > 0) {
         customCategoryList.style.left = -(movingNow + speedEnd) + "px";
         movingBefore = movingNow + speedEnd;
      }
      if (movingNow + speedEnd >= scrollWidthList) {
         customCategoryList.style.left = -(scrollWidthList) + "px";
         movingNow = scrollWidthList;
         movingBefore = movingNow;
      }
   }
      
   
   
}); 



