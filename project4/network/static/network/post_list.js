function getCookie(cname) {
    // Fetching Cookie values
    let name = cname + "=";
    let decodedCookie = decodeURIComponent(document.cookie);
    let ca = decodedCookie.split(';');
    for(let i = 0; i <ca.length; i++) {
      let c = ca[i];
      while (c.charAt(0) == ' ') {
        c = c.substring(1);
      }
      if (c.indexOf(name) == 0) {
        return c.substring(name.length, c.length);
      }
    }
    return "";
  }

document.addEventListener('DOMContentLoaded', function() {
    let postList = document.querySelector("#postList");
    // only for views with post list
    if (postList) {
        // edit/cancel button
        let editPostButtons = document.querySelectorAll(".edit-post");
        editPostButtons.forEach(el => el.addEventListener('click', event => {
            // display change
            el.style.display = 'none';
            document.querySelector("#post-"+el.dataset["postId"]+"-body").style.display = 'none';
            document.querySelector("#post-"+el.dataset["postId"]+"-form").style.display = 'block';
            document.querySelector("#post-"+el.dataset["postId"]+"-cancel-edit-button").style.display = 'block';
        }));
        let cancelEditPostButtons = document.querySelectorAll(".cancel-edit-post");
        cancelEditPostButtons.forEach(el => el.addEventListener('click', event => {
            // display change
            el.style.display = 'none';
            document.querySelector("#post-"+el.dataset["postId"]+"-body").style.display = 'block';
            document.querySelector("#post-"+el.dataset["postId"]+"-form").style.display = 'none';
            document.querySelector("#post-"+el.dataset["postId"]+"-edit-button").style.display = 'block';
        }));
        
        // send edits
        let sendPostEditButtons = document.querySelectorAll(".send-edit-post");
        sendPostEditButtons.forEach(el => el.addEventListener('click', event => {
            event.preventDefault();
            let postBody = document.querySelector("#post-"+el.dataset["postId"]+"-textarea").value
            fetch('/posts/'+el.dataset["postId"], {
                method: 'PUT',
                headers: {
                  'Accept': 'application/json',
                  'Content-Type': 'application/json',
                  'X-CSRFToken': getCookie("csrftoken") // to avoid disabling csrf in View
                },
                body: JSON.stringify({ 
                  "postBody": postBody,
                })
              }).then((response) => {
                if (response.status == 200) {
                    response.json().then(response => { 
                        document.querySelector("#post-"+el.dataset["postId"]+"-body").innerHTML = response["body"];
                    });
                } else {
                  response.json().then(response => {
                    document.querySelector("#messages-view").style.color = "red";
                    document.querySelector("#messages-view").style.background = "#ffe6e6";
                    document.querySelector("#messages-view").innerHTML = "ERROR: " + response["error"];
                  });
                }
              });
            // display change
            document.querySelector("#post-"+el.dataset["postId"]+"-form").style.display = 'none';
            document.querySelector("#post-"+el.dataset["postId"]+"-body").style.display = 'block';
            document.querySelector("#post-"+el.dataset["postId"]+"-edit-button").style.display = 'block';
            document.querySelector("#post-"+el.dataset["postId"]+"-cancel-edit-button").style.display = 'none';
        }));

        // like/unlike
        let likeButtons = document.querySelectorAll(".like-toggle-button");
        likeButtons.forEach(el => el.addEventListener('click', event => {
            //alert(el.dataset["postId"]);
            fetch('/posts/'+el.dataset["postId"]+'/likes', {
                method: 'POST',
                headers: {
                  'Accept': 'application/json',
                  'Content-Type': 'application/json',
                  'X-CSRFToken': getCookie("csrftoken")
                },
            }).then((response) => {
                if (response.status == 200) {
                    response.json().then(response => { 
                        if(response["like"]["active"]){
                            el.innerHTML = '<i class="bi bi-heart-fill"></i>'
                        } else {
                            el.innerHTML = '<i class="bi bi-heart"></i>'
                        }
                        document.querySelector("#post-"+el.dataset["postId"]+"-like-count").innerHTML = response["post_like_count"];
                    });
                } else {
                  response.json().then(response => {
                    document.querySelector("#messages-view").style.color = "red";
                    document.querySelector("#messages-view").style.background = "#ffe6e6";
                    document.querySelector("#messages-view").innerHTML = "ERROR: " + response["error"];
                  });
                }
            });;
        }));
    }
});