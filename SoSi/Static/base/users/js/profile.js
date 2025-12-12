// ----------------------
// CSRF TOKEN SETUP (Django requirement)
// ----------------------
function getCSRFToken() {
    let cookieValue = null;
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
        const c = cookie.trim();
        if (c.startsWith('csrftoken=')) {
            cookieValue = c.substring('csrftoken='.length, c.length);
        }
    }
    return cookieValue;
}

const csrftoken = getCSRFToken();

// ----------------------
// FOLLOW / UNFOLLOW BUTTON
// ----------------------
document.addEventListener("click", async function (event) {
    if (event.target.classList.contains("follow-btn")) {
        const button = event.target;
        const userId = button.dataset.userId;

        const response = await fetch(`/follow/${userId}/`, {
            method: "POST",
            headers: {
                "X-CSRFToken": csrftoken,
            }
        });

        const data = await response.json();

        if (data.status === "followed") {
            button.textContent = "Unfollow";
            button.classList.add("btn-danger");
            button.classList.remove("btn-primary");
        } else {
            button.textContent = "Follow";
            button.classList.add("btn-primary");
            button.classList.remove("btn-danger");
        }

        document.getElementById("followers-count").textContent = data.followers;
    }
});


// ----------------------
// LIKE / UNLIKE POST
// ----------------------
document.addEventListener("click", async function (event) {
    if (event.target.classList.contains("like-btn")) {
        const button = event.target;
        const postId = button.dataset.postId;

        const response = await fetch(`/like/${postId}/`, {
            method: "POST",
            headers: {
                "X-CSRFToken": csrftoken,
            }
        });

        const data = await response.json();

        document.getElementById(`like-count-${postId}`).textContent = data.likes;

        if (data.liked) {
            button.textContent = "Unlike";
            button.classList.remove("btn-outline-primary");
            button.classList.add("btn-primary");
        } else {
            button.textContent = "Like";
            button.classList.remove("btn-primary");
            button.classList.add("btn-outline-primary");
        }
    }
});


// ----------------------
// EDIT PROFILE (AJAX)
// ----------------------
document.getElementById("editProfileForm")?.addEventListener("submit", async function (event) {
    event.preventDefault();

    const formData = new FormData(this);

    const response = await fetch("/update-profile/", {
        method: "POST",
        headers: {
            "X-CSRFToken": csrftoken,
        },
        body: formData
    });

    const data = await response.json();

    if (data.status === "success") {
        alert("Profile updated successfully!");
        location.reload();
    } else {
        alert("Error updating profile.");
    }
});


// ----------------------
// PROFILE PICTURE LIVE PREVIEW
// ----------------------
document.getElementById("profilePicInput")?.addEventListener("change", function () {
    const file = this.files[0];
    if (file) {
        const preview = document.getElementById("profilePicPreview");
        preview.src = URL.createObjectURL(file);
    }
});


// ----------------------
// INFINITE SCROLL FOR POSTS
// ----------------------
let page = 1;
let loading = false;

window.addEventListener("scroll", async function () {
    if (window.innerHeight + window.scrollY >= document.body.offsetHeight - 100 && !loading) {
        loading = true;
        page += 1;

        const response = await fetch(`/profile-posts?page=${page}`);
        const data = await response.text();

        document.getElementById("postsContainer").insertAdjacentHTML("beforeend", data);
        loading = false;
    }
});

