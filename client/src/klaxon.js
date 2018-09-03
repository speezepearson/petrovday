class Klaxon {
  constructor() {
    this.audio = new Audio('/static/klaxon.mp3');
    this.intervalPlayer = null;
  }

  start() {
    if (this.intervalPlayer === null) {
      this.intervalPlayer = setInterval(() => this.audio.play(), 2900);
      this.audio.play();
    }
  }

  stop() {
    if (this.intervalPlayer !== null) {
      clearInterval(this.intervalPlayer);
      this.intervalPlayer = null;
      this.audio.pause();
      this.audio.currentTime = 0;
    }
  }
}

export default Klaxon;
