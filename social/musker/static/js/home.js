function submitComment(event, meep_id) {
    event.preventDefault();
  
    // Get the comment form data
    const form = document.getElementById(`comment-form-${meep_id}`);
    const formData = new FormData(form);
  
    // Make a POST request to the Django server-side code
    fetch(`/comment/${meep_id}`, {
      method: 'POST',
      body: formData
    })
    .then(response => response.json())
    .then(data => {
      if (data.success) {
        // Update the page with the new comment
        const commentContainer = document.getElementById(`comment-container-${meep_id}`);
        const comment = data.comment;
        const createdAt = new Date(comment.created_at);
        const formattedDate = createdAt.toLocaleString('en-US', { month: 'long', day: 'numeric', year: 'numeric', hour: 'numeric', minute: 'numeric', hour12: true });
        const commentHTML = `
          <div class="col d-flex justify-content-between">
            <p class="card-text">${comment.body}</p>
            <p class="card-text">${comment.user} <small class="text-body-secondary">@ ${formattedDate.replace(" at", ",").replace("AM", "a.m.").replace("PM", "p.m.")}</small></p>
          </div>
        `;
        commentContainer.insertAdjacentHTML('afterend', commentHTML);
  
        // Clear the comment form
        form.reset();
      } else {
        // Handle form validation errors
        const errors = data.errors;
        // ...
      }
    })
    .catch(error => {
      console.error(error);
    });
  }

  
function submitLike(meep_id){
  fetch(`like/${meep_id}`)
  .then(response => response.json())
  .then(data => {
    if (data) {
      likeButton = document.getElementById(`like-button-${meep_id}`)
      likeCounter = document.getElementById(`like-count-${meep_id}`)

      if (data.like === true) {
        likeButton.classList.remove('btn-primary');
        likeButton.classList.remove('btn-success');
        likeButton.classList.add('btn-danger');
        likeButton.textContent = 'Unlike'
        likeCounter.textContent = parseInt(likeCounter.textContent) + 1;
      } else {
        likeButton.classList.remove('btn-secondary');
        likeButton.classList.remove('btn-danger');
        likeButton.classList.add('btn-success');
        likeButton.textContent = 'Like'
        likeCounter.textContent = parseInt(likeCounter.textContent) - 1;
      }
    } else {
      console.error('Invalid response from server:', data);
    }
  })
  .catch(error => console.error('Error sending like request:', error));
    }
  
const searchInput = document.getElementById('search-input');
const userResults = document.getElementById('user-results');
const autocompleteContainer = document.querySelector('.autocomplete-container')

searchInput.addEventListener('focus', function() {
  autocompleteContainer.classList.remove('d-none');
})

searchInput.addEventListener('blur', function() {
  setTimeout(function() {
    autocompleteContainer.classList.add('d-none');
  }, 100);
});

const debounceTimeout = 500;
let debounceTimer;

function debounce(func) {
  clearTimeout(debounceTimer);
  debounceTimer = setTimeout(func, debounceTimeout);
}

searchInput.addEventListener('input', function() {
  const searchQuery = searchInput.value;
  if (searchQuery.length >= 1) {
    debounce(function() {
      fetch(`search/${searchQuery}`)
      .then(response => response.json())
      .then(data => {
        autocompleteContainer.innerHTML = data.users.map(user => `<li class="dropdown-item"><a href="profile/${user.user_id}">${user.username}</a></li>`).join('');
      })
      .catch(error => console.error(error));
    });
  }
});
