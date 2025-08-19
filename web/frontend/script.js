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
 * Show results in the UI
 */
function showResults(result) {
    // Show result card
    document.getElementById('resultCard').style.display = 'block';
    
    // Populate results
    document.getElementById('generatedCode').textContent = result.generated_code || 'No code generated';
    document.getElementById('codeReview').textContent = JSON.stringify(result.review_result, null, 2);
    document.getElementById('optimizedCode').textContent = result.optimization_result?.optimized_code || 'No optimized code';
    document.getElementById('testCode').textContent = result.test_result?.test_code || 'No tests generated';
    
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

// Add fade-in CSS for tab transitions
const style = document.createElement('style');
style.textContent = `
    .fade-in {
        animation: fadeIn 0.3s ease-in;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
`;
document.head.appendChild(style);