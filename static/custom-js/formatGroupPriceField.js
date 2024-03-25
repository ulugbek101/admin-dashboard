let groupPaymentAmountField = document.getElementById('id_price')

if (groupPaymentAmountField) {
	groupPaymentAmountField.addEventListener('input', formatInput)
	
	function formatInput() {
		// Get the input element
		let inputElement = document.getElementById('id_price')

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

	formatInput()
}
