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
