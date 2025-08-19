/*
 * JavaScript for the AutoGen Multi-Agent Code Generator frontend with TailwindCSS
 */

// Agent status tracking
let activeAgents = {
    'requirements-agent': false,
    'codegen-agent': false,
    'review-agent': false,
    'optimization-agent': false,
    'testing-agent': false
};

// Agent steps mapping
const agentSteps = {
    'requirements': 'requirements-agent',
    'codegen': 'codegen-agent',
    'review': 'review-agent',
    'optimization': 'optimization-agent',
    'testing': 'testing-agent'
};

// Agent progress mapping (0-100%)
const agentProgress = {
    'requirements': 20,
    'codegen': 40,
    'review': 60,
    'optimization': 80,
    'testing': 90
};

// Current task tracking
let currentTaskId = null;
let pollingTimer = null;

// Initialize when the DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Form submission handler
    document.getElementById('codeForm').addEventListener('submit', handleFormSubmit);
    
    // Tab switching enhancement
    setupTabNavigation();
    
    // Add animation to agent cards
    setupAgentAnimations();
    
    // Initialize all agents to green (completed state)
    resetAgentStatus();
    
    // Set up page unload handler
    setupPageUnloadHandler();
    
    // Show first tab by default
    showDefaultTab();
    
    // Show status card by default (it's hidden in HTML)
    showStatusCard();
});

// Set up page unload handler to stop all processes
function setupPageUnloadHandler() {
    window.addEventListener('beforeunload', function(e) {
        // Cancel any ongoing polling
        if (pollingTimer) {
            clearTimeout(pollingTimer);
        }
        
        // If there's an active task, send a cancel request
        if (currentTaskId) {
            // Send a request to cancel the task (best effort)
            fetch(`/api/v1/cancel-task/${currentTaskId}`, {
                method: 'POST'
            }).catch(err => {
                // Ignore errors in cancel request
                console.log('Failed to cancel task:', err);
            });
        }
        
        // Reset UI to initial state
        resetToInitialState();
        
        // Return null to avoid showing a confirmation dialog
        return null;
    });
}

// Reset UI to initial state
function resetToInitialState() {
    // Reset form
    document.getElementById('codeForm').reset();
    
    // Reset button
    const generateBtn = document.getElementById('generateBtn');
    generateBtn.disabled = false;
    generateBtn.innerHTML = '生成代码';
    
    // Hide status card (it should be hidden by default)
    document.getElementById('statusCard').classList.add('hidden');
    
    // Reset status indicator
    document.getElementById('statusIndicator').className = 'status-indicator status-pending w-4 h-4 rounded-full mr-3';
    document.getElementById('statusText').textContent = '待处理...';
    document.getElementById('progressBar').style.width = '0%';
    
    // Reset agent indicators
    resetAgentStatus();
    
    // Clear all result content
    document.querySelectorAll('.result-content').forEach(content => {
        content.innerHTML = '';
    });
    
    // Show first tab
    showDefaultTab();
}

// Show default tab
function showDefaultTab() {
    // Hide all tab panes except the first one
    document.querySelectorAll('.tab-pane').forEach((pane, index) => {
        if (index === 0) {
            pane.classList.remove('hidden');
        } else {
            pane.classList.add('hidden');
        }
    });
    
    // Set first tab as active
    const firstTab = document.querySelector('.tab-button');
    if (firstTab) {
        firstTab.classList.add('active');
        firstTab.querySelector('span').classList.remove('hidden');
    }
}

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
        showAlert('请输入你的需求描述', 'warning');
        return;
    }
    
    // Reset and initialize agent status
    resetAgentStatus();
    
    // Disable button and show loading
    const generateBtn = document.getElementById('generateBtn');
    const originalBtnText = generateBtn.innerHTML;
    generateBtn.disabled = true;
    generateBtn.innerHTML = '<i class="fas fa-spinner fa-spin mr-2"></i>生成中...';
    
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
            throw new Error(`代码生成失败: ${response.status} ${response.statusText}`);
        }
        
        const data = await response.json();
        currentTaskId = data.task_id;
        
        // Show status card
        showStatusCard();
        updateStatus('处理中...', 'processing', 10);
        
        // Poll for task status
        await pollTaskStatus(currentTaskId);
        
    } catch (error) {
        console.error('Error:', error);
        showAlert('代码生成错误: ' + error.message, 'danger');
        resetForm(originalBtnText);
        resetAgentStatus();
        currentTaskId = null;
    }
}

/**
 * Poll for task status
 */
async function pollTaskStatus(taskId) {
    try {
        const response = await fetch(`/api/v1/code-status/${taskId}`);
        
        if (!response.ok) {
            throw new Error(`获取任务状态失败: ${response.status} ${response.statusText}`);
        }
        
        const data = await response.json();
        
        if (data.status === 'completed') {
            // Task completed, show results
            showResults(data.result);
            updateStatus('完成!', 'completed', 100);
            resetForm();
            resetAgentStatus(); // Reset to green when completed
            currentTaskId = null;
        } else if (data.status === 'failed') {
            // Task failed
            updateStatus('失败: ' + data.error, 'failed', 0);
            resetForm();
            resetAgentStatus(); // Reset to green when failed
            currentTaskId = null;
        } else {
            // Still processing, continue polling
            // Update agent status based on current processing step if available
            let progress = 30; // Default progress when no specific step is provided
            if (data.current_step) {
                updateAgentStatus(data.current_step);
                // Set progress based on current step
                progress = agentProgress[data.current_step] || 30;
            }
            updateStatus('处理中...', 'processing', progress);
            // Use pollingTimer to keep track of the timeout
            pollingTimer = setTimeout(() => pollTaskStatus(taskId), 2000);
        }
    } catch (error) {
        console.error('Error polling task status:', error);
        updateStatus('错误: ' + error.message, 'failed', 0);
        resetForm();
        resetAgentStatus(); // Reset to green when error
        currentTaskId = null;
    }
}

/**
 * Show results in the UI with formatted code
 */
function showResults(result) {
    // Populate results with formatted code
    document.getElementById('code-tab-content').querySelector('.result-content').innerHTML = formatCodeResult(result.generated_code || '未生成代码');
    document.getElementById('review-tab-content').querySelector('.result-content').innerHTML = formatReviewResult(result.review_result);
    document.getElementById('optimized-tab-content').querySelector('.result-content').innerHTML = formatCodeResult(result.optimization_result?.optimized_code || '未优化代码');
    document.getElementById('tests-tab-content').querySelector('.result-content').innerHTML = formatCodeResult(result.test_result?.test_code || '未生成测试');
    
    // Scroll to results
    document.getElementById('resultCard').scrollIntoView({ behavior: 'smooth' });
}

/**
 * Update status display
 */
function updateStatus(text, status, progress) {
    document.getElementById('statusText').textContent = text;
    document.getElementById('statusIndicator').className = 'status-indicator status-' + status + ' w-4 h-4 rounded-full mr-3';
    document.getElementById('progressBar').style.width = progress + '%';
}

/**
 * Show status card
 */
function showStatusCard() {
    document.getElementById('statusCard').classList.remove('hidden');
}

/**
 * Reset form to initial state
 */
function resetForm(originalBtnText) {
    const generateBtn = document.getElementById('generateBtn');
    generateBtn.disabled = false;
    generateBtn.innerHTML = originalBtnText || '生成代码';
}

/**
 * Reset all agent indicators to green (completed state)
 */
function resetAgentStatus() {
    Object.keys(activeAgents).forEach(agentId => {
        const indicator = document.querySelector(`#${agentId} .agent-indicator`);
        if (indicator) {
            indicator.className = 'agent-indicator w-3 h-3 rounded-full mr-3 bg-green-500';
            activeAgents[agentId] = false;
        }
    });
}

/**
 * Update agent status to show which agent is currently active
 */
function updateAgentStatus(currentStep) {
    // Reset all agents to green first
    resetAgentStatus();
    
    const agentId = agentSteps[currentStep];
    if (agentId && document.getElementById(agentId)) {
        const indicator = document.getElementById(agentId).querySelector('.agent-indicator');
        if (indicator) {
            indicator.className = 'agent-indicator w-3 h-3 rounded-full mr-3 bg-red-500 animate-pulse';
            activeAgents[agentId] = true;
        } else {
            console.log('Indicator not found for agent:', agentId);
        }
    } else {
        console.log('Agent not found for step:', currentStep, 'AgentId:', agentId);
    }
}

/**
 * Set up tab navigation enhancement
 */
function setupTabNavigation() {
    const tabs = document.querySelectorAll('.tab-button');
    const tabPanes = document.querySelectorAll('.tab-pane');
    
    tabs.forEach(tab => {
        tab.addEventListener('click', function(e) {
            e.preventDefault();
            
            // Remove active class from all tabs
            tabs.forEach(t => {
                t.classList.remove('active');
                t.querySelector('span').classList.add('hidden');
            });
            
            // Hide all tab panes
            tabPanes.forEach(pane => pane.classList.add('hidden'));
            
            // Add active class to clicked tab
            this.classList.add('active');
            this.querySelector('span').classList.remove('hidden');
            
            // Show corresponding tab pane
            const tabId = this.dataset.tab + '-tab-content';
            document.getElementById(tabId).classList.remove('hidden');
            
            // Add visual feedback
            document.getElementById(tabId).classList.add('fade-in');
            setTimeout(() => document.getElementById(tabId).classList.remove('fade-in'), 300);
        });
    });
}

/**
 * Set up agent card animations
 */
function setupAgentAnimations() {
    const agentCards = document.querySelectorAll('#requirements-agent, #codegen-agent, #review-agent, #optimization-agent, #testing-agent');
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
    alertDiv.className = `rounded-lg p-4 mb-6 ${
        type === 'warning' ? 'bg-yellow-50 text-yellow-800 border border-yellow-200' : 
        type === 'danger' ? 'bg-red-50 text-red-800 border border-red-200' : 
        'bg-blue-50 text-blue-800 border border-blue-200'
    }`;
    alertDiv.innerHTML = `
        <div class="flex items-center">
            <i class="fas fa-exclamation-circle mr-2"></i>
            <span>${message}</span>
            <button type="button" class="ml-auto text-lg" onclick="this.parentElement.parentElement.remove()">×</button>
        </div>
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

/**
 * Format review result with unified checking mechanism to prevent JSON string display
 */
function formatReviewResult(content) {
    if (!content) {
        return '<div class="text-content">没有可用内容</div>';
    }
    
    // If content is an object, extract meaningful information instead of displaying raw JSON
    if (typeof content === 'object') {
        try {
            // Extract key information from review result object
            let formattedContent = '';
            
            // Add overall assessment if available
            if (content.overall_assessment) {
                formattedContent += `<div class="text-content"><strong>总体评估:</strong> ${escapeHtml(content.overall_assessment)}</div>`;
            }
            
            // Add code quality score if available
            if (content.code_quality_score !== undefined) {
                formattedContent += `<div class="text-content"><strong>代码质量评分:</strong> ${content.code_quality_score}/100</div>`;
            }
            
            // Add PEP8 compliance if available
            if (content.pep8_compliance !== undefined) {
                const complianceText = content.pep8_compliance ? '符合' : '不符合';
                formattedContent += `<div class="text-content"><strong>PEP8合规性:</strong> ${complianceText}</div>`;
            }
            
            // Add issues if available
            if (content.issues && Array.isArray(content.issues) && content.issues.length > 0) {
                formattedContent += '<div class="text-content"><strong>发现的问题:</strong></div>';
                content.issues.forEach((issue, index) => {
                    formattedContent += `<div class="text-content">${index + 1}. ${escapeHtml(issue.description || issue)}</div>`;
                });
            }
            
            // Add suggestions if available
            if (content.suggestions && Array.isArray(content.suggestions) && content.suggestions.length > 0) {
                formattedContent += '<div class="text-content"><strong>改进建议:</strong></div>';
                content.suggestions.forEach((suggestion, index) => {
                    formattedContent += `<div class="text-content">${index + 1}. ${escapeHtml(suggestion.description || suggestion)}</div>`;
                });
            }
            
            // If no meaningful content was extracted, show a generic message
            if (!formattedContent) {
                formattedContent = '<div class="text-content">代码审查已完成</div>';
            }
            
            return formattedContent;
        } catch (e) {
            // If extraction fails, show a generic message
            return '<div class="text-content">代码审查已完成</div>';
        }
    }
    
    // If content is a string, format it appropriately
    if (typeof content === 'string') {
        // Check if content contains code blocks
        const codeBlockRegex = /```(?:python)?\s*\n([\s\S]*?)```/g;
        const hasCodeBlocks = codeBlockRegex.test(content);
        
        if (!hasCodeBlocks) {
            // If no code blocks, treat as plain text with line breaks
            const lines = content.split('\n');
            return lines.map(line => {
                if (line.trim()) {
                    return `<div class="text-content">${escapeHtml(line)}</div>`;
                }
                return '';
            }).join('');
        }
        
        let formattedContent = '';
        let lastIndex = 0;
        
        // Reset regex
        codeBlockRegex.lastIndex = 0;
        
        let match;
        while ((match = codeBlockRegex.exec(content)) !== null) {
            // Add text before code block
            const textBefore = content.substring(lastIndex, match.index);
            if (textBefore.trim()) {
                const lines = textBefore.split('\n');
                lines.forEach(line => {
                    if (line.trim()) {
                        formattedContent += `<div class="text-content">${escapeHtml(line)}</div>`;
                    }
                });
            }
            
            // Add code block
            const codeContent = match[1];
            formattedContent += formatCodeBlock(codeContent);
            
            lastIndex = match.index + match[0].length;
        }
        
        // Add remaining text after last code block
        const remainingText = content.substring(lastIndex);
        if (remainingText.trim()) {
            const lines = remainingText.split('\n');
            lines.forEach(line => {
                if (line.trim()) {
                    formattedContent += `<div class="text-content">${escapeHtml(line)}</div>`;
                }
            });
        }
        
        return formattedContent;
    }
    
    // Fallback for any other content type
    return `<div class="text-content">${escapeHtml(String(content))}</div>`;
}

/**
 * Format code result with unified checking mechanism to ensure valid Python code
 * and comment out irrelevant content with single-line comments
 */
function formatCodeResult(content) {
    if (!content || typeof content !== 'string') {
        return '<div class="text-content">没有可用内容</div>';
    }
    
    // Check if content contains code blocks
    const codeBlockRegex = /```(?:python)?\s*\n([\s\S]*?)```/g;
    const hasCodeBlocks = codeBlockRegex.test(content);
    
    if (!hasCodeBlocks) {
        // If no code blocks, check if it's valid Python code
        if (isValidPythonCode(content)) {
            return formatCodeBlock(content);
        } else {
            // If not valid Python code, treat as plain text with line breaks
            const lines = content.split('\n');
            return lines.map(line => {
                if (line.trim()) {
                    return `<div class="text-content">${escapeHtml(line)}</div>`;
                }
                return '';
            }).join('');
        }
    }
    
    let formattedContent = '';
    let lastIndex = 0;
    
    // Reset regex
    codeBlockRegex.lastIndex = 0;
    
    let match;
    while ((match = codeBlockRegex.exec(content)) !== null) {
        // Add text before code block
        const textBefore = content.substring(lastIndex, match.index);
        if (textBefore.trim()) {
            const lines = textBefore.split('\n');
            lines.forEach(line => {
                if (line.trim()) {
                    formattedContent += `<div class="text-content"># ${escapeHtml(line)}</div>`;
                }
            });
        }
        
        // Add code block
        const codeContent = match[1];
        formattedContent += formatCodeBlock(codeContent);
        
        lastIndex = match.index + match[0].length;
    }
    
    // Add remaining text after last code block
    const remainingText = content.substring(lastIndex);
    if (remainingText.trim()) {
        const lines = remainingText.split('\n');
        lines.forEach(line => {
            if (line.trim()) {
                formattedContent += `<div class="text-content"># ${escapeHtml(line)}</div>`;
            }
        });
    }
    
    return formattedContent;
}

/**
 * Format a code block with proper styling and line preservation
 */
function formatCodeBlock(code) {
    // Preserve line breaks and indentation
    const formattedCode = code
        .split('\n')
        .map(line => line) // Keep original lines as they are
        .join('\n');
    
    if (!formattedCode.trim()) return '';
    
    return `
        <div class="code-container">
            <div class="code-header">Python 代码</div>
            <div class="code-content">
                <pre><code class="language-python">${escapeHtml(formattedCode)}</code></pre>
            </div>
        </div>
    `;
}

/**
 * Check if content is valid Python code
 */
function isValidPythonCode(code) {
    // Simple heuristic to check if content looks like Python code
    // This is not a full Python syntax checker, just a basic validation
    
    // Remove leading/trailing whitespace
    const trimmedCode = code.trim();
    
    // Empty code is not considered valid
    if (!trimmedCode) return false;
    
    // Check for common Python constructs
    const pythonPatterns = [
        /^import\s+\w/,                           // import statements
        /^from\s+\w+\s+import/,                  // from ... import statements
        /^class\s+\w+/,                           // class definitions
        /^def\s+\w+\s*\(/,                        // function definitions
        /^\s*if\s+.*:/,                           // if statements
        /^\s*for\s+.*:/,                          // for loops
        /^\s*while\s+.*:/,                        // while loops
        /^\s*try\s*:.*\s+except/,                // try/except blocks
        /^\s*with\s+.*:/,                         // with statements
        /=\s*.*$/,                                // assignments
        /^\s*[a-zA-Z_]\w*\s*\([^)]*\)/           // function calls
    ];
    
    // Check if code contains at least one Python pattern
    return pythonPatterns.some(pattern => pattern.test(trimmedCode));
}

/**
 * Escape HTML special characters
 */
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}