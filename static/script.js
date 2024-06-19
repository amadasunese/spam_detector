document.getElementById('classifyButton').addEventListener('click', function() {
    var emailText = document.getElementById('emailText').value;
    fetch('https://spamdetector.pythonanywhere.com/predict', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: 'text=' + encodeURIComponent(emailText)
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('result').innerText = data.spam ? 'This email is likely Spam.' : 'This email is likely Not Spam';
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('result').innerText = 'Error occurred!';
    });
});
