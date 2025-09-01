<script lang="ts">
  import { onMount } from 'svelte';
  import { shakeDetection, textToSpeech, selectedVoice } from './stores';

  let motionPermissionGranted = false;
  let needsMotionPermission = false;
  let voices: SpeechSynthesisVoice[] = [];

  function setupShakeDetection() {
    let lastX: number, lastY: number, lastZ: number;
    let moveCounter = 0;
    const shakeThreshold = 15;

    window.addEventListener('devicemotion', (event) => {
      if (!$shakeDetection) return;

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
        window.dispatchEvent(new Event('shake'));
        moveCounter = 0;
      }

      lastX = x!;
      lastY = y!;
      lastZ = z!;
    });
  }

  async function requestMotionPermission() {
    if (typeof (DeviceMotionEvent as any).requestPermission === 'function') {
      try {
        const permissionState = await (DeviceMotionEvent as any).requestPermission();
        if (permissionState === 'granted') {
          motionPermissionGranted = true;
          $shakeDetection = true;
        } else {
          alert('Shake detection will not work without motion sensor permission.');
          $shakeDetection = false;
        }
      } catch (error) {
        console.error('Error requesting device motion permission:', error);
        $shakeDetection = false;
      }
    } else {
      motionPermissionGranted = true;
      $shakeDetection = true;
    }
  }

  onMount(() => {
    if (typeof (DeviceMotionEvent as any).requestPermission === 'function') {
      needsMotionPermission = true;
    } else {
      setupShakeDetection();
    }

    shakeDetection.subscribe(enabled => {
      if (enabled && needsMotionPermission && !motionPermissionGranted) {
        requestMotionPermission();
      } else if (enabled && (!needsMotionPermission || motionPermissionGranted)) {
        setupShakeDetection();
      }
    });

    function populateVoiceList() {
        voices = speechSynthesis.getVoices().filter(v => v.lang === 'en-US');
        if (voices.length > 0 && !$selectedVoice) {
            const lastVoice = voices.at(-1);
            selectedVoice.set(lastVoice.voiceURI);
        }
    }


    populateVoiceList();
    if (speechSynthesis.onvoiceschanged !== undefined) {
      speechSynthesis.onvoiceschanged = populateVoiceList;
    }
  });

  function handleShakeDetectionChange(event: Event) {
    const target = event.target as HTMLInputElement;
    shakeDetection.set(target.checked);
  }

  function handleTextToSpeechChange(event: Event) {
    const target = event.target as HTMLInputElement;
    textToSpeech.set(target.checked);
  }

  function handleVoiceChange(event: Event) {
    const target = event.target as HTMLSelectElement;
    console.log('selected voice:', target.value);
    selectedVoice.set(target.value);
  }
</script>

<div class="max-w-lg">
  <button popovertarget="desktop-menu-solutions" class="inline-flex items-center gap-x-1 text-sm/6 font-semibold text-gray-900 dark:text-white">
    <span class="hidden">Settings</span>
    <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
    </svg>
  </button>

  <el-popover id="desktop-menu-solutions" anchor="bottom start" popover class="w-screen max-w-none left-0 sm:max-w-max sm:left-auto overflow-visible bg-transparent px-4 transition transition-discrete [--anchor-gap:--spacing(5)] backdrop:bg-transparent open:flex data-closed:translate-y-1 data-closed:opacity-0 data-enter:duration-200 data-enter:ease-out data-leave:duration-150 data-leave:ease-in">
    <div class="w-screen max-w-sm flex-auto rounded-3xl bg-white p-4 text-sm/6 shadow-lg outline-1 outline-gray-900/5 dark:bg-gray-800 dark:shadow-none dark:-outline-offset-1 dark:outline-white/10">
      <div class="flex flex-col gap-4">
        <div class="flex items-center justify-between">
          <span class="text-white">Enable Shake Detection</span>
          <div class="group relative inline-flex w-11 shrink-0 rounded-full bg-gray-200 p-0.5 inset-ring inset-ring-gray-900/5 outline-offset-2 outline-indigo-600 transition-colors duration-200 ease-in-out has-checked:bg-indigo-600 has-focus-visible:outline-2 dark:bg-white/5 dark:inset-ring-white/10 dark:outline-indigo-500 dark:has-checked:bg-indigo-500">
            <span class="size-5 rounded-full bg-white shadow-xs ring-1 ring-gray-900/5 transition-transform duration-200 ease-in-out group-has-checked:translate-x-5"></span>
            <input type="checkbox" name="setting" aria-label="Enable Shake Detection" class="absolute inset-0 appearance-none focus:outline-hidden" on:change={handleShakeDetectionChange} checked={$shakeDetection} />
          </div>
        </div>
        <div class="flex items-center justify-between">
          <span class="text-white">Enable Text-to-Speech</span>
          <div class="group relative inline-flex w-11 shrink-0 rounded-full bg-gray-200 p-0.5 inset-ring inset-ring-gray-900/5 outline-offset-2 outline-indigo-600 transition-colors duration-200 ease-in-out has-checked:bg-indigo-600 has-focus-visible:outline-2 dark:bg-white/5 dark:inset-ring-white/10 dark:outline-indigo-500 dark:has-checked:bg-indigo-500">
            <span class="size-5 rounded-full bg-white shadow-xs ring-1 ring-gray-900/5 transition-transform duration-200 ease-in-out group-has-checked:translate-x-5"></span>
            <input type="checkbox" name="setting" aria-label="Enable Text-to-Speech" class="absolute inset-0 appearance-none focus:outline-hidden" on:change={handleTextToSpeechChange} checked={$textToSpeech} />
          </div>
        </div>
        <div>
          <label for="voice-select" class="block text-sm/6 font-medium text-gray-900 dark:text-white">Choose a voice</label>
          <div class="mt-2 grid grid-cols-1">
            <select
              id="voice-select"
              name="voice-select"
              class="col-start-1 row-start-1 w-full appearance-none rounded-md bg-white py-1.5 pr-8 pl-3 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 focus-visible:outline-2 focus-visible:-outline-offset-2 focus-visible:outline-indigo-600 sm:text-sm/6 dark:bg-white/5 dark:text-white dark:outline-white/10 dark:*:bg-gray-800 dark:focus-visible:outline-indigo-500"
              on:change={handleVoiceChange}
              bind:value={$selectedVoice}
            >
              {#each voices as voice}
                <option value={voice.voiceURI}>{voice.name} ({voice.lang})</option>
              {/each}
            </select>
            <svg viewBox="0 0 16 16" fill="currentColor" data-slot="icon" aria-hidden="true" class="pointer-events-none col-start-1 row-start-1 mr-2 size-5 self-center justify-self-end text-gray-500 sm:size-4 dark:text-gray-400">
              <path d="M4.22 6.22a.75.75 0 0 1 1.06 0L8 8.94l2.72-2.72a.75.75 0 1 1 1.06 1.06l-3.25 3.25a.75.75 0 0 1-1.06 0L4.22 7.28a.75.75 0 0 1 0-1.06Z" clip-rule="evenodd" fill-rule="evenodd" />
            </svg>
          </div>
        </div>
      </div>
    </div>
  </el-popover>
</div>
