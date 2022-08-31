let titleEl = document.getElementById("Title");
let artistEl = document.getElementById("Artist");
function getMetaData() {
    fetch("/api/getmetadata")
        .then((res) => {
            res.json().then((res) => {
                console.log(res);
                titleEl.textContent = `${res.title}`;
                artistEl.textContent = `By ${res.artist}`;
            });
        })
        .catch((e) => {
            console.error(e);
        });
}
getMetaData();
setInterval(getMetaData, 5 * 1000);
