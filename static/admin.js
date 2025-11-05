// admin.js

const authKeyInput = document.getElementById('auth-key');
const verifyBtn = document.getElementById('verifyBtn');
const authMsg = document.getElementById('auth-message');
const statusMsg = document.getElementById('status-message');
const panel = document.getElementById('admin-panel-content');
const tableBody = document.getElementById('complaints-table');

let modifyKey = null;

function showAlert(el, message, type) {
  el.textContent = message;
  el.className = `alert ${type}`;
  el.style.display = 'block';
  setTimeout(() => (el.style.display = 'none'), 4000);
}

verifyBtn.addEventListener('click', async () => {
  const key = authKeyInput.value.trim();
  if (!key) return showAlert(authMsg, 'Please enter key.', 'error');

  showAlert(authMsg, 'Verifying...', 'success');
  try {
    const res = await fetch('/verify_key', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ key }),
    });
    const data = await res.json();

    if (res.ok && data.success) {
      panel.style.display = 'block';
      showAlert(authMsg, 'Access granted.', 'success');
      modifyKey = data.permission_level === 'read-write' ? key : null;
      loadComplaints();
    } else showAlert(authMsg, data.error || 'Invalid key.', 'error');
  } catch (err) {
    showAlert(authMsg, err.message, 'error');
  }
});

async function loadComplaints() {
  try {
    const res = await fetch('/all_complaints');
    const data = await res.json();

    if (res.ok) {
      tableBody.innerHTML = '';
      data.forEach((c) => {
        const row = document.createElement('tr');
        row.innerHTML = `
          <td>${c.complaint_id}</td>
          <td>${new Date(c.created_at).toLocaleString()}</td>
          <td>${c.user_input}</td>
          <td>
            <select ${!modifyKey ? 'disabled' : ''}>
              <option ${c.status === 'Pending' ? 'selected' : ''}>Pending</option>
              <option ${c.status === 'In Progress' ? 'selected' : ''}>In Progress</option>
              <option ${c.status === 'Resolved' ? 'selected' : ''}>Resolved</option>
            </select>
          </td>
          <td><input type="text" value="${c.assigned_to}" ${!modifyKey ? 'disabled' : ''}></td>
          <td>
            <button ${!modifyKey ? 'disabled' : ''} onclick="updateComplaint('${c.complaint_id}', this)">Update</button>
            <button ${!modifyKey ? 'disabled' : ''} onclick="deleteComplaint('${c.complaint_id}', this)">Delete</button>
          </td>`;
        tableBody.appendChild(row);
      });
    } else showAlert(statusMsg, data.error || 'Failed to load.', 'error');
  } catch (err) {
    showAlert(statusMsg, err.message, 'error');
  }
}

async function updateComplaint(id, btn) {
  const row = btn.closest('tr');
  const status = row.querySelector('select').value;
  const assignedTo = row.querySelector('input').value;

  try {
    const res = await fetch('/update_complaint', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ complaint_id: id, modify_key: modifyKey, status, assigned_to: assignedTo }),
    });
    const data = await res.json();
    if (res.ok && data.success) showAlert(statusMsg, data.message, 'success');
    else showAlert(statusMsg, data.error || 'Update failed.', 'error');
  } catch (err) {
    showAlert(statusMsg, err.message, 'error');
  }
}

async function deleteComplaint(id, btn) {
  if (!confirm('Are you sure you want to delete this complaint?')) return;

  try {
    const res = await fetch('/delete_complaint', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ complaint_id: id, modify_key: modifyKey }),
    });
    const data = await res.json();
    if (res.ok && data.success) {
      btn.closest('tr').remove();
      showAlert(statusMsg, data.message, 'success');
    } else showAlert(statusMsg, data.error || 'Delete failed.', 'error');
  } catch (err) {
    showAlert(statusMsg, err.message, 'error');
  }
}

document.addEventListener("DOMContentLoaded", () => {
  document.body.classList.add("fade-in");
});