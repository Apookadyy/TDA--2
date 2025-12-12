 
// Like button toggle logic

function toggleLike(postId) {
    let icon = document.getElementById(`like-icon-${postId}`);

    if (icon.classList.contains("liked")) {
        icon.classList.remove("liked");
        icon.src = "/static/posts/img/post-icons/like-outline.png";
    } else {
        icon.classList.add("liked");
        icon.src = "/static/posts/img/post-icons/like-filled.png";
    }

    console.log("Like toggled for Post:", postId);
}
