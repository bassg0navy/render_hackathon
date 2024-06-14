document.getElementById('send-btn').addEventListener('click', sendMessage);
document.getElementById('user-input').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') sendMessage();
});

function sendMessage() {
    const userInput = document.getElementById('user-input').value;
    if (!userInput) return;

    addMessageToChat('User', userInput);
    document.getElementById('user-input').value = '';

    // Simulate chatbot response
    setTimeout(() => {
        const botResponse = getBotResponse(userInput);
        addMessageToChat('Bot', botResponse);
    }, 1000);
}

function addMessageToChat(sender, message) {
    const chatBox = document.getElementById('chat-box');
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message');
    messageDiv.innerHTML = `<strong>${sender}:</strong> ${message}`;
    chatBox.appendChild(messageDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
}

function getBotResponse(userInput) {
    // This is a placeholder function. Replace with actual chatbot logic.
    return `You said: ${userInput}`;
}
