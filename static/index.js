const sideMenu = document.querySelector("aside");
const menuBtn = document.getElementById("menu-btn");
const closeBtn = document.getElementById("close-btn");
const modalCloseBtn = document.querySelector(".modal-window-top button");
const modalWindow = document.querySelector(".modal-window");
const modalWindowShade = document.querySelector(".modal-window-shade");

const darkMode = document.querySelector(".dark-mode");
let colorScheme;

function updateTheme() {
  if (localStorage.getItem("theme") === "dark") {
    document.querySelector('body').classList.add('dark-mode-variables')
  }
  else {
    document.querySelector('body').classList.remove('dark-mode-variables')
  }
}

(function setColorScheme() {
  if (!localStorage.getItem("theme")) {
    if (window.matchMedia('(prefers-color-scheme: dark)').matches) {
      colorScheme = "dark"
    }
    else {
      colorScheme = "light"
    }
    localStorage.setItem("theme", colorScheme);
    colorScheme === "dark" && document.querySelector('body').classList.add('dark-mode-variables');
    colorScheme === "light" && document.querySelector('body').classList.remove('dark-mode-variables');


  }
  else {
    updateTheme()
  }

  localStorage.getItem("theme") === "dark" ? darkMode.querySelector('span:nth-child(2)').classList.add('active') : darkMode.querySelector('span:nth-child(1)').classList.add('active');

})();

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

  darkMode.querySelector("span:nth-child(1)").classList.toggle("active");
  darkMode.querySelector("span:nth-child(2)").classList.toggle("active");

  darkMode.querySelector("span:nth-child(1)").classList.contains("active") && localStorage.setItem("theme", "light");
  darkMode.querySelector("span:nth-child(2)").classList.contains("active") && localStorage.setItem("theme", "dark");

  updateTheme()
});

const removeModalWindow = () => {
  modalWindow.classList.remove("modal-active");
  modalWindowShade.classList.remove("modal-active");
}

export { modalWindow, modalWindowShade };
