<script lang="ts">
  import { onMount } from 'svelte';
  import { textToSpeech, selectedVoice } from './lib/stores';
  import Settings from './lib/Settings.svelte';

  let question = "";
  let answer = "";
  const imageUrl = "https://lh3.googleusercontent.com/aida-public/AB6AXuCpAyL9LlB39CCfquvZSBM3YZN3HOsaSHBZ2uAZPenq31sPyTncvgV_5HsBQvv_FOFY5iB3npzC3XFnay0Op8h-zkNP783tJl4WWvgwyf6B4CfjAZx-3IW5_-EyWmHHdnaLA218WEMSI8_RO4oHBoJI5dz1wcpmSG1_CKzFHucDNb8A5yGDSVEun8dn5XYBQt_3oY0G4_vvCqlpmCB4SGDFdfZYFc_XC3a2IIzsPTK07z0rw49wZRyo1_r_9fdB9oVW5VwD-OnOG28";


  const answers = [
    "The answer is unclear",
    "Uncertain at this time",
    "I have no idea",
    "Absolutely yes!",
    "Ask again later",
    "Emphatically No!",
    "Signs point to yes, definitely!",
    "My sources say no, but they've been wrong before.",
    "Reply hazy, try again after a coffee.",
    "It is decidedly so.",
    "Outlook not so good, maybe ask your cat?",
    "You may rely on it.",
    "Error 404: Future not found."
  ];

  let lastShakeTime = 0;
  const shakeCooldown = 2000; // 2 seconds

  // Speech to Text
  let isListening = false;
  let recognition: SpeechRecognition | null = null;

  function getAnswer() {
    if (!question) {
      alert("Please ask a question first!");
      return;
    }
    const now = Date.now();
    if (now - lastShakeTime < shakeCooldown) {
      return;
    }
    lastShakeTime = now;
    const randomIndex = Math.floor(Math.random() * answers.length);
    answer = answers[randomIndex];

    if ($textToSpeech) {
      const utterance = new SpeechSynthesisUtterance(answer);
      const voices = speechSynthesis.getVoices();
      const voice = voices.find(v => v.voiceURI === $selectedVoice);
      if (voice) {
        utterance.voice = voice;
      }
      speechSynthesis.speak(utterance);
    }
  }

  onMount(() => {
    // Speech Recognition setup
    const SpeechRecognition = window.SpeechRecognition || (window as any).webkitSpeechRecognition;
    if (SpeechRecognition) {
      recognition = new SpeechRecognition();
      recognition.continuous = false;
      recognition.lang = navigator.language || 'en-US';
      recognition.interimResults = false;

      recognition.onresult = (event: SpeechRecognitionEvent) => {
        let finalTranscript = '';
        for (let i = event.resultIndex; i < event.results.length; ++i) {
          if (event.results[i].isFinal) {
            finalTranscript += event.results[i][0].transcript;
          }
        }
        if (finalTranscript) {
          question = (question ? question + ' ' : '') + finalTranscript.trim();
        }
      };

      recognition.onend = () => {
        isListening = false;
      };

      recognition.onerror = () => {
        isListening = false;
      };
    }

    window.addEventListener('shake', getAnswer);

    return () => {
      window.removeEventListener('shake', getAnswer);
    }
  });

  function toggleListen() {
    if (!recognition) return;
    if (isListening) {
      recognition.stop();
    } else {
      recognition.start();
    }
    isListening = !isListening;
  }
</script>

<main class="flex min-h-screen w-full items-center justify-center bg-[#141122]">
  <div class="w-full h-full max-w-lg max-h-[90vh] bg-[#141122] rounded-xl shadow-lg flex flex-col justify-between group/design-root overflow-x-hidden relative">
    <div class="flex items-center bg-[#141122] p-4 pb-2 justify-between">
      <h2 class="text-white text-lg font-bold leading-tight tracking-[-0.015em] flex-1 text-center pl-12">
        Magic 8 Ball
      </h2>
     <Settings />
    </div>



    <div class="flex max-w-[480px] flex-wrap items-end gap-4 px-4 py-3">
        <label class="relative flex flex-col min-w-40 flex-1">
          <input
            placeholder="Ask a question"
            class="form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-xl text-white focus:outline-0 focus:ring-0 border-none bg-[#2a2447] focus:border-none h-14 placeholder:text-[#9c93c8] p-4 text-base font-normal leading-normal pr-20"
            bind:value={question}
            on:input={() => { answer = ""; }}
            on:keydown={(e) => {
              if (e.key === 'Enter') getAnswer();
              else answer = "";
            }}
            autocomplete="off"
          />
          {#if question}
            <button
              type="button"
              class="absolute right-12 top-1/2 -translate-y-1/2 text-[#9c93c8] hover:text-white text-xl focus:outline-none"
              on:click={() => { question = ""; answer = ""; }}
              aria-label="Clear"
              tabindex="-1"
            >×</button>
          {/if}
          {#if recognition}
            <button
              type="button"
              class="absolute right-3 top-1/2 -translate-y-1/2 flex items-center justify-center w-8 h-8 rounded-full bg-[#2a2447] hover:bg-[#3a3360] border border-[#3a3360] focus:outline-none transition-colors duration-150 {isListening ? 'bg-red-200 border-red-500' : ''}"
              on:click={toggleListen}
              aria-label="Speak your question"
              tabindex="-1"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5 {isListening ? 'text-red-600' : 'text-[#9c93c8]'}" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                <path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"></path>
                <path d="M19 10v2a7 7 0 0 1-14 0v-2"></path>
                <line x1="12" y1="19" x2="12" y2="23"></line>
                <line x1="8" y1="23" x2="16" y2="23"></line>
              </svg>
            </button>
          {/if}
        </label>
    </div>
    <div class="flex w-full grow bg-[#141122] @container p-4">
      <div class="w-full gap-1 overflow-hidden bg-[#141122] @[480px]:gap-2 aspect-[2/3] rounded-xl flex">
        <div
          class="w-full bg-center bg-no-repeat bg-cover aspect-auto rounded-none flex-1 relative"
          style="background-image: url('{imageUrl}');"
          on:click={getAnswer}
        >
          {#if answer}
          <div class="absolute inset-0 flex items-center justify-center">
            <p class="text-white text-2xl font-bold text-center bg-black bg-opacity-50 p-4 rounded-lg">
              {answer}
            </p>
          </div>
          {/if}
        </div>
      </div>
    </div>
    <p class="text-white text-base font-normal leading-normal pb-3 pt-1 px-4 text-center">
      Tap the ball or shake your phone for an answer.
    </p>
  </div>
</main>
