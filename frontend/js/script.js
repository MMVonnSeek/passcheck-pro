// Configuração da API
const API_URL = 'http://localhost:5001';

// Estado da aplicação
let advancedOpen = false;

// Toggle da visibilidade da senha
function togglePassword() {
    const passwordInput = document.getElementById('password');
    const toggleIcon = document.getElementById('toggleIcon');
    
    if (passwordInput.type === 'password') {
        passwordInput.type = 'text';
        toggleIcon.classList.remove('fa-eye');
        toggleIcon.classList.add('fa-eye-slash');
    } else {
        passwordInput.type = 'password';
        toggleIcon.classList.remove('fa-eye-slash');
        toggleIcon.classList.add('fa-eye');
    }
}

// Toggle das opções avançadas
function toggleAdvanced() {
    const content = document.getElementById('advancedContent');
    const icon = document.getElementById('advancedIcon');
    
    advancedOpen = !advancedOpen;
    
    if (advancedOpen) {
        content.classList.add('show');
        icon.style.transform = 'rotate(180deg)';
    } else {
        content.classList.remove('show');
        icon.style.transform = 'rotate(0deg)';
    }
}

// Atualiza o medidor de força em tempo real
document.getElementById('password').addEventListener('input', function(e) {
    const password = e.target.value;
    updateStrengthMeter(password);
});

function updateStrengthMeter(password) {
    const meterFill = document.getElementById('meterFill');
    const strengthLabel = document.getElementById('strengthLabel');
    
    if (!password) {
        meterFill.style.width = '0%';
        strengthLabel.textContent = 'Aguardando...';
        return;
    }
    
    // Análise básica em tempo real
    let score = 0;
    
    // Comprimento
    if (password.length >= 8) score += 25;
    else if (password.length >= 6) score += 15;
    else score += 5;
    
    // Complexidade
    if (/[a-z]/.test(password)) score += 15;
    if (/[A-Z]/.test(password)) score += 15;
    if (/[0-9]/.test(password)) score += 15;
    if (/[^a-zA-Z0-9]/.test(password)) score += 20;
    
    // Sem padrões óbvios
    if (!/(123|abc|qwerty|senha|password)/i.test(password)) score += 10;
    
    // Limita o score
    score = Math.min(100, score);
    
    // Atualiza a barra
    meterFill.style.width = score + '%';
    
    // Atualiza o label
    if (score < 30) {
        meterFill.style.background = 'linear-gradient(135deg, #ef4444, #dc2626)';
        strengthLabel.textContent = '🔴 Muito Fraca';
    } else if (score < 50) {
        meterFill.style.background = 'linear-gradient(135deg, #f59e0b, #d97706)';
        strengthLabel.textContent = '🟠 Fraca';
    } else if (score < 70) {
        meterFill.style.background = 'linear-gradient(135deg, #f8c032, #f59e0b)';
        strengthLabel.textContent = '🟡 Moderada';
    } else if (score < 90) {
        meterFill.style.background = 'linear-gradient(135deg, #10b981, #059669)';
        strengthLabel.textContent = '🟢 Forte';
    } else {
        meterFill.style.background = 'linear-gradient(135deg, #8b5cf6, #6366f1)';
        strengthLabel.textContent = '🟣 Muito Forte';
    }
}

// Função principal de análise
async function analyzePassword() {
    const password = document.getElementById('password').value;
    
    if (!password) {
        alert('Por favor, digite uma senha para analisar');
        return;
    }
    
    // Mostra loading
    document.getElementById('loading').classList.add('show');
    document.getElementById('results').classList.remove('show');
    
    // Coleta informações pessoais
    const personalInfo = {
        name: document.getElementById('personalName').value,
        birth: document.getElementById('personalBirth').value,
        email: document.getElementById('personalEmail').value,
        company: document.getElementById('personalCompany').value
    };
    
    // Remove campos vazios
    Object.keys(personalInfo).forEach(key => {
        if (!personalInfo[key]) delete personalInfo[key];
    });
    
    try {
        let response;
        
        // Decide qual endpoint usar
        if (Object.keys(personalInfo).length > 0) {
            // Usa endpoint com contexto
            response = await fetch(`${API_URL}/analyze-with-context`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    password: password,
                    personal_info: personalInfo
                })
            });
        } else {
            // Usa endpoint simples
            response = await fetch(`${API_URL}/analyze`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    password: password
                })
            });
        }
        
        const data = await response.json();
        
        // Esconde loading
        document.getElementById('loading').classList.remove('show');
        
        // Mostra resultados
        displayResults(data);
        
    } catch (error) {
        console.error('Erro:', error);
        document.getElementById('loading').classList.remove('show');
        alert('Erro ao analisar senha. Verifique se a API está rodando.');
    }
}

// Exibe os resultados
function displayResults(data) {
    const resultsDiv = document.getElementById('results');
    
    // Cria o HTML dos resultados
    let feedbackHtml = '';
    
    if (data.feedback && data.feedback.length > 0) {
        data.feedback.forEach(msg => {
            let type = 'warning';
            if (msg.includes('✅')) type = 'success';
            if (msg.includes('❌')) type = 'error';
            
            feedbackHtml += `
                <div class="feedback-item ${type}">
                    <i class="fas ${type === 'success' ? 'fa-check-circle' : type === 'warning' ? 'fa-exclamation-triangle' : 'fa-times-circle'}"></i>
                    <span>${msg}</span>
                </div>
            `;
        });
    }
    
    // Detalhes das heurísticas
    let detailsHtml = '';
    if (data.details) {
        detailsHtml = '<div style="margin-top: 1rem; padding-top: 1rem; border-top: 1px solid #e2e8f0;">';
        detailsHtml += '<h4 style="margin-bottom: 0.5rem;">Detalhes Técnicos:</h4>';
        
        for (const [heuristic, result] of Object.entries(data.details)) {
            detailsHtml += `
                <div style="font-size: 0.9rem; margin-bottom: 0.5rem; padding: 0.5rem; background: #f8fafc; border-radius: 4px;">
                    <strong>${heuristic}:</strong> Score ${result.score}
                </div>
            `;
        }
        
        detailsHtml += '</div>';
    }
    
    resultsDiv.innerHTML = `
        <div style="text-align: center;">
            <div class="score-circle" style="background: conic-gradient(from 0deg, var(--primary) ${data.score * 3.6}deg, #e2e8f0 0deg);">
                <div class="score-text">${data.score}</div>
            </div>
            <h3 style="margin-bottom: 1rem;">${data.strength}</h3>
            ${feedbackHtml}
            ${detailsHtml}
        </div>
    `;
    
    resultsDiv.classList.add('show');
}

// Testa os endpoints da API
async function tryEndpoint(endpoint) {
    const responseDiv = document.getElementById('responseCode');
    
    try {
        let response;
        
        if (endpoint === 'health') {
            response = await fetch(`${API_URL}/health`);
        } else if (endpoint === 'analyze') {
            response = await fetch(`${API_URL}/analyze`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    password: 'exemplo123'
                })
            });
        } else if (endpoint === 'context') {
            response = await fetch(`${API_URL}/analyze-with-context`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    password: 'joao1990',
                    personal_info: {
                        name: 'Joao',
                        birth: '1990'
                    }
                })
            });
        }
        
        const data = await response.json();
        responseDiv.textContent = JSON.stringify(data, null, 2);
        
    } catch (error) {
        responseDiv.textContent = `Erro: ${error.message}`;
    }
}
