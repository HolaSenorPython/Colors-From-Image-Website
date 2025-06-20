// This is my first time writing in JS!! Gonna make a sound play on
// button hover thanks to ChatGPT.

// Get element references.
const button = document.getElementById('clickBtn')
const sound = document.getElementById('clickSound')

// Play le sound!
button.addEventListener('click', (event) => {
    event.preventDefault(); // DON'T redirect immediately, play sound first
    sound.currentTime = 0; // Rewind to start of sound every click
    sound.volume = 0.8; // Set volume to 70%
    sound.play();

    // Make it so that visually, the button is back to unfocused mode
    button.blur();

    // Redirect to the anchor link AFTER the delay
    setTimeout(() => {
        window.location.href = button.href;
    }, 1400); // 1400 ms delay, equal to 1.4 seconds for the sound, let FULL sound play before redirect
})