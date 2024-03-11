const pupilSearchField = document.getElementById('search-field')
let rows = document.querySelector('.pupils-table tbody')
let table = document.querySelector('table')

function handlePupilCheckboxEvent() {
    let pupilCheckboxesSelector = document.querySelector(
        '.pupil-checkboxes-selector'
    )   
    if (pupilCheckboxesSelector) {
        pupilCheckboxesSelector.addEventListener('change', event => {
            let pupilCheckboxes = document.querySelectorAll('.pupil-checkbox')
    
            pupilCheckboxes.forEach(checkbox => {
                checkbox.checked = event.target.checked && true
            })
        })
    }
}

function updatePupilsList(pupilsList) {
    rows.innerHTML = ""

    if (pupilsList.length > 0) {
        rows.innerHTML += `
        <tr>
            <td></td>
            <td></td>
            <td></td>
            <td></td>
            <td></td>
            <td></td>
            <td>
                <input
                    class="pupil-checkboxes-selector"
                    style="width: 24px; height: 24px"
                    type="checkbox"
                />
            </td>
        </tr>
        `
    }

    pupilsList.forEach((filteredPupil, index) => {
        rows.innerHTML += `
            <tr>
                <td>${index + 1}</td>
                <td>${filteredPupil.fullName}</td>
                <td>${filteredPupil.groupName}</td>
                
                <td
                    class="${filteredPupil.payment === filteredPupil.groupPayment && 'success'}"
                >
                    ${filteredPupil.payment} / ${filteredPupil.groupPayment}
                </td>
                <td class="manage-pupil">
                    <div class="row-change-controller">
                        <a href="/update-pupil/${filteredPupil.id}/">
                            <span class="material-icons-sharp"> edit </span>
                        </a>
                        <a href="/delete-pupil/${filteredPupil.id}/">
                            <span class="material-icons-sharp"> delete </span>
                        </a>
                        ${isSuperuser.toLowerCase() === 'true' ? `
                        <a
                            href="/add_payment/${filteredPupil.groupId}/${filteredPupil.id}/"
                            >
                                <span class="material-icons-sharp"> credit_card </span>
                        </a>
                        ` : '<a href=""></a>'}
                    </div>
                </td>
                <td>${filteredPupil.phoneNumber}</td>
                <td>
                    <input
                        class="pupil-checkbox"
                        data-pupil="${filteredPupil.id}"
                        style="
                            height: 24px;
                            width: 24px;
                            accent-color: var(--color-success);
                        "
                        type="checkbox"
                    />
                </td>
            </tr>
        `
    }) 
} 

function filterSubjects(event) {
    const searchValue = event.target.value.toLowerCase()
    if (searchValue.trim().length === 0) {
        updatePupilsList(pupilsList)
        handlePupilCheckboxEvent()
        return
    }
    const filteredPupils = pupilsList.filter(pupil => {
        return pupil.fullName.toLowerCase().includes(searchValue) ||
                pupil.phoneNumber.replaceAll(' ', '').includes(searchValue) ||
                pupil.groupName.toLowerCase().includes(searchValue)
    })
    updatePupilsList(filteredPupils)
    handlePupilCheckboxEvent()
}

pupilSearchField.addEventListener('input', filterSubjects)

