const sideMenu = document.querySelector('aside')
const menuBtn = document.getElementById('menu-btn')
const closeBtn = document.getElementById('close-btn')
const modalCloseBtn = document.querySelector('.modal-window-top button')
const modalWindow = document.querySelector('.modal-window')
const modalWindowShade = document.querySelector('.modal-window-shade')
let sendSMSButton = document.querySelector('button.send-sms')
let sendSMSModalWindow = document.querySelector('.sendSMSModalWindow')
let sendSMSTextButton = document.querySelector('button.send-sms-button')
let SMSModelWindowBackdrop = document.querySelector(
    '.sendSMSModalWindowBackdrop'
)
let paymentAmountField = document.getElementById('id_amount')
let phoneNumberField = document.getElementById('phone')
let form = document.querySelector('.form')
let pupilCheckboxesSelector = document.querySelector(
    '.pupil-checkboxes-selector'
)

let checkedPupilsList = []

// To format payment amount in adding payment amount
function formatInput() {
    // Get the input element
    let inputElement = document.getElementById('id_amount')

    // Get the value entered by the user
    let value = inputElement.value

    // Remove non-digit characters from the value
    let numericValue = value.replace(/[^\d.]/g, '')

    // Format the numeric value with space every three digits
    let formattedValue = formatMoneyAmount(numericValue)

    // Set the formatted value back to the input
    inputElement.value = formattedValue
}

function formatMoneyAmount(amount) {
    // Split the amount into integer and fractional parts
    let parts = amount.split('.')

    // Format integer part with space every three digits
    parts[0] = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, ' ')

    // Join integer and fractional parts with dot
    return parts.join('.')
}

function sendSMSToCheckedPupils(pupilsList, smsText) {
    let pupilsListUnique = new Set(pupilsList)
    pupilsListUnique = new Array(...pupilsListUnique)

    fetch(
    	'/profiles/send-sms/',
    	{
    		method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                pupils: pupilsListUnique,
                text: smsText
            })
    	}
    )
}

function getAllCheckedPupils() {
    return document.querySelectorAll('.pupil-checkbox:checked')
}

function uncheckPupils() {
    let checkedPupils = getAllCheckedPupils()
    checkedPupils.forEach(checkbox => {
        checkbox.checked = false
    })
}

function hideSMSModelWindow() {
    sendSMSModalWindow.style.display = 'none'
    SMSModelWindowBackdrop.style.display = 'none'
}

function showSMSModelWindow() {
    sendSMSModalWindow.style.display = 'block'
    SMSModelWindowBackdrop.style.display = 'block'
}

if (pupilCheckboxesSelector) {
    pupilCheckboxesSelector.addEventListener('change', event => {
        let pupilCheckboxes = document.querySelectorAll('.pupil-checkbox')

        pupilCheckboxes.forEach(checkbox => {
            checkbox.checked = event.target.checked && true
        })
    })
}

if (form && form.querySelector('#id_amount')) {
    form.addEventListener('submit', event => {
        let paymentAmountField = form.querySelector('#id_amount')
        paymentAmountField.value = paymentAmountField.value.replaceAll(' ', '')
        form.submit()
    })
}

if (paymentAmountField) {
    formatInput()
    paymentAmountField.addEventListener('input', formatInput)
}

if (sendSMSButton) {
    sendSMSButton.addEventListener('click', event => {
        let pupilCheckboxes = document.querySelectorAll('.pupil-checkbox:checked')

        if (pupilCheckboxes.length === 0) return

        showSMSModelWindow()

        pupilCheckboxes.forEach(checkedPupil => {
            checkedPupilsList.push(checkedPupil.dataset.pupil)
        })

        uncheckPupils()
        pupilCheckboxesSelector.checked = false
    })
}

if (sendSMSTextButton) {
    sendSMSTextButton.addEventListener('click', event => {
        event.preventDefault()
        let smsText = document.getElementById('sms-body')

        if (smsText.value.trim().length === 0) return

        sendSMSToCheckedPupils(checkedPupilsList, smsText.value)

        uncheckPupils()
        hideSMSModelWindow()
        smsText.value = ''
        checkedPupilsList = []
    })
}

if (SMSModelWindowBackdrop) {
    SMSModelWindowBackdrop.addEventListener('click', () => {
        hideSMSModelWindow()
    })
}

if (phoneNumberField) {
    phoneNumberField.addEventListener('input', function (e) {
        var x = e.target.value
            .replace(/\D/g, '')
            .match(/(\d{0,3})(\d{0,2})(\d{0,3})(\d{0,2})(\d{0,2})/)
        e.target.value =
            '+(' + x[1] + ') ' + x[2] + '-' + x[3] + '-' + x[4] + '-' + x[5]
    })
}

const darkMode = document.querySelector('.dark-mode')
let colorScheme

function updateTheme() {
    if (localStorage.getItem('theme') === 'dark') {
        document.querySelector('body').classList.add('dark-mode-variables')
    } else {
        document.querySelector('body').classList.remove('dark-mode-variables')
    }
}

;(function setColorScheme() {
    if (!localStorage.getItem('theme')) {
        if (window.matchMedia('(prefers-color-scheme: dark)').matches) {
            colorScheme = 'dark'
        } else {
            colorScheme = 'light'
        }
        localStorage.setItem('theme', colorScheme)
        colorScheme === 'dark' &&
        document.querySelector('body').classList.add('dark-mode-variables')
        colorScheme === 'light' &&
        document.querySelector('body').classList.remove('dark-mode-variables')
    } else {
        updateTheme()
    }

    localStorage.getItem('theme') === 'dark'
        ? darkMode.querySelector('span:nth-child(2)').classList.add('active')
        : darkMode.querySelector('span:nth-child(1)').classList.add('active')
})()

modalWindowShade.addEventListener('click', () => {
    checkedPupilsList = []
    removeModalWindow()
})

modalCloseBtn.addEventListener('click', () => {
    removeModalWindow()
})

menuBtn.addEventListener('click', () => {
    sideMenu.style.display = 'block'
})

if (closeBtn) {
    closeBtn.addEventListener('click', () => {
        sideMenu.style.display = 'none'
    })
}

darkMode.addEventListener('click', () => {
    darkMode.querySelector('span:nth-child(1)').classList.toggle('active')
    darkMode.querySelector('span:nth-child(2)').classList.toggle('active')

    darkMode.querySelector('span:nth-child(1)').classList.contains('active') &&
    localStorage.setItem('theme', 'light')
    darkMode.querySelector('span:nth-child(2)').classList.contains('active') &&
    localStorage.setItem('theme', 'dark')

    updateTheme()
})

const removeModalWindow = () => {
    modalWindow.classList.remove('modal-active')
    modalWindowShade.classList.remove('modal-active')
}
