// CODE FOR CONTROLS
let playPauseEl = document.getElementById("play/pause");
console.log(playPauseEl);
let sourceEl = document.getElementById("streamSRC");
let volUpEl = document.getElementById("volUp");
let volDownEl = document.getElementById("volDown");
let playerEl = document.getElementById("player");
let originalSourceUrl = sourceEl.getAttribute("src");

function play() {
    console.log("PLAYING!");
    playPauseEl.innerHTML =
        '<span class="material-symbols-outlined">pause</span>';

    if (!sourceEl.getAttribute("src")) {
        sourceEl.setAttribute("src", originalSourceUrl);
        playerEl.load(); // This restarts the stream download
    }

    playerEl.muted = false;
    playerEl.play();
}
function pause() {
    console.log("PAUSED!");
    playPauseEl.innerHTML =
        '<span class="material-symbols-outlined">play_arrow</span>';

    sourceEl.setAttribute("src", "");
    playerEl.pause();
    setTimeout(function () {
        playerEl.load();
    });
    playerEl.muted = true;
}

playerEl.addEventListener("canplaythrough", () => {
    playerEl.muted = true;
    play();
});

playerEl.muted = true;
playPauseEl.addEventListener("click", () => {
    console.log("ye");
    console.log(playerEl.muted);
    if (playerEl.muted === true) {
        play();
    } else {
        pause();
    }
});
volUpEl.addEventListener("click", () => {
    playerEl.volume += 0.1;
});
volDownEl.addEventListener("click", () => {
    if (playerEl.volume > 0.1) playerEl.volume -= 0.1;
});

// CODE FOR METATADA!!

let titleEl = document.getElementById("Title");
let artistEl = document.getElementById("Artist");
let albumEl = document.getElementById("Album");
let coverEl = document.getElementById("albumcover");
function getMetaData() {
    fetch("/api/getmetadata")
        .then((res) => {
            res.json().then((res) => {
                console.log(res);
                titleEl.textContent = `${res.title}`;
                artistEl.textContent = `By ${res.artist}`;
                albumEl.textContent = `from ${res.album}`;
            });
        })
        .catch((e) => {
            console.error(e);
        });
}
function getCoverArt() {
    fetch("/api/cover")
        .then((res) => {
            res.json().then((res) => {
                console.log(res);
                coverEl.src = "data:image/png;base64," + res.img;
            });
        })
        .catch((e) => {
            console.error(e);
        });
}
getCoverArt();
setInterval(getCoverArt, 5 * 1000);
getMetaData();
setInterval(getMetaData, 5 * 1000);
