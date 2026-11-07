(() => {
  'use strict';

  const form = document.getElementById('ask-form');
  const input = document.getElementById('question-input');
  const list = document.getElementById('question-list');
  const pane = document.getElementById('questions');

  const POSTED_ICON = 'Hand_Raised_Inverted.jpg';

  /**
   * Hook for the back-end team: send the question to the server here.
   * Return a promise; if it rejects, the question is not added to the list.
   * For now it resolves immediately so the front end can be tested on its own.
   */
  async function sendQuestionToServer(text) {
    // e.g. await fetch('/api/questions', { method: 'POST', body: JSON.stringify({ text }) });
    return { text };
  }

  /** Build a posted-question list item (text is inserted as text, never as HTML). */
  function createPostedQuestion(text) {
    const li = document.createElement('li');
    li.className = 'question posted';

    const bubble = document.createElement('p');
    bubble.className = 'bubble';
    bubble.textContent = text;

    const icon = document.createElement('span');
    icon.className = 'q-icon';

    const img = document.createElement('img');
    img.src = POSTED_ICON;
    img.alt = 'Question you posted';

    icon.appendChild(img);
    li.append(bubble, icon);
    return li;
  }

  function scrollQuestionsToBottom() {
    pane.scrollTop = pane.scrollHeight;
  }

  /* Auto-grow fallback for browsers without CSS field-sizing */
  const supportsFieldSizing = window.CSS && CSS.supports && CSS.supports('field-sizing', 'content');

  function resizeInput() {
    if (supportsFieldSizing) return;
    input.style.height = 'auto';
    input.style.height = input.scrollHeight + 4 + 'px'; // +4 for the 2px borders
  }

  async function submitQuestion() {
    const text = input.value.trim();
    if (!text) return; // ignore empty questions

    input.disabled = true;
    try {
      await sendQuestionToServer(text);
      list.appendChild(createPostedQuestion(text));
      input.value = '';
      resizeInput();
    } catch (err) {
      console.error('Could not post question:', err);
    } finally {
      input.disabled = false;
      input.focus();
      scrollQuestionsToBottom();
    }
  }

  form.addEventListener('submit', (event) => {
    event.preventDefault();
    submitQuestion();
  });

  // Enter submits; Shift+Enter inserts a new line.
  input.addEventListener('keydown', (event) => {
    if (event.key === 'Enter' && !event.shiftKey && !event.isComposing) {
      event.preventDefault();
      submitQuestion();
    }
  });

  input.addEventListener('input', resizeInput);

  // Start scrolled to the newest question.
  scrollQuestionsToBottom();
})();
