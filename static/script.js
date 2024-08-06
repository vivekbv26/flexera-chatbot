// Event listener for the send button
document.getElementById('send-button').addEventListener('click', sendMessage);

// Event listener for the Enter key
document.getElementById('user-input').addEventListener('keypress', function (e) {
  if (e.key === 'Enter') {
    sendMessage();
  }
});

// Function to send the user's message to the backend
function sendMessage() {
  const userInput = document.getElementById('user-input').value;
  if (userInput.trim() !== '') {
    displayMessage(userInput, 'user-message');
    document.getElementById('user-input').value = '';
    getBotResponse(userInput);
  }
}

// Function to display messages in the chat box
function displayMessage(text, className) {
  const messageElement = document.createElement('div');
  messageElement.className = 'message ' + className;
  messageElement.textContent = text;
  document.getElementById('chat-box').appendChild(messageElement);
  document.getElementById('chat-box').scrollTop = document.getElementById('chat-box').scrollHeight;
}

// Function to fetch the bot's response from the backend
function getBotResponse(userInput) {
  fetch('/get-response', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ message: userInput })
  })
  .then(response => {
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    return response.json();
  })
  .then(data => {
    displayMessage(data.response, 'bot-message');
  })
  .catch(error => {
    console.error('There was a problem with the fetch operation:', error);
  });
}
