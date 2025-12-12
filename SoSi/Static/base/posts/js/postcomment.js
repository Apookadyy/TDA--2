 
function submitComment(postId) {
    let comment = document.getElementById(`comment-input-${postId}`).value;

    if(comment.trim() === "") return;

    console.log("Comment submitted:", comment);
}
