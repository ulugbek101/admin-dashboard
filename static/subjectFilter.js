const subjectSearchField = document.getElementById('search-field')
let rows = document.querySelector('.subjects-table tbody')

function updateSubjectsList(subjectsList) {
    rows.innerHTML = ""
    subjectsList.forEach((filteredSubject, index) => {
        rows.innerHTML += `
            <tr>
                <td>${index + 1}</td>
                <td>${filteredSubject.name}</td>
                <td>${filteredSubject.groups_count}</td>
                <td>${filteredSubject.pupils_count}</td>
                <td class="manage-pupil">
                    <div class="row-change-controller">
                        <a href="/update-subject/${filteredSubject.id}/">
                            <span class="material-icons-sharp"> edit </span>
                        </a>
                        <a href="/delete-subject/${filteredSubject.id}/">
                                    <span class="material-icons-sharp"> delete </span>
                        </a>
                    </div>
                </td>
            </tr>
        `
    })
}

function filterSubjects(event) {
    const subjectName = event.target.value
    if (subjectName.trim().length === 0) {
        updateSubjectsList(subjectsList)
        return
    }
    const filteredSubjects = subjectsList.filter(subject => subject.name.toLowerCase().includes(subjectName.toLowerCase()))
    updateSubjectsList(filteredSubjects)
}

subjectSearchField.addEventListener('keyup', filterSubjects)
