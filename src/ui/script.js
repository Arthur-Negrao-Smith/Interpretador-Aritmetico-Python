const result = document.getElementById('result');
const inputField = document.getElementById('expression-input');
const analyzeButton = document.getElementById('enter-btn');
const errorArea = document.getElementById('error-area')

const apiUrl = 'http://127.0.0.1:8000'

function addOperator(operator) {
    inputField.value += operator;
    inputField.focus()
}

const sendExpression = async () => {
    const expression = inputField.value;
    if (!expression) {
        result.textContent = '0';
        return;
    }

    const apiUrl_expressions = apiUrl + "/expressions" 

    try {
        const response = await fetch(apiUrl_expressions, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ expression: expression }),
        });

        const data = await response.json();

        if (response.ok) {
            result.textContent = `${data.result}`;
        } else {
            errorArea.textContent = data.type_error, data.error;
        }
    } catch (error) {
        console.error('Erro ao conectar com a API:', error);
        errorArea.textContent = 'Não foi possível conectar ao servidor.';
    }
};

analyzeButton.addEventListener('click', sendExpression);

inputField.addEventListener('keypress', (event) => {
    if (event.key === 'Enter') {
        sendExpression();
    }
});
