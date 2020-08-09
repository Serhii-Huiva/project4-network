// follow/unfollow user 
function follow(fol, id) {
    const userName = document.querySelector('#userName').innerHTML;
    const followUser = document.querySelector('#usern').innerHTML;

    fetch(`${id}/follow`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json;charset=utf-8'
        },
        body: JSON.stringify({'follow': fol, 'userName': userName, 'followUser': followUser})
    })
    .then(response => response.json())
    .then(data => {
        if (data.status) {
            location.reload();
        };
    });
};

// save post before edit
function savePost(id) {
    let ID = '#ID' + String(`${id}`);
    let post = document.querySelector(ID);
    let content = post.firstElementChild.value;

    fetch(`${id}/changepost`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json;charset=utf-8'
        },
        body: JSON.stringify({'content': content})
    })
    .then(response => response.json())
    .then(data => {
        if (data.status) {
            post.innerHTML = "";

            let h5 = document.createElement('h5');
            h5.id = "postMessage";
            h5.innerHTML = content;

            post.appendChild(h5);
        }
    });
};

//like/Unlike post
function likePost(id, like) {
    const user = document.querySelector('#userName').innerHTML;

    fetch(`${id}/likepost`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json;charset=utf-8'
        },
        body: JSON.stringify({'like': like, 'user': user})
    })
    .then(response => response.json())
    .then(data => {
        if (data.status) {
            let button = document.querySelector(`.B${id}`);
            let likeCount = document.querySelector(`#like${id}`);
            let count = Number(likeCount.innerHTML.slice(7));

            if (button.innerHTML == 'Like') {
                button.innerHTML = "Unlike";
                button.setAttribute('onclick', `likePost(${id}, false)`);
                likeCount.innerHTML = `Likes: ${count + 1}`;
            }
            else {
                button.innerHTML = "Like";
                button.setAttribute('onclick', `likePost(${id}, true)`);
                likeCount.innerHTML = `Likes: ${count - 1}`;
            }
        }
    })
};