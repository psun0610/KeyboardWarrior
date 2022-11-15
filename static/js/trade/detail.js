new Swiper('#trade-slide', {
  auto_play: true,
  slidesPerView: 1, // 동시에 보여줄 슬라이드 갯수
  spaceBetween: 0, // 슬라이드간 간격
  slidesPerGroup: 1, // 그룹으로 묶을 수, slidesPerView 와 같은 값을 지정하는게 좋음

  // 그룹수가 맞지 않을 경우 빈칸으로 메우기
  // 3개가 나와야 되는데 1개만 있다면 2개는 빈칸으로 채워서 3개를 만듬
  loopFillGroupWithBlank: true,
  navigation: {
    nextEl: '.swiper-button-next',
    prevEl: '.swiper-button-prev'
  },
  loop: true, // 무한 반복
  observer: true,
  observeParents: true,
  pagination: { // 페이징
    el: '.swiper-pagination',
    clickable: true, // 페이징을 클릭하면 해당 영역으로 이동, 필요시 지정해 줘야 기능 작동
  },
  navigation: {
    nextEl: '.swiper-button-next',
    prevEl: '.swiper-button-prev',
  },
});