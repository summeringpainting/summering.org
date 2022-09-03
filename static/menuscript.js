// MENU CODE YAA
let menuEl = document.getElementById("menu");
let menuPopupEl = document.getElementById("menupopup");
let overlayEl = document.getElementById("overlay");

menuEl.addEventListener("click", () => {
    menuPopupEl.style.display = "block";
    overlayEl.style.height = "100%";
});

overlayEl.addEventListener("click", () => {
    overlayEl.style.height = "0%";
    setTimeout(() => (menuPopupEl.style.display = "none"), 200);
});
