import { writable } from 'svelte/store';

export const shakeDetection = writable(false);
export const textToSpeech = writable(false);
export const selectedVoice = writable<string | null>(null);
