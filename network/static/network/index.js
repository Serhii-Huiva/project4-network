document.addEventListener('DOMContentLoaded', () => {
    // Create edit button
    let post = document.querySelector('.post');
    if (post != undefined) {
        document.querySelectorAll('#usrN').forEach( name => {
            const userName = document.querySelector('#userName').innerHTML;
            const postUserName = name.innerHTML;
    
            if (userName == postUserName) {
                const editButton = document.createElement('button');
                editButton.className = "editButton";
                editButton.innerText = "Edit post";
                editButton.onclick = "editPost()"
    
                name.parentElement.appendChild(editButton);
            }
        })
    }
})