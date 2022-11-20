//좋아요 비동기
const likeBtn = document.querySelector('#like-btn')
likeBtn.addEventListener('click', function (event) {
console.log(event.target.dataset)
axios({method: 'get', url: `/reviews/${event.target.dataset.likeId}/like/`}).then(response => {
    console.log(response.data)
    if (response.data.isLike === true) {
    event.target.classList.add('bi-heart-fill')
    event.target.classList.add('article-heart-fill')
    event.target.classList.remove('bi-heart')
    event.target.classList.remove('article-heart')
    // console.log('좋아요')
    } else {
    event.target.classList.add('bi-heart')
    event.target.classList.add('article-heart')
    event.target.classList.remove('bi-heart-fill')
    event.target.classList.remove('article-heart-fill')
    // console.log('좋아요아님')
    }
    const likeCount = document.querySelector('.likes')
    const likeCount2 = document.querySelector('.heart>p')
    likeCount.innerHTML = `<h6 class="likes m-0"> ${response.data.likeCount}</h6>`
    likeCount2.innerHTML = `<h6 class="likes m-0"> ${response.data.likeCount}</h6>`
})
})


// 댓글 좋아요 비동기

const likecomment = (e) => {
  const comment_id = document
    .querySelector(`#${e.id}`)
    .id;
  axios({method: 'get', url: `/reviews/${event.target.dataset.reviewId}/like/${event.target.dataset.commentId}/`}).then(response => {
    console.log(response)
    if (response.data.isLike === true) {
      e.classList.add('bi-heart-fill')
      e.classList.remove('bi-heart')
    // console.log('좋아요')
    } else {
      e.classList.add('bi-heart')
      e.classList.remove('bi-heart-fill')
    // console.log('좋아요아님')
    }
  })
}