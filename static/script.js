let titleEl = document.getElementById("Title");
let artistEl = document.getElementById("Artist");
let albumEl = document.getElementById("Album");
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
getMetaData();
setInterval(getMetaData, 5 * 1000);
