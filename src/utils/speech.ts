// Speech synthesis utility for English pronunciation
export class SpeechService {
  private static instance: SpeechService;
  private synth: SpeechSynthesis;
  private voices: SpeechSynthesisVoice[] = [];
  private englishVoice: SpeechSynthesisVoice | null = null;
  private russianVoice: SpeechSynthesisVoice | null = null;

  private constructor() {
    this.synth = window.speechSynthesis;
    this.loadVoices();
  }

  static getInstance(): SpeechService {
    if (!SpeechService.instance) {
      SpeechService.instance = new SpeechService();
    }
    return SpeechService.instance;
  }

  private loadVoices() {
    this.voices = this.synth.getVoices();
    
    if (this.voices.length === 0) {
      this.synth.onvoiceschanged = () => {
        this.voices = this.synth.getVoices();
        this.selectBestVoices();
      };
    } else {
      this.selectBestVoices();
    }
  }

  private selectBestVoices() {
    // Find best English voice
    const englishVoices = this.voices.filter(v => v.lang.startsWith('en'));
    
    // Prefer Google or Microsoft voices for better quality
    this.englishVoice = englishVoices.find(v => 
      v.name.includes('Google') || v.name.includes('Microsoft')
    ) || englishVoices.find(v => v.lang === 'en-US') || englishVoices[0] || null;

    // Find Russian voice
    const russianVoices = this.voices.filter(v => v.lang.startsWith('ru'));
    this.russianVoice = russianVoices.find(v => 
      v.name.includes('Google') || v.name.includes('Microsoft')
    ) || russianVoices[0] || null;
  }

  speak(text: string, lang: 'en' | 'ru' = 'en', rate: number = 0.85): Promise<void> {
    return new Promise((resolve, reject) => {
      // Cancel any ongoing speech
      this.synth.cancel();

      // Reload voices if needed
      if (this.voices.length === 0) {
        this.loadVoices();
      }

      const utterance = new SpeechSynthesisUtterance(text);
      
      if (lang === 'en') {
        utterance.lang = 'en-US';
        if (this.englishVoice) {
          utterance.voice = this.englishVoice;
        }
      } else {
        utterance.lang = 'ru-RU';
        if (this.russianVoice) {
          utterance.voice = this.russianVoice;
        }
      }

      utterance.rate = rate;
      utterance.pitch = 1;
      utterance.volume = 1;

      utterance.onend = () => resolve();
      utterance.onerror = (e) => {
        if (e.error !== 'canceled') {
          reject(e);
        }
      };

      this.synth.speak(utterance);
    });
  }

  speakWord(word: string): Promise<void> {
    return this.speak(word, 'en', 0.75);
  }

  speakSentence(sentence: string): Promise<void> {
    return this.speak(sentence, 'en', 0.85);
  }

  speakSlow(word: string): Promise<void> {
    return this.speak(word, 'en', 0.5);
  }

  stop() {
    this.synth.cancel();
  }

  isSpeaking(): boolean {
    return this.synth.speaking;
  }
}

export const speechService = SpeechService.getInstance();
