        //댓글 생성 비동기
        const commentForm = document.querySelector('#comment-form')
        const csrftoken = document
        .querySelector('[name=csrfmiddlewaretoken]')
        .value

        commentForm
        .addEventListener('submit', function (event) {
            event.preventDefault();
            axios({
            method: 'post',
            url: `/reviews/${event.target.dataset.reviewId}/comment_create/`,
            headers: {
                'X-CSRFToken': csrftoken
            },
            data: new FormData(commentForm)
            })
            .then(response => {
                console.log(response)
                const comments = document.querySelector('#comments')
                comments.textContent = "";
                const hr = document.createElement('hr')
                const comment_data = response.data.comment_data

                const user = response.data.user
                for (let i = 0; i < comment_data.length; i++) {
                  const review_pk = response.data.review_pk
                    console.log(comment_data[i].id, user)
                    if (user === comment_data[i].id) {
                      if (comment_data[i].islike) {
                        comments.insertAdjacentHTML('beforeend', `
                          <div class='comment'>
                          <div class="keyboard-comment">
                      {% if request.user.image %}
                      <img class="comment-profile-img" src="{{ request.user.image.url }}">
                      {% else %}
                      <img class="comment-profile-img" src="{% static 'images/logo_png.png' %}">
                      {% endif %}
                            <div class="keyboard-comment-box">
                              <p class="keyboard-comment-user">${comment_data[i].userName}</p>
                              <i class="bi bi-heart" onclick="likecomment(this)" data-review-id="${review_pk}" data-comment-id="${comment_data[i].commentPk}" id="commentlike"></i> <button class="comment-delete-btn" onclick="delete_comment(this)" id="comment-delete-${comment_data[i].commentPk}" data-reviewdel-id="${review_pk}" data-commentdel-id="${comment_data[i].commentPk}">삭제</button>
                          <div> ${comment_data[i].content} </div>
                        `);
                      } else {
                        comments.insertAdjacentHTML('beforeend', `
                          <div class='comment'>
                  
                          <div class="keyboard-comment">
                      {% if request.user.image %}
                      <img class="comment-profile-img" src="{{ request.user.image.url }}">
                      {% else %}
                      <img class="comment-profile-img" src="{% static 'images/logo_png.png' %}">
                      {% endif %}
                            <div class="keyboard-comment-box">
                              <p class="keyboard-comment-user">${comment_data[i].userName}</p>
                              <i class="bi bi-heart-fill" onclick="likecomment(this)" data-review-id="${review_pk}" data-comment-id="${comment_data[i].commentPk}" id="commentlike"></i> <button class="comment-delete-btn" onclick="delete_comment(this)" id="comment-delete-${comment_data[i].commentPk}" data-reviewdel-id="${review_pk}" data-commentdel-id="${comment_data[i].commentPk}">삭제</button>
                          <div> ${comment_data[i].content} </div>
                        `);
                      }
                    } else {
                      if (comment_data[i].islike) {
                        comments.insertAdjacentHTML('beforeend', `
                          <div class='comment'>
                  
                          <div class="keyboard-comment">
                      {% if comment.user.image %}
                      <img class="comment-profile-img" src="{{ comment.user.image.url }}">
                      {% else %}
                      <img class="comment-profile-img" src="{% static 'images/logo_png.png' %}">
                      {% endif %}
                            <div class="keyboard-comment-box">
                              <p class="keyboard-comment-user">${comment_data[i].userName}</p>
                              <i class="bi bi-heart" onclick="likecomment(this)" data-review-id="${review_pk}" data-comment-id="${comment_data[i].commentPk}" id="commentlike"></i>
                          <div> ${comment_data[i].content} </div>
                        `);
                      } else {
                        comments.insertAdjacentHTML('beforeend', `
                          <div class='comment'>
                  
                          <div class="keyboard-comment">
                      {% if comment.user.image %}
                      <img class="comment-profile-img" src="{{ comment.user.image.url }}">
                      {% else %}
                      <img class="comment-profile-img" src="{% static 'images/logo_png.png' %}">
                      {% endif %}
                            <div class="keyboard-comment-box">
                              <p class="keyboard-comment-user">${comment_data[i].userName}</p>
                              <i class="bi bi-heart-fill" onclick="likecomment(this)" data-review-id="${review_pk}" data-comment-id="${comment_data[i].commentPk}" id="commentlike"></i>
                          <div> ${comment_data[i].content} </div>
                        `);
                      }
                    }
                }
                commentForm
                .reset()
            })
            .catch(console.log(1))
            })

        // 댓글 삭제 비동기
        const delete_comment = (e) => {
        const comment_id = document
            .querySelector(`#${e.id}`)
            .id;
        axios({
            method: 'post',
            url: `/reviews/${event.target.dataset.reviewdelId}/comment_delete/${event.target.dataset.commentdelId}/delete/`,
            headers: {
            'X-CSRFToken': csrftoken
            }
        }).then(response => {
            console.log(response)
            const comments = document.querySelector('#comments')
            comments.textContent = "";
            const hr = document.createElement('hr')
            const comment_data = response.data.comment_data
            const user = response.data.user
            for (let i = 0; i < comment_data.length; i++) {
              const review_pk = response.data.review_pk
                console.log(comment_data[i].id, user)
              if (user === comment_data[i].id) {
                if (comment_data[i].islike) {
                  comments.insertAdjacentHTML('beforeend', `
                          <div class='comment'>
                  
                          <div class="keyboard-comment">
                      {% if request.user.image %}
                      <img class="comment-profile-img" src="{{ request.user.image.url }}">
                      {% else %}
                      <img class="comment-profile-img" src="{% static 'images/logo_png.png' %}">
                      {% endif %}
                            <div class="keyboard-comment-box">
                              <p class="keyboard-comment-user">${comment_data[i].userName}</p><i class="bi bi-heart" onclick="likecomment(this)" data-review-id="${review_pk}" data-comment-id="${comment_data[i].commentPk}" id="commentlike"></i>  <button class="comment-delete-btn" onclick="delete_comment(this)" id="comment-delete-${comment_data[i].commentPk}" data-reviewdel-id="${review_pk}" data-commentdel-id="${comment_data[i].commentPk}">삭제</button>
                          <div> ${comment_data[i].content} </div>
                        `);
                } else {
                  comments.insertAdjacentHTML('beforeend', `
                          <div class='comment'>
                  
                          <div class="keyboard-comment">
                      {% if request.user.image %}
                      <img class="comment-profile-img" src="{{ request.user.image.url }}">
                      {% else %}
                      <img class="comment-profile-img" src="{% static 'images/logo_png.png' %}">
                      {% endif %}
                            <div class="keyboard-comment-box">
                              <p class="keyboard-comment-user">${comment_data[i].userName}</p>
                              <i class="bi bi-heart-fill" onclick="likecomment(this)" data-review-id="${review_pk}" data-comment-id="${comment_data[i].commentPk}" id="commentlike"></i>  <button class="comment-delete-btn" onclick="delete_comment(this)" id="comment-delete-${comment_data[i].commentPk}" data-reviewdel-id="${review_pk}" data-commentdel-id="${comment_data[i].commentPk}">삭제</button>
                          <div> ${comment_data[i].content} </div>
                        `);
                }
              } else {
                if (comment_data[i].islike) {
                  comments.insertAdjacentHTML('beforeend', `
                          <div class='comment'>
                  
                          <div class="keyboard-comment">
                      {% if comment.user.image %}
                      <img class="comment-profile-img" src="{{ comment.user.image.url }}">
                      {% else %}
                      <img class="comment-profile-img" src="{% static 'images/logo_png.png' %}">
                      {% endif %}
                            <div class="keyboard-comment-box">
                              <p class="keyboard-comment-user">${comment_data[i].userName}</p>
                              <i class="bi bi-heart" onclick="likecomment(this)" data-review-id="${review_pk}" data-comment-id="${comment_data[i].commentPk}" id="commentlike"></i>
                          <div> ${comment_data[i].content} </div>
                        `);
                } else {
                  comments.insertAdjacentHTML('beforeend', `
                          <div class='comment'>
                  
                          <div class="keyboard-comment">
                      {% if comment.user.image %}
                      <img class="comment-profile-img" src="{{ comment.user.image.url }}">
                      {% else %}
                      <img class="comment-profile-img" src="{% static 'images/logo_png.png' %}">
                      {% endif %}
                            <div class="keyboard-comment-box">
                              <p class="keyboard-comment-user">${comment_data[i].userName}</p>
                              <i class="bi bi-heart-fill" onclick="likecomment(this)" data-review-id="${review_pk}" data-comment-id="${comment_data[i].commentPk}" id="commentlike"></i>
                          <div> ${comment_data[i].content} </div>
                        `);
                }
              }
            }
            }
        )
      }