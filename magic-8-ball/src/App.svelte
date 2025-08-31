<script lang="ts">
  import { onMount } from 'svelte';

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
  }

  onMount(() => {
    let lastX: number, lastY: number, lastZ: number;
    let moveCounter = 0;
    const shakeThreshold = 15;

    window.addEventListener('devicemotion', (event) => {
      const { x, y, z } = event.accelerationIncludingGravity!;
      if (lastX === undefined) {
        lastX = x!;
        lastY = y!;
        lastZ = z!;
        return;
      }

      const deltaX = Math.abs(x! - lastX);
      const deltaY = Math.abs(y! - lastY);
      const deltaZ = Math.abs(z! - lastZ);

      if (deltaX + deltaY + deltaZ > shakeThreshold) {
        moveCounter++;
      } else {
        moveCounter = 0;
      }

      if (moveCounter > 2) {
        getAnswer();
        moveCounter = 0;
      }

      lastX = x!;
      lastY = y!;
      lastZ = z!;
    });
  });
</script>

<div class="relative flex size-full min-h-screen flex-col bg-[#141122] dark justify-between group/design-root overflow-x-hidden">
    <div>
        <div class="flex items-center bg-[#141122] p-4 pb-2 justify-between">
            <h2 class="text-white text-lg font-bold leading-tight tracking-[-0.015em] flex-1 text-center pl-12 pr-12">
                Magic 8 Ball
            </h2>
        </div>
        <div class="flex max-w-[480px] flex-wrap items-end gap-4 px-4 py-3">
            <label class="flex flex-col min-w-40 flex-1">
                <input
                    placeholder="Ask a question"
                    class="form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-xl text-white focus:outline-0 focus:ring-0 border-none bg-[#2a2447] focus:border-none h-14 placeholder:text-[#9c93c8] p-4 text-base font-normal leading-normal"
                    bind:value={question}
                />
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
</div>
