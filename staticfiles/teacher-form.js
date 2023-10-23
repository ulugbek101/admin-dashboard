import { modalWindow, modalWindowShade } from "./index.js";

const addTeacherBtn = document.querySelector(".add-user");
const teacherForm = document.querySelector(".teacher-form");

addTeacherBtn.addEventListener("click", () => {
  modalWindow.classList.add('modal-active');
  modalWindowShade.classList.add('modal-active');
});

teacherForm.addEventListener('submit', (event) => {
    event.preventDefault()
    console.log(event)
})
