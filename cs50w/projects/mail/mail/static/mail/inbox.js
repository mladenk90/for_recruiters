document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // Create event listener for composing mail
  document.querySelector('#compose-form').addEventListener('submit', send_email)

  // By default, load the inbox
  load_mailbox('inbox');
});



function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#emails-detail-view').style.display = 'none';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function send_email(event) {
  event.preventDefault();

  // Store data from specific fields
  const recipient = document.querySelector('#compose-recipients').value;
  const subject = document.querySelector('#compose-subject').value;
  const body = document.querySelector('#compose-body').value;

  // fetch data from backend
  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
      recipients: recipient,
      subject: subject,
      body: body
    })
  })
  .then(response => response.json())
  .then(result => {
    // Print result
    console.log(result);
    load_mailbox('sent');
  }); 
   
}

function view_email(id){
  fetch(`/emails/${id}`)
  .then(response => response.json())
  .then(email => {
    console.log(email);

    // Show email view and hide other views
    document.querySelector('#emails-view').style.display = 'none';
    document.querySelector('#compose-view').style.display = 'none';
    document.querySelector('#emails-detail-view').style.display = 'block';
    // query for list view to show all email details(emphasized): sender.recipient,subject,time, and body of message
    document.querySelector('#emails-detail-view').innerHTML = `
      <ul class="list-group">
        <li class="list-group-item"><strong>From:</strong>${email.sender}</li>
        <li class="list-group-item"><strong>To:</strong>${email.recipients}</li>
        <li class="list-group-item"><strong>Subject:</strong>${email.subject}</li>
        <li class="list-group-item"><strong>Time:</strong>${email.timestamp}</li>
        <li class="list-group-item">${email.body}</li>
      </ul>
      `
      // change email to read once viewed
      if(!email.read){
        fetch(`/emails/${email.id}`, {
          method: 'PUT',
          body: JSON.stringify({
            read: true
          })
        })
      }

      //archive/unarchive button
      const btn_archive = document.createElement('button');
      btn_archive.innerHTML = email.archived ? "Unarchive" : "Archive";
      btn_archive.className = email.archived ? "btn btn-success" : "btn btn-warning";
      btn_archive.addEventListener('click', function() {
        fetch(`/emails/${email.id}`, {
          method: 'PUT', 
          body: JSON.stringify({
              archived: !email.archived
          })
        })
        .then(() => { load_mailbox('archive')})
      });
      document.querySelector('#emails-detail-view').append(btn_archive);

      // reply button
      const btn_reply = document.createElement('button');
      btn_reply.innerHTML = "Reply"
      btn_reply.className = "btn btn-primary";
      btn_reply.addEventListener('click', function() {
        compose_email();

        document.querySelector('#compose-recipients').value = email.sender;
        let subject = email.subject;
        if(subject.split('',1)[0] != "RE:"){
          subject = "RE:" + email.subject;
        }
        document.querySelector('#compose-subject').value = subject;
        document.querySelector('#compose-body').value = `${email.timestamp} ${email.sender} sent ${email.body}`;
      });
      document.querySelector('#emails-detail-view').append(btn_reply);
  });
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#emails-detail-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  // fetch emails for specific user/inbox
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
    // foreach loop for each email
    emails.forEach(singleEmail => {

      console.log(singleEmail);

      // div for each email
      const newEmail = document.createElement('div');
      newEmail.className = 'email-group-item';
      // query to retrieve corresponding data
      newEmail.innerHTML = `
        <h5>Sender: ${singleEmail.sender}</h5>
        <h4>Subject: ${singleEmail.subject}</h4>
        <p>${singleEmail.timestamp}</p>
      `;
      // change color from white to grey
      newEmail.className = singleEmail.read ? "read": "unread";
      // add event listener for click
      newEmail.addEventListener('click', function() {
        view_email(singleEmail.id)
      });      
      document.querySelector('#emails-view').append(newEmail);
    })
  });
  }



