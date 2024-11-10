const isPreferentialField = document.getElementById('id_is_preferential');

if (isPreferentialField) {
    isPreferentialField.addEventListener('click', (event) => {
        if (event.target.checked) {
            let groupPaymentElement = document.createElement('div');
            groupPaymentElement.id = 'group-payment';
            groupPaymentElement.innerHTML = `
                <input type="number" name="group_payment" min="1" required="" id="id_group_payment"> 
            `;
            event.target.parentNode.insertAdjacentElement('beforeend', groupPaymentElement);
            document.getElementById("id_group_payment").focus()
        } else {
            const existingGroupPaymentElement = document.getElementById('group-payment');
            if (existingGroupPaymentElement) {
                existingGroupPaymentElement.remove();
            }
        }
    });
}
