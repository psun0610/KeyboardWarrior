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