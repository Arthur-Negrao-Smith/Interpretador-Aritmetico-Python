let Total = 0;

const result = document.getElementById('.result');

function addOperator(operator) {
    const inputField = document.getElementById('expression-input');
    inputField.value += operator;
    inputField.focus()
}