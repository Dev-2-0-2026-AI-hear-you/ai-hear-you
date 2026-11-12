(() => {
  'use strict';

  const pane = document.getElementById('questions');
  const list = document.getElementById('question-list');
  //const testBar = document.getElementById('test-bar');

  const ICON_CLOSED = '/static/Hand_Raised.jpg';
  const ICON_OPEN = '/static/Hand_Raised_Inverted.jpg';
  const PLACEHOLDER = 'A student has a question';

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
   * Adds a question to the list (collapsed by default).
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

    function setOpen(open) {
      li.classList.toggle('open', open);
      img.src = open ? ICON_OPEN : ICON_CLOSED;
      img.alt = '';
      iconBtn.setAttribute('aria-expanded', String(open));
      iconBtn.setAttribute('aria-label', open ? 'Close question' : 'Open question');
      bubble.textContent = open ? text : PLACEHOLDER; // text is never parsed as HTML

      // Only the collapsed bubble acts like a button (it can open, never close)
      if (open) {
        bubble.removeAttribute('role');
        bubble.removeAttribute('tabindex');
      } else {
        bubble.setAttribute('role', 'button');
        bubble.setAttribute('tabindex', '0');
      }
    }

    // The icon toggles: the ONLY way to close a question.
    iconBtn.addEventListener('click', () => setOpen(!li.classList.contains('open')));

    // The text field can open a question, but never closes it.
    bubble.addEventListener('click', () => {
      if (!li.classList.contains('open')) setOpen(true);
    });
    bubble.addEventListener('keydown', (event) => {
      if (!li.classList.contains('open') && (event.key === 'Enter' || event.key === ' ')) {
        event.preventDefault();
        setOpen(true);
      }
    });

    setOpen(false);
    list.appendChild(li);
    scrollToBottom();
    return li;
  }

  window.addQuestion = addQuestion;

  /* ---------- Retrieve questions from Flask ---------- */

  // Keep track of questions already displayed
  const seenQuestionIds = new Set();

  async function loadQuestions() {
    try {
        const response = await fetch('/questions');

        if (!response.ok) {
            throw new Error('Could not retrieve questions');
        }

        const questions = await response.json();

        questions.forEach((question) => {
            // Only display questions we haven't seen before
            if (!seenQuestionIds.has(question.id)) {
                seenQuestionIds.add(question.id);

                const date = new Date(question.created_at);

                addQuestion(question.question, date);
            }
        });

    } catch (error) {
        console.error('Error loading questions:', error);
    }
  }

// Load existing questions immediately
loadQuestions();

// Check for new questions every 2 seconds
setInterval(loadQuestions, 2000);

  // /* ---------- TEST ONLY: top bar adds a predetermined question ---------- */

  // var testQuestion = 'Hi, this is the question I asked. You chose to see the question by clicking on it, indicated by the icon change. I LOOOOOVE asking questions';

  // function addTestQuestion() {
  //   addQuestion(testQuestion);
  // }

  // testBar.addEventListener('click', addTestQuestion);
  // testBar.addEventListener('keydown', (event) => {
  //   if (event.key === 'Enter' || event.key === ' ') {
  //     event.preventDefault();
  //     addTestQuestion();
  //   }
  // });
})();
