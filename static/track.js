// track.js

const statusMessage = document.getElementById('statusMessage');
const detailsSection = document.getElementById('detailsSection');
const detailsEl = document.getElementById('details');
const logsList = document.getElementById('logs-list');
const copyBtn = document.getElementById('copyBtn');

function showStatus(msg, type) {
  statusMessage.textContent = msg;
  statusMessage.className = `alert ${type}`;
  statusMessage.style.display = 'block';
  setTimeout(() => (statusMessage.style.display = 'none'), 4000);
}

async function get_status_details() {
  const complaintId = document.getElementById('complaint_id').value.trim();
  if (!complaintId) return showStatus('Please enter a Complaint ID.', 'error');

  detailsSection.style.display = 'block';
  detailsEl.textContent = 'Fetching complaint details...';
  logsList.innerHTML = '';
  showStatus('Loading details...', 'success');

  try {
    const res = await fetch(`/get_status/${complaintId}`);
    const data = await res.json();

    if (res.ok) {
      detailsEl.textContent =
        `Complaint ID            : ${data.complaint_id}\n` +
        `Submitted On            : ${new Date(data.submitted_at).toLocaleString()}\n\n` +
        `Current Status          : ${data.status}\n` +
        `Assigned Department     : ${data.assigned_to}\n\n` +
        `Urgency                 : ${data.urgency}\n` +
        `Complaint               : ${data.complaint_text}\n\n` +
        `Expected Resolution     : ${data.eta_message}\n` +
        `Escalation Contact      : ${data.escalation_email}`;

      copyBtn.onclick = () => {
        navigator.clipboard.writeText(data.complaint_id);
        showStatus('Complaint ID copied!', 'success');
      };

      logsList.innerHTML = '';
      if (data.logs && data.logs.length > 0) {
        data.logs.forEach((log) => {
          const div = document.createElement('pre');
          div.className = 'log-entry';
          div.textContent =
            `Status   : ${log.status}\n` +
            `Assigned : ${log.assigned_to}\n` +
            `Time     : ${new Date(log.timestamp).toLocaleString()}`;
          logsList.appendChild(div);
        });
      } else logsList.innerHTML = '<p>No status history available.</p>';

      showStatus('Complaint details loaded.', 'success');
    } else showStatus(data.error || 'Complaint not found.', 'error');
  } catch (err) {
    showStatus('Error: ' + err.message, 'error');
  }
}

// Auto-track if ?id= present
document.addEventListener('DOMContentLoaded', () => {
  const params = new URLSearchParams(window.location.search);
  const id = params.get('id');
  if (id) {
    document.getElementById('complaint_id').value = id;
    get_status_details();
  }
});

document.addEventListener("DOMContentLoaded", () => {
  document.body.classList.add("fade-in");
});