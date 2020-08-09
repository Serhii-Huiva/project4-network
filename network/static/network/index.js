document.addEventListener('DOMContentLoaded', () => {
    // switch like/unlike button
    if (document.querySelector('.post')) {
        //create like button
        if (document.querySelector('#userName')) {
            var user = document.querySelector('#userName').innerHTML;
            
            document.querySelectorAll('.postLike').forEach( button => {
                const postUser = button.id.slice(4);

                if (postUser == user) {
                    button.style.display = 'none';
                }
            })
        }

        //query users-likes list
        let IDList = [];
        let i = 0;
        document.querySelectorAll(".likeCount").forEach(element => {
            IDList[i] = element.id.slice(4);
            i++;
        });

        fetch(`/getlike`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json;charset=utf-8'
            },
            body: JSON.stringify({"IDlist": IDList})
        })
        .then(response => response.json())
        .then(data => {
            for (const key in data) {
                const usersLikeList = data[key];
                const likeNumPost = document.querySelector(`#like${key}`);
                const likeButton = document.querySelector(`.B${key}`);

                likeNumPost.innerHTML = `Likes: ${usersLikeList.length}`;

                //const user = document.querySelector('#userName').innerHTML;

                for (let i=0; i<usersLikeList.length; i++) {
                    console.log(usersLikeList[i], user);
                    if (usersLikeList[i] == user) {
                        likeButton.innerHTML = 'Unlike';
                        likeButton.setAttribute('onclick', `likePost(${key}, false)`);
                        break;
                    }
                    if (i == usersLikeList.length - 1) {
                        likeButton.innerHTML = 'Like';
                        likeButton.setAttribute('onclick', `likePost(${key}, true)`);
                    }
                }
            };
        })
    }
});

// edit post
function editPost(id) {
    let ID = '#ID' + String(`${id}`);
    let post = document.querySelector(ID);

    let innerHTLM = post.firstElementChild.innerHTML;
    post.innerHTML = "";

    let textarea = document.createElement('textarea');
    textarea.className = "editPostContent";
    textarea.value = innerHTLM;

    let button = document.createElement('button');
    button.className = "savePost";
    button.innerHTML = "Save";
    button.setAttribute('onclick', `savePost(${id})`);

    post.appendChild(textarea);
    post.appendChild(button);
};
