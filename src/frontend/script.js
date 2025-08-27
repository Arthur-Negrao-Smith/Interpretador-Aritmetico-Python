const result = document.getElementById('result');
const inputField = document.getElementById('expression-input');
const analyzeButton = document.getElementById('enter-btn');
const errorArea = document.getElementById('error-area')
const resetButton = document.getElementById('reset-button')

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
            errorArea.textContent = `${data.type_error}` + `\n${data.error}`;
        }
    } catch (error) {
        console.error('Erro ao conectar com a API:', error);
        errorArea.textContent = 'Não foi possível conectar ao servidor.';
    }
};

const resetData = async () => {
    const resetUrl = apiUrl + "/interpreter/reset"; 

    try {
        const response = await fetch(resetUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        const data = await response.json();

        if (response.ok) {
            inputField.value = '';   
            result.textContent = '0';   
            errorArea.textContent = '';   
            alert("Os dados foram resetados com sucesso!");
        } else {
            console.error('Erro do servidor:', data);
            errorArea.textContent = 'Não foi possível resetar.';
        }
    } catch (error) {
        console.error('Erro ao conectar com a API para reset:', error);
        errorArea.textContent = 'Não foi possível conectar ao servidor para resetar.';
    }
};

analyzeButton.addEventListener('click', sendExpression);
resetButton.addEventListener('click', resetData)

inputField.addEventListener('keypress', (event) => {
    if (event.key === 'Enter') {
        sendExpression();
    }
});
