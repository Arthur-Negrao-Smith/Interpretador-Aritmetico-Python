// --- DOM Element References ---
/** @description Elemento HTML onde o resultado do interpretador é visualizado.*/
const result = document.getElementById('result');
/** @description Área de input onde o usuário digita uma expressão matemática.*/
const inputField = document.getElementById('expression-input');
/** @description Botão que envia a expressão para o interpretador.*/
const analyzeButton = document.getElementById('enter-btn');
/** @description Área para retorno de possíveis erros.*/
const errorArea = document.getElementById('error-area');
/** @description Botão que reseta valores de variáveis armazenadas no interpretador.*/
const resetButton = document.getElementById('reset-button');

// --- API Configuration ---

/** @description URL base para o API. */
const apiUrl = 'http://127.0.0.1:8000'

// --- Functions ---

/**
 * Adiciona um operador ou símbolo matemático para a área de input e mantém o foco nela.
 * É realizado o chamado nos botões disponíveis no HTML
 * @param {string} operator Caractere operador que é adicionado à expressão.
 */
function addOperator(operator) {
    inputField.value += operator;
    inputField.focus()
}

/**
 * Envia de maneira assíncrona a expressão matemática do input para a API do backend para análise.
 * Ele trata a resposta da API, atualizando o frontend ou com um resultado ou com uma mensagem de erro.
 * Também trata os erros de conexão se a API não estiver disponível.
 * @async
 * @returns {Promise<void>} Uma promessa que é cumprida quando a operação de busca e a atualização do frontend foram completadas.
 */
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
            // Em caso de sucesso, mostra o resultado da API
            result.textContent = `${data.result}`;
            errorArea.textContent = ''; // Apaga os possíveis erros anteriores
        } else {
            // Se houver algum erro, mostra o tipo de erro e a mensagem API.
            errorArea.textContent = `${data.type_error}` + `\n${data.error}`;
        }
    } catch (error) {
        console.error('Erro ao conectar com a API:', error);
        errorArea.textContent = 'Não foi possível conectar ao servidor.';
    }
};
/**
 * Envia de maneira assíncrona uma requisição para a API do backend para resetar o estado do interpretador.
 * Se for reset for um sucesso, também limpa todos os campos do frontend (input, result, error) e notifica o usuário com um alerta.
 * @async
 * @returns {Promise<void>} Uma promessa que é cumprida quando a operação de busca e a atualização do frontend foram completadas
 */
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
            // Limpa todos os campos e notifica o sucesso. 
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

// --- Event Listeners ---

/**
 * Attaches the sendExpression function to the click event of the analyze button.
 */
analyzeButton.addEventListener('click', sendExpression);

/**
 * Attaches the resetData function to the click event of the reset button.
 */
resetButton.addEventListener('click', resetData);

/**
 * Adds a keypress listener to the input field to allow form submission
 * by pressing the 'Enter' key, triggering the sendExpression function.
 */
inputField.addEventListener('keypress', (event) => {
    if (event.key === 'Enter') {
        sendExpression();
    }
});