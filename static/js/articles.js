// main.html
// 스크롤하면 나타나는 애니메이션
const saDefaultMargin = 300;
let saTriggerMargin = 0;
let saTriggerHeight = 0;
const saElementList = document.querySelectorAll('.sa');

const saFunc = function () {
  for (const element of saElementList) {
    if (!element.classList.contains('show')) {
      if (element.dataset.saMargin) {
        saTriggerMargin = parseInt(element.dataset.saMargin);
      } else {
        saTriggerMargin = saDefaultMargin;
      }

      if (element.dataset.saTrigger) {
        saTriggerHeight = document
          .querySelector(element.dataset.saTrigger)
          .getBoundingClientRect()
          .top + saTriggerMargin;
      } else {
        saTriggerHeight = element
          .getBoundingClientRect()
          .top + saTriggerMargin;
      }

      if (window.innerHeight > saTriggerHeight) {
        let delay = (element.dataset.saDelay)
          ? element.dataset.saDelay
          : 0;
        setTimeout(function () {
          element
            .classList
            .add('show');
        }, delay);
      }
    }
  }
}

window.addEventListener('load', saFunc);
window.addEventListener('scroll', saFunc);


// all.html
let nav_flag = 0
document.querySelector('#all-nav-button').addEventListener("click",  function() {
  if(!nav_flag){
    const nav_close = document.querySelector('.all-nav-close')
    nav_close.className = 'all-nav-open'
    const nav_table = document.querySelector('#nav-table')
    nav_table.style.display = 'block'
    nav_flag = 1
  }
  else {
    const nav_close = document.querySelector('.all-nav-open')
    nav_close.className = 'all-nav-close'
    const nav_table = document.querySelector('#nav-table')
    nav_table.style.display = 'none'
    nav_flag = 0
  }
})

const ad_card = document.querySelectorAll('.ad-card')

ad_card.forEach((card, index) => {
  card.addEventListener('mouseover', function() {
    this.querySelector('.ad-card-context').className = 'ad-card-context-hover'
  })
  card.addEventListener('mouseout', function() {
    this.querySelector('.ad-card-context-hover').className = 'ad-card-context'
  })
})