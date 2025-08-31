<script lang="ts">
  import { onMount } from 'svelte';
  import { shakeDetection, textToSpeech } from './stores';

  let motionPermissionGranted = false;
  let needsMotionPermission = false;

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
  });

  function handleShakeDetectionChange(event: Event) {
    const target = event.target as HTMLInputElement;
    shakeDetection.set(target.checked);
  }

  function handleTextToSpeechChange(event: Event) {
    const target = event.target as HTMLInputElement;
    textToSpeech.set(target.checked);
  }
</script>

<div class="absolute inset-0 bg-[#141122] bg-opacity-90 p-4 flex flex-col">
  <div class="flex items-center justify-between mb-4">
    <h2 class="text-white text-lg font-bold">Settings</h2>
    <button on:click={() => window.dispatchEvent(new Event('close-settings'))} class="text-white text-2xl">&times;</button>
  </div>

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
  </div>
</div>
