/*
 * JavaScript for the AutoGen Multi-Agent Code Generator frontend
 */

// Initialize when the DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Form submission handler
    document.getElementById('codeForm').addEventListener('submit', handleFormSubmit);
    
    // Tab switching enhancement
    setupTabNavigation();
    
    // Add animation to agent cards
    setupAgentAnimations();
});

/**
 * Handle form submission for code generation
 */
async function handleFormSubmit(e) {
    e.preventDefault();
    
    // Get form data
    const requirements = document.getElementById('requirements').value;
    const language = document.getElementById('language').value;
    const complexity = document.getElementById('complexity').value;
    
    // Validate input
    if (!requirements.trim()) {
        showAlert('Please enter your requirements', 'warning');
        return;
    }
    
    // Disable button and show loading
    const generateBtn = document.getElementById('generateBtn');
    const originalBtnText = generateBtn.innerHTML;
    generateBtn.disabled = true;
    generateBtn.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Generating...';
    
    try {
        // Send request to generate code
        const response = await fetch('/api/v1/generate-code', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                requirements: requirements,
                language: language,
                complexity: complexity
            })
        });
        
        if (!response.ok) {
            throw new Error(`Failed to generate code: ${response.status} ${response.statusText}`);
        }
        
        const data = await response.json();
        const taskId = data.task_id;
        
        // Show status card
        showStatusCard();
        updateStatus('Processing...', 'processing', 30);
        
        // Poll for task status
        await pollTaskStatus(taskId);
        
    } catch (error) {
        console.error('Error:', error);
        showAlert('Error generating code: ' + error.message, 'danger');
        resetForm(originalBtnText);
    }
}

/**
 * Poll for task status
 */
async function pollTaskStatus(taskId) {
    try {
        const response = await fetch(`/api/v1/code-status/${taskId}`);
        
        if (!response.ok) {
            throw new Error(`Failed to get task status: ${response.status} ${response.statusText}`);
        }
        
        const data = await response.json();
        
        if (data.status === 'completed') {
            // Task completed, show results
            showResults(data.result);
            updateStatus('Completed!', 'completed', 100);
            resetForm();
        } else if (data.status === 'failed') {
            // Task failed
            updateStatus('Failed: ' + data.error, 'failed', 0);
            resetForm();
        } else {
            // Still processing, continue polling
            updateStatus('Processing...', 'processing', 60);
            setTimeout(() => pollTaskStatus(taskId), 2000);
        }
    } catch (error) {
        console.error('Error polling task status:', error);
        updateStatus('Error: ' + error.message, 'failed', 0);
        resetForm();
    }
}

/**
 * Show results in the UI with formatted code
 */
function showResults(result) {
    // Show result card
    document.getElementById('resultCard').style.display = 'block';
    
    // Populate results with formatted code
    document.getElementById('generatedCode').innerHTML = formatCodeOutput(result.generated_code || 'No code generated');
    document.getElementById('codeReview').innerHTML = formatCodeOutput(JSON.stringify(result.review_result, null, 2));
    document.getElementById('optimizedCode').innerHTML = formatCodeOutput(result.optimization_result?.optimized_code || 'No optimized code');
    document.getElementById('testCode').innerHTML = formatCodeOutput(result.test_result?.test_code || 'No tests generated');
    
    // Apply syntax highlighting
    applySyntaxHighlighting();
    
    // Scroll to results
    document.getElementById('resultCard').scrollIntoView({ behavior: 'smooth' });
}

/**
 * Update status display
 */
function updateStatus(text, status, progress) {
    document.getElementById('statusText').textContent = text;
    document.getElementById('statusIndicator').className = 'status-indicator status-' + status;
    document.getElementById('progressBar').style.width = progress + '%';
}

/**
 * Show status card
 */
function showStatusCard() {
    document.getElementById('statusCard').style.display = 'block';
}

/**
 * Reset form to initial state
 */
function resetForm(originalBtnText) {
    const generateBtn = document.getElementById('generateBtn');
    generateBtn.disabled = false;
    generateBtn.innerHTML = originalBtnText || 'Generate Code';
}

/**
 * Set up tab navigation enhancement
 */
function setupTabNavigation() {
    const tabs = document.querySelectorAll('[data-bs-toggle="tab"]');
    tabs.forEach(tab => {
        tab.addEventListener('shown.bs.tab', function (e) {
            // Add visual feedback when tab is switched
            const target = document.querySelector(e.target.getAttribute('data-bs-target'));
            target.classList.add('fade-in');
            setTimeout(() => target.classList.remove('fade-in'), 300);
        });
    });
}

/**
 * Set up agent card animations
 */
function setupAgentAnimations() {
    const agentCards = document.querySelectorAll('.agent-card .d-flex');
    agentCards.forEach((card, index) => {
        // Add delay for staggered animation
        card.style.animationDelay = (index * 0.1) + 's';
        
        // Add hover effect
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateX(5px)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateX(0)';
        });
    });
}

/**
 * Show alert message
 */
function showAlert(message, type) {
    // Create alert element
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.role = 'alert';
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;
    
    // Insert before form
    const form = document.getElementById('codeForm');
    form.parentNode.insertBefore(alertDiv, form);
    
    // Auto-dismiss after 5 seconds
    setTimeout(() => {
        if (alertDiv.parentNode) {
            alertDiv.parentNode.removeChild(alertDiv);
        }
    }, 5000);
}

// Add fade-in CSS for tab transitions and code formatting
const style = document.createElement('style');
style.textContent = `
    .fade-in {
        animation: fadeIn 0.3s ease-in;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .code-container {
        background-color: #2d2d2d;
        border-radius: 8px;
        overflow: hidden;
        margin: 15px 0;
    }
    
    .code-header {
        background-color: #1e1e1e;
        padding: 10px 15px;
        color: #ccc;
        font-size: 12px;
        font-weight: 500;
        border-bottom: 1px solid #444;
    }
    
    .code-content {
        padding: 20px;
        font-family: 'Fira Code', 'Courier New', monospace;
        font-size: 14px;
        line-height: 1.5;
        max-height: 400px;
        overflow: auto;
    }
    
    .code-content pre {
        margin: 0;
        color: #f8f8f2;
    }
    
    .code-content .comment { color: #6a9955; }
    .code-content .keyword { color: #569cd6; }
    .code-content .string { color: #ce9178; }
    .code-content .number { color: #b5cea8; }
    .code-content .function { color: #dcdcaa; }
    .code-content .class { color: #4ec9b0; }
    .code-content .operator { color: #d4d4d4; }
    
    .text-content {
        background-color: #f8f9fa;
        border-left: 4px solid #007bff;
        padding: 15px;
        margin: 10px 0;
        border-radius: 4px;
        color: #333;
        line-height: 1.6;
    }
`;
document.head.appendChild(style);

/**
 * Format code output by separating text and code blocks
 * with double line breaks and removes code comments
 */
function formatCodeOutput(content) {
    if (!content || typeof content !== 'string') {
        return '<div class="text-content">没有可用内容</div>';
    }
    
    // Check if content contains code blocks
    const codeBlockRegex = /```(?:python)?\s*\n([\s\S]*?)```/g;
    const hasCodeBlocks = codeBlockRegex.test(content);
    
    if (!hasCodeBlocks) {
        // If no code blocks, treat as plain text with double line breaks
        const paragraphs = content.split('\n\n').filter(p => p.trim());
        return paragraphs.map(p => `<div class="text-content">${escapeHtml(p.trim())}</div>`).join('\n\n');
    }
    
    let formattedContent = '';
    let lastIndex = 0;
    
    // Reset regex
    codeBlockRegex.lastIndex = 0;
    
    let match;
    while ((match = codeBlockRegex.exec(content)) !== null) {
        // Add text before code block with double line breaks
        const textBefore = content.substring(lastIndex, match.index);
        if (textBefore.trim()) {
            const paragraphs = textBefore.split('\n\n').filter(p => p.trim());
            paragraphs.forEach(paragraph => {
                formattedContent += `<div class="text-content">${escapeHtml(paragraph.trim())}</div>`;
            });
        }
        
        // Add code block with comments removed
        const codeContent = removeComments(match[1].trim());
        formattedContent += `
            <div class="code-container">
                <div class="code-header">Python 代码</div>
                <div class="code-content">
                    <pre><code class="language-python">${escapeHtml(codeContent)}</code></pre>
                </div>
            </div>
        `;
        
        lastIndex = match.index + match[0].length;
    }
    
    // Add remaining text after last code block with double line breaks
    const remainingText = content.substring(lastIndex);
    if (remainingText.trim()) {
        const paragraphs = remainingText.split('\n\n').filter(p => p.trim());
        paragraphs.forEach(paragraph => {
            formattedContent += `<div class="text-content">${escapeHtml(paragraph.trim())}</div>`;
        });
    }
    
    return formattedContent;
}

/**
 * Escape HTML special characters
 */
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

/**
 * Remove comments from Python code
 */
function removeComments(code) {
    // Remove single line comments
    let cleanedCode = code.replace(/#.*$/gm, '');
    
    // Remove multi-line comments (docstrings)
    cleanedCode = cleanedCode.replace(/"""[\s\S]*?"""|'''[\s\S]*?'''/g, '');
    
    // Remove empty lines and trim
    return cleanedCode
        .split('\n')
        .map(line => line.trim())
        .filter(line => line.length > 0)
        .join('\n');
}

/**
 * Apply basic syntax highlighting to code blocks
 */
function applySyntaxHighlighting() {
    const codeBlocks = document.querySelectorAll('.code-content code');
    codeBlocks.forEach(block => {
        let code = block.innerHTML;
        
        // Basic Python syntax highlighting
        code = code
            .replace(/(#.*)/g, '<span class="comment">$1</span>')
            .replace(/\b(def|class|if|else|elif|for|while|return|import|from|as|try|except|finally|with|lambda|yield|async|await|True|False|None)\b/g, '<span class="keyword">$1</span>')
            .replace(/('.*?'|".*?")/g, '<span class="string">$1</span>')
            .replace(/\b(\d+\.?\d*)\b/g, '<span class="number">$1</span>')
            .replace(/\b([a-zA-Z_][a-zA-Z0-9_]*)\s*\(/g, '<span class="function">$1</span>(')
            .replace(/\b(class)\s+([a-zA-Z_][a-zA-Z0-9_]*)/g, '<span class="keyword">$1</span> <span class="class">$2</span>')
            .replace(/(\+|\-|\*|\/|\=|\<|\>|\&|\||\!|\%|\^)/g, '<span class="operator">$1</span>');
        
        block.innerHTML = code;
    });
}