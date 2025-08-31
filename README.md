# Magic 8 Ball

The Magic 8 Ball is a classic fortune-telling toy that provides answers to yes-or-no questions. Ask your question, shake (or tap) the ball, and receive a mysterious, sometimes humorous, answer!

---

## Python App (`pyapp`)

A simple command-line Magic 8 Ball game written in Python.
- This project uses uv to handle dependencies.
- Run it with Python 3.12 or later.
- Asks the user for a question and returns a random answer from a set of possibilities.

**How to run:**
```bash
cd pyapp
uv run main.py
```

---

## Svelte App (`magic-8-ball`)

A modern web version of the Magic 8 Ball built with Svelte, TypeScript, Vite, and Tailwind CSS.
- Responsive design for mobile and desktop.
- Features shake detection, speech-to-text input, and a fun UI.

**How to run locally:**
```bash
cd magic-8-ball
npm install
npm run dev
```

**How to build for production:**
```bash
npm run build
```

