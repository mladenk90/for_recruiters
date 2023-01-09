// load all content of page
document.addEventListener('DOMContentLoaded', function() {

});


// play/pause button
let playpause_btn = document.querySelector(".playpause-track");
// time seeker on song
let seek_slider = document.querySelector(".seek_slider");
let curr_time = document.querySelector(".current-time");
let total_duration = document.querySelector(".total-duration");

// confirm if playing already
let isPlaying = false;
let updateTimer;
// confirm current track
let curr_track = document.createElement('audio');
// function to load track
function loadTrack(curr_track) {
    // clear the previous intervals/reset
    clearInterval(updateTimer);
    resetValues();
    // load current track info
    curr_track.load()
    updateTimer = setInterval(seekUpdate, 1000);
}
// function to reset intervals
function resetValues() {
    seek_slider.value = 0;
  }
// playpromise via google
var playPromise = curr_track.play();
if (playPromise !== undefined) {
    playPromise.then(_ => {
        curr_track.pause();
    })
    
}
// function for play/pause button
function playpauseTrack() {
    // switch between playing and pausing depending on the current state
    if (!isPlaying) {
        playTrack();
    }
    else {
        pauseTrack();
    }
  }

function playTrack() {
    // play
    curr_track.play();
    isPlaying = true;

    // play button to pause button
    playpause_btn.innerHTML = '<i class="fa fa-pause-circle fa-5x"></i>';
}

function pauseTrack() {
// pause
    curr_track.pause();
    isPlaying = false;

    // pause button to play
    playpause_btn.innerHTML = '<i class="fa fa-play-circle fa-5x"></i>';
}

function seekTo() {
    // Calculate the seek position by the percentage of the seek slider and get the relative duration to the track
    seekto = curr_track.total_duration * (seek_slider.value / 100);
   
    // Set the current track position to the calculated seek position
    curr_track.currentTime = seekto;
  }
