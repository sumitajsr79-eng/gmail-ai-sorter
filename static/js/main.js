document.addEventListener('DOMContentLoaded', () => {
    const dryRunToggle = document.getElementById('dryRunToggle');
    const modeLabel = document.getElementById('modeLabel');

    if (dryRunToggle) {
        modeLabel.textContent = dryRunToggle.checked ? 'Dry-Run (Preview Only)' : 'Live Mode (Create & Apply Gmail Labels)';
        dryRunToggle.addEventListener('change', () => {
            if (dryRunToggle.checked) {
                modeLabel.textContent = 'Dry-Run (Preview Only)';
            } else {
                modeLabel.textContent = 'Live Mode (Create & Apply Gmail Labels)';
            }
        });
    }

    loadGmailLabels();
});

function toggleSetupModal() {
    const modal = document.getElementById('setupModal');
    modal.classList.toggle('hidden');
}

function toggleAppPasswordModal() {
    const modal = document.getElementById('appPasswordModal');
    modal.classList.toggle('hidden');
}

function toggleLabelInspectorModal() {
    const modal = document.getElementById('labelEmailsModal');
    modal.classList.toggle('hidden');
}

async function connectIMAP() {
    const email = document.getElementById('imapEmail').value.trim();
    const appPassword = document.getElementById('imapPassword').value.trim();

    if (!email || !appPassword) {
        alert('Please enter your Gmail address and 16-character App Password.');
        return;
    }

    try {
        const response = await fetch('/login_imap', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email: email, app_password: appPassword })
        });

        const data = await response.json();
        if (response.ok && data.status === 'success') {
            window.location.reload();
        } else {
            alert(data.error || 'Failed to authenticate via IMAP.');
        }
    } catch (err) {
        console.error(err);
        alert('Error connecting to server.');
    }
}

function removeCategory(btnElement) {
    const chip = btnElement.closest('.category-chip');
    chip.remove();
    updateCategoryCount();
}

function addCategory() {
    const input = document.getElementById('newCategoryInput');
    const val = input.value.trim();
    if (!val) return;

    const container = document.getElementById('categoriesContainer');
    const chip = document.createElement('div');
    chip.className = 'category-chip';
    chip.innerHTML = `
        <span class="cat-name">${escapeHtml(val)}</span>
        <button class="btn-remove" onclick="removeCategory(this)">✕</button>
    `;
    container.appendChild(chip);
    input.value = '';
    updateCategoryCount();
}

function updateCategoryCount() {
    const count = document.querySelectorAll('#categoriesContainer .category-chip').length;
    document.getElementById('categoryCount').textContent = `${count} active`;
}

function getCategories() {
    const chips = document.querySelectorAll('#categoriesContainer .cat-name');
    const list = [];
    chips.forEach(c => list.push(c.textContent.trim()));
    return list;
}

async function saveSettings() {
    const geminiKey = document.getElementById('geminiKeyInput').value.trim();
    const categories = getCategories();

    try {
        const response = await fetch('/api/save_settings', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                gemini_api_key: geminiKey,
                categories: categories
            })
        });
        const res = await response.json();
        if (res.status === 'success') {
            alert('Settings saved successfully!');
        }
    } catch (err) {
        console.error(err);
        alert('Failed to save settings');
    }
}

function updateProgressBar(percentage, statusText) {
    const fill = document.getElementById('progressBarFill');
    const text = document.getElementById('progressText');
    const status = document.getElementById('loaderStatusText');

    if (fill) fill.style.width = `${percentage}%`;
    if (text) text.textContent = `${percentage}% Completed`;
    if (status && statusText) status.textContent = statusText;
}

async function startSorting() {
    const maxEmails = document.getElementById('maxEmailsSelect').value;
    const dryRun = document.getElementById('dryRunToggle').checked;
    const removeInbox = document.getElementById('archiveToggle').checked;

    const loader = document.getElementById('loader');
    const emptyState = document.getElementById('emptyState');
    const resultsList = document.getElementById('resultsList');
    const startBtn = document.getElementById('startSortBtn');

    loader.classList.remove('hidden');
    emptyState.classList.add('hidden');
    resultsList.innerHTML = '';
    if (startBtn) startBtn.disabled = true;

    // Simulate smooth live progress bar
    let progress = 10;
    updateProgressBar(progress, 'Connecting to Gmail Inbox...');

    const interval = setInterval(() => {
        if (progress < 90) {
            progress += 10;
            updateProgressBar(progress, `Scanning & Classifying with Gemini AI (${progress}%)...`);
        }
    }, 400);

    try {
        const response = await fetch('/api/run_sorting', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                dry_run: dryRun,
                max_emails: parseInt(maxEmails),
                remove_inbox: removeInbox
            })
        });

        clearInterval(interval);
        updateProgressBar(100, 'Sorting Completed!');

        const data = await response.json();

        if (response.status !== 200) {
            alert(data.error || 'An error occurred during sorting.');
            emptyState.classList.remove('hidden');
            return;
        }

        document.getElementById('resultsCount').textContent = `${data.total_analyzed} emails processed`;

        if (data.results && data.results.length > 0) {
            data.results.forEach(item => {
                const card = document.createElement('div');
                card.className = 'result-card';
                card.innerHTML = `
                    <div class="result-header">
                        <div>
                            <div class="email-subject">${escapeHtml(item.subject)}</div>
                            <div class="email-sender">${escapeHtml(item.sender)}</div>
                        </div>
                        <span class="cat-badge">${escapeHtml(item.assigned_category)}</span>
                    </div>
                    <div class="email-snippet">${escapeHtml(item.snippet)}</div>
                    <div class="help-text mt-3">Action: ${escapeHtml(item.action_taken)}</div>
                `;
                resultsList.appendChild(card);
            });
            loadGmailLabels();
        } else {
            emptyState.classList.remove('hidden');
            emptyState.querySelector('p').textContent = 'No messages found in Inbox.';
        }

    } catch (err) {
        clearInterval(interval);
        console.error(err);
        alert('Network or server error while sorting emails.');
        emptyState.classList.remove('hidden');
    } finally {
        setTimeout(() => {
            loader.classList.add('hidden');
            if (startBtn) startBtn.disabled = false;
        }, 800);
    }
}

async function restoreInbox() {
    if (!confirm("Do you want to restore all archived emails back to your main Gmail Inbox?")) return;

    try {
        const response = await fetch('/api/restore_inbox', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' }
        });
        const data = await response.json();
        if (response.ok && data.status === 'success') {
            alert(data.message || 'All emails restored to Inbox successfully!');
            window.location.reload();
        } else {
            alert(data.error || 'Failed to restore emails.');
        }
    } catch (err) {
        console.error(err);
        alert('Network error while restoring emails.');
    }
}

async function loadGmailLabels() {
    const container = document.getElementById('labelsExplorer');
    if (!container) return;

    try {
        const response = await fetch('/api/list_labels');
        const data = await response.json();

        if (data.labels && data.labels.length > 0) {
            container.innerHTML = '';
            data.labels.forEach(lbl => {
                const item = document.createElement('div');
                item.className = 'label-explorer-item';
                item.innerHTML = `
                    <div>
                        <strong>📂 ${escapeHtml(lbl.name)}</strong>
                        <span class="badge ml-2">${lbl.count} emails</span>
                    </div>
                    <div class="label-explorer-actions">
                        <button class="btn-sm btn-secondary" onclick="openLabelInspector('${escapeHtml(lbl.name)}')">Open</button>
                        <button class="btn-sm btn-danger" onclick="deleteLabel('${escapeHtml(lbl.name)}')">Delete</button>
                    </div>
                `;
                container.appendChild(item);
            });
        } else {
            container.innerHTML = '<p class="help-text">No custom Gmail labels found yet. Click Sort Inbox to create them!</p>';
        }
    } catch (err) {
        console.error(err);
    }
}

async function openLabelInspector(labelName) {
    const modal = document.getElementById('labelEmailsModal');
    const title = document.getElementById('inspectorLabelTitle');
    const list = document.getElementById('inspectorEmailsList');

    title.textContent = `📂 Label: ${labelName}`;
    list.innerHTML = '<div class="spinner"></div><p class="text-center">Loading emails...</p>';
    modal.classList.remove('hidden');

    try {
        const response = await fetch('/api/get_label_emails', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ label_name: labelName })
        });
        const data = await response.json();

        list.innerHTML = '';
        if (data.emails && data.emails.length > 0) {
            data.emails.forEach(item => {
                const card = document.createElement('div');
                card.className = 'result-card';
                card.innerHTML = `
                    <div class="result-header">
                        <div>
                            <div class="email-subject">${escapeHtml(item.subject)}</div>
                            <div class="email-sender">${escapeHtml(item.sender)}</div>
                        </div>
                        <button class="btn-sm btn-danger" onclick="deleteEmail('${item.id}', '${escapeHtml(labelName)}', this)">🗑️ Trash</button>
                    </div>
                    <div class="email-snippet">${escapeHtml(item.snippet)}</div>
                `;
                list.appendChild(card);
            });
        } else {
            list.innerHTML = '<p class="empty-state">No emails found inside this label.</p>';
        }
    } catch (err) {
        console.error(err);
        list.innerHTML = '<p class="text-warning">Failed to fetch emails for this label.</p>';
    }
}

async function deleteLabel(labelName) {
    if (!confirm(`Are you sure you want to delete the Gmail label "${labelName}"?`)) return;

    try {
        const response = await fetch('/api/delete_label', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ label_name: labelName })
        });
        const data = await response.json();
        if (response.ok && data.status === 'success') {
            alert(data.message);
            loadGmailLabels();
        } else {
            alert(data.error || 'Failed to delete label.');
        }
    } catch (err) {
        console.error(err);
        alert('Network error while deleting label.');
    }
}

async function deleteEmail(messageId, folderName, btnElement) {
    if (!confirm('Move this email to Gmail Trash?')) return;

    try {
        const response = await fetch('/api/delete_email', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message_id: messageId, folder_name: folderName })
        });
        const data = await response.json();
        if (response.ok && data.status === 'success') {
            const card = btnElement.closest('.result-card');
            if (card) card.remove();
            alert('Email moved to Trash!');
        } else {
            alert(data.error || 'Failed to delete email.');
        }
    } catch (err) {
        console.error(err);
        alert('Network error while deleting email.');
    }
}

function escapeHtml(str) {
    if (!str) return '';
    return str.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;").replace(/'/g, "&#039;");
}
