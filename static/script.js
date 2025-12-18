/*  GET HTML ELEMENTS */

const chatBox = document.getElementById('chatBox');
const chatForm = document.getElementById('chatForm');
const questionInput = document.getElementById('questionInput');
const sendBtn = document.getElementById('btn');
const typingIndicator = document.getElementById('typingIndicator');

/* TYPING ANIMATION FUNCTION  */

/**
 * Creates ChatGPT-style typing effect
 * @param {HTMLElement} element - Where to display text
 * @param {string} text - The text to type out
 * @param {number} speed - Milliseconds per character
 * @returns {Promise} - Resolves when typing completes
 */
function typeWriter(element, text, speed = 15) {
    let i = 0;
    element.innerHTML = ''; // Clear existing text
    
    return new Promise((resolve) => {
        function type() {
            if (i < text.length) {
                // Add next character
                element.innerHTML += text.charAt(i);
                i++;
                
                // Auto-scroll if needed
                chatBox.scrollTop = chatBox.scrollHeight;
                
                // Continue typing
                setTimeout(type, speed);
            } else {
                // Typing complete
                resolve();
            }
        }
        type();
    });
}

/*  HANDLE FORM SUBMISSION */

chatForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const question = questionInput.value.trim();
    if (!question) return;

    /*  STEP 1: CLEAR CHATBOX & SHOW QUESTION */
    
     chatBox.innerHTML = '';
    
    const questionDiv = document.createElement('div');
    questionDiv.className = 'answer-text';
    questionDiv.style.color = '#667eea';
    questionDiv.style.marginBottom = '20px';
    questionDiv.innerHTML = `<strong>Q:</strong> ${question}`;
    chatBox.appendChild(questionDiv);

    /* STEP 2: PREPARE UI  */

    questionInput.value = '';
    sendBtn.disabled = true;
    sendBtn.textContent = 'Thinking...';
    typingIndicator.style.display = 'block';

    /* 
       STEP 3: SEND REQUEST TO BACKEND
       */
    
    try {
        const response = await fetch('/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: `question=${encodeURIComponent(question)}`
        });

        // Parse JSON response
        const data = await response.json();
        
        // Get the answer
        const answer = data.answer || 'Sorry, I could not get a response.';

        /*
           STEP 4: SHOW ANSWER WITH TYPING
           */
        
        typingIndicator.style.display = 'none';

        const answerDiv = document.createElement('div');
        answerDiv.className = 'answer-text';
        chatBox.appendChild(answerDiv);

        // Type out the answer
        await typeWriter(answerDiv, answer, 15);

    } catch (error) {
        /* 
           STEP 5: HANDLE ERRORS
          */
        
        console.error('Error:', error);
        typingIndicator.style.display = 'none';
        
        const errorDiv = document.createElement('div');
        errorDiv.className = 'answer-text';
        errorDiv.style.color = '#ff6b6b';
        errorDiv.textContent = '❌ Error: Could not connect to server.';
        chatBox.appendChild(errorDiv);
    }

    /* 
       STEP 6: RE-ENABLE BUTTON
       */
    
    sendBtn.disabled = false;
    sendBtn.textContent = 'Ask';
    chatBox.scrollTop = chatBox.scrollHeight;
});

// Auto-focus input
questionInput.focus();

// Keyboard shortcut
document.addEventListener('keydown', (e) => {
    if (e.ctrlKey && e.key === 'k') {
        e.preventDefault();
        questionInput.focus();
    }
});