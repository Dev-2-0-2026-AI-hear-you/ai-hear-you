
(() => {
  'use strict';
 
  const pane = document.getElementById('questions');
  const list = document.getElementById('question-list');
  const testBar = document.getElementById('test-bar');
 
  const ICON_PENDING = 'Hand_Raised.jpg';
  const ICON_ANSWERED = 'Hand_Raised_Inverted.jpg';
 
  /* ---------- Helpers ---------- */
 
  // "2:08" style (12-hour, no AM/PM, to match the mockup)
  function formatTime(date) {
    const h = date.getHours() % 12 || 12;
    const m = String(date.getMinutes()).padStart(2, '0');
    return `${h}:${m}`;
  }
 
  function scrollToBottom() {
    pane.scrollTop = pane.scrollHeight;
  }
 
  /* ---------- Question item ---------- */
 
  /**
   * Adds a question to the list (text visible, unanswered by default).
   * The back-end team can call this (window.addQuestion) for each incoming question.
   */
  function addQuestion(text, date = new Date()) {
    const li = document.createElement('li');
    li.className = 'p-question';
 
    const time = document.createElement('time');
    time.className = 'p-time';
    time.dateTime = date.toISOString();
    time.textContent = formatTime(date);
 
    const iconBtn = document.createElement('button');
    iconBtn.type = 'button';
    iconBtn.className = 'q-icon';
    const img = document.createElement('img');
    iconBtn.appendChild(img);
 
    const bubble = document.createElement('div');
    bubble.className = 'p-bubble';
 
    li.append(time, iconBtn, bubble);
 
    bubble.textContent = text; // text is never parsed as HTML
    img.alt = '';
 
    function render(answered) {
      li.classList.toggle('answered', answered);
      img.src = answered ? ICON_ANSWERED : ICON_PENDING;
      iconBtn.setAttribute('aria-label', answered ? 'Question answered' : 'Mark question as answered');
      iconBtn.disabled = answered; // one-way: once answered, it stays answered
    }
 
    // Clicking the icon marks the question as answered. This cannot be undone.
    iconBtn.addEventListener('click', () => {
      if (!li.classList.contains('answered')) render(true);
    });
 
    render(false);
    list.appendChild(li);
    scrollToBottom();
    return li;
  }
 
  window.addQuestion = addQuestion;
 
  /* ---------- TEST ONLY: top bar adds a predetermined question ---------- */
 
  var testQuestion = 'Hi, this is the question I asked. Click the hand icon to mark it as answered: the icon inverts and this text greys out. I LOOOOOVE asking questions';
 
  function addTestQuestion() {
    addQuestion(testQuestion);
  }
 
  testBar.addEventListener('click', addTestQuestion);
  testBar.addEventListener('keydown', (event) => {
    if (event.key === 'Enter' || event.key === ' ') {
      event.preventDefault();
      addTestQuestion();
    }
  });
})();
 