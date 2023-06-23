document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email(replyData=null) {
  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Reset Messages
  document.querySelector("#messages-view").style.color = "black";
  document.querySelector("#messages-view").style.background = "#ffffff";
  document.querySelector("#messages-view").innerHTML = "";

  if (replyData['sender']) {
    // Set Reply Data
    document.querySelector('#compose-recipients').value = replyData['sender'];
    if(replyData['subject'].match(/^.{3}/) == "Re:") {
      document.querySelector('#compose-subject').value = replyData['subject'];
    }
    else {
      document.querySelector('#compose-subject').value = "Re: " + replyData['subject'];
    }
    let bodyReplyLine = "\nOn "+replyData['timestamp']+" "+replyData['sender']+" wrote: \n"
    document.querySelector('#compose-body').value = bodyReplyLine + replyData['body'];
  }
  else {
    // Clear out composition fields
    document.querySelector('#compose-recipients').value = '';
    document.querySelector('#compose-subject').value = '';
    document.querySelector('#compose-body').value = '';
  }

  document.querySelector("#compose-form").onsubmit = function(event) {
    event.preventDefault()
    
    const recipients = document.querySelector("#compose-recipients").value;
    const subject = document.querySelector("#compose-subject").value;
    const body = document.querySelector("#compose-body").value;

    fetch('/emails', {
      method: 'POST',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ 
        "recipients": recipients,
        "subject": subject, 
        "body": body
      })
    }).then((response) => {
      if (response.status == 201) {
        response.json().then(response => {
          document.querySelector("#messages-view").style.color = "green";
          document.querySelector("#messages-view").style.background = "#e6ffe6";
          document.querySelector("#messages-view").innerHTML = response["message"];
        });
        load_mailbox('sent');
      }
      else {
        response.json().then(response => {
          document.querySelector("#messages-view").style.color = "red";
          document.querySelector("#messages-view").style.background = "#ffe6e6";
          document.querySelector("#messages-view").innerHTML = "ERROR: " + response["error"];

        });
      }
    });
  }
}

function show_email(id, mailbox) {
  // Reset Messages
  document.querySelector("#messages-view").style.color = "black";
  document.querySelector("#messages-view").style.background = "#ffffff";
  document.querySelector("#messages-view").innerHTML = "";

  let emailView = document.querySelector('#email-view');
  fetch("/emails/"+id).then(response => {
    if (response.status == 200){
      response.json().then(data => {
        let sentAt = new Date(data["timestamp"]);
        let emailCard = `<div class="card">
        <div class="card-header">
          <div class="float-left">`+data["sender"]+`</div>
          <div class="float-right">`+sentAt.toLocaleDateString()+` `+sentAt.toLocaleTimeString()+`</div>
        </div>
        <div class="card-body">
          <h5 class="card-title">`+data["subject"]+`</h5>
          <p class="card-text">`+data["body"].replace(/(?:\r\n|\r|\n)/g, '<br>')+`</a>
        </div>
        <div class="card-footer text-muted">
          <button id="replyButton" class="float-left btn btn-sm btn-outline-primary">Reply <i class="bi bi-reply"></i></button>`;
        let archiveButtonHtml = "";
        if (mailbox == 'inbox' && !data["archived"]){
          archiveButtonHtml = `<button id="archiveButton" class="float-right btn btn-sm btn-outline-secondary">Archive <i class="bi bi-archive"></i></button>`;
        }
        if (mailbox == 'archive' && data["archived"]){
          archiveButtonHtml = `<button id="archiveButton" data-archived="1" class="float-right btn btn-sm btn-outline-primary">Unarchive <i class="bi bi-inboxes"></i></button>`;
        }
        emailCard = emailCard + archiveButtonHtml;
        emailCard = emailCard + `</div>
        </div>`;
        emailView.innerHTML = emailCard;

        // Archiving
        let archiveButton = document.querySelector("#archiveButton");
        if(archiveButton){
          archiveButton.addEventListener('click', event => {
            fetch("/emails/"+id, { 
              method: "PUT",
              headers: {
                "Content-Type": "application/json",
              },
              body: JSON.stringify({
                "archived": archiveButton.dataset["archived"] == 1 ? false : true
              })
            }).then(response => {
              if (response.status == 204) {
                // Success, Load the inbox
                load_mailbox('inbox');
              }
              else {
                response.json().then(response => {
                  document.querySelector("#messages-view").style.color = "red";
                  document.querySelector("#messages-view").style.background = "#ffe6e6";
                  document.querySelector("#messages-view").innerHTML = "ERROR: " + response["error"];
                });
              }
            });
          });
        }

        // Replying
      let replyButton = document.querySelector("#replyButton");
      if(replyButton){
        replyButton.addEventListener('click', event => {
          compose_email(data);
        });
      }
      });
  
      // Set to READ
      fetch("/emails/"+id, { 
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          "read": true
        })
      }).then(response => {
        if (response.status != 204) {
          response.json().then(response => {
            document.querySelector("#messages-view").style.color = "red";
            document.querySelector("#messages-view").style.background = "#ffe6e6";
            document.querySelector("#messages-view").innerHTML = "ERROR: " + response["error"];
          });
        }
      });
    }
    else {
      response.json().then(response => {
        document.querySelector("#messages-view").style.color = "red";
        document.querySelector("#messages-view").style.background = "#ffe6e6";
        document.querySelector("#messages-view").innerHTML = "ERROR: " + response["error"];

      });
    } 
  });

  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
}

function load_mailbox(mailbox) {
  // Reset Messages
  document.querySelector("#messages-view").style.color = "black";
  document.querySelector("#messages-view").style.background = "#ffffff";
  document.querySelector("#messages-view").innerHTML = "";

  // Show the mailbox name
  let emailList = document.querySelector('#emails-view');
  emailList.innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  fetch("/emails/"+mailbox).then(response => {
    if (response.status == 200){
      response.json().then(data => {
        data.forEach(element => {
          let sentAt = new Date(element["timestamp"]);
          let emailStatus = element["read"] ? 'read' : 'unread';
          let emailDiv = `<div class="email `+ emailStatus +`" id="`+element["id"]+`">
            <div class="email-head"><div class="from">`+element["sender"]+`</div>
            <div class="sent">`+sentAt.toLocaleDateString()+` `+sentAt.toLocaleTimeString()+`</div></div>
            <div class="subject">`+element["subject"]+`</div>
            </div>`;
          emailList.innerHTML = emailList.innerHTML + emailDiv;
        });        
        const mails = document.querySelectorAll('.email');
        mails.forEach(el => el.addEventListener('click', event => {
            show_email(el.id, mailbox);
        }));
      });
    }
    else {
      response.json().then(response => {
        document.querySelector("#messages-view").style.color = "red";
        document.querySelector("#messages-view").style.background = "#ffe6e6";
        document.querySelector("#messages-view").innerHTML = "ERROR: " + response["error"];

      });
    }
  }).catch(error => {
    console.log("Error ", error);
    document.querySelector("#messages-view").style.color = "red";
    document.querySelector("#messages-view").style.background = "#ffe6e6";
    document.querySelector("#messages-view").innerHTML = "ERROR: " + error;
  });

  // {"error": "Invalid mailbox."}                
  // /emails/<mailbox>
  // <a><div>FROM, SUBJECT, TIMESTAMP, READ=grey/UNREAD=white</div></a>
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#email-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
}