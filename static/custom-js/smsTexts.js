const smsTextsRaw = document.getElementById("sms-texts");
const smsTexts = JSON.parse(smsTextsRaw.textContent);
const smsTextsContainer = document.getElementById("sms-texts-container");
const smsBody = document.getElementById("sms-body");
let sendSMSButton = document.querySelector('button.send-sms')
let SMSModelWindowBackdrop = document.querySelector(
    '.sendSMSModalWindowBackdrop'
)

smsTexts.forEach(smsText => {
    const smsTextCard = document.createElement("div");
    smsTextCard.id = "smsTextCard";
    smsTextCard.className = "button";
    smsTextCard.style.cssText = `
        padding: 10px;
        width: 100%;
        border: 1px solid var(--color-dark-variant);
        border-radius: var(--border-radius-1);
        white-space: pre-wrap; /* Preserve newlines and spaces */
    `;
    smsTextCard.textContent = smsText;
    smsTextsContainer.appendChild(smsTextCard);
});

function addEventListenerToSMSCards() {
    const smsTextsContainer = document.getElementById("sms-texts-container");
    smsTextsContainer.addEventListener("click", function (event) {
        const clickedElement = event.target.closest("#smsTextCard");
        if (clickedElement) {
            smsBody.textContent = clickedElement.textContent.trim();
        }
    });
}

addEventListenerToSMSCards()

