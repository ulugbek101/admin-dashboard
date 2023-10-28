const sideMenu = document.querySelector("aside");
const menuBtn = document.getElementById("menu-btn");
const closeBtn = document.getElementById("close-btn");
const modalCloseBtn = document.querySelector(".modal-window-top button");
const modalWindow = document.querySelector(".modal-window");
const modalWindowShade = document.querySelector(".modal-window-shade");

const darkMode = document.querySelector(".dark-mode");

modalWindowShade.addEventListener("click", () => {
  removeModalWindow();
});

modalCloseBtn.addEventListener("click", () => {
  removeModalWindow();
});

menuBtn.addEventListener("click", () => {
  sideMenu.style.display = "block";
});

closeBtn.addEventListener("click", () => {
  sideMenu.style.display = "none";
});

darkMode.addEventListener("click", () => {
  document.body.classList.toggle("dark-mode-variables");
  darkMode.querySelector("span:nth-child(1)").classList.toggle("active");
  darkMode.querySelector("span:nth-child(2)").classList.toggle("active");
});

const removeModalWindow = () => {
  modalWindow.classList.remove("modal-active");
  modalWindowShade.classList.remove("modal-active");
}

export {modalWindow, modalWindowShade};
