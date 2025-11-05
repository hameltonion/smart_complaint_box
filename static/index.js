// index.js

const complaintForm = document.getElementById('complaintForm');
const complaintTextarea = document.getElementById('complaintText');
const predictBtn = document.getElementById('predictBtn');
const predictionResult = document.getElementById('predictionResult');
const predictionOutput = document.getElementById('predictionOutput');
const submitComplaintBtn = document.getElementById('submitComplaintBtn');
const confirmationSection = document.getElementById('confirmationSection');
const finalDetailsOutput = document.getElementById('finalDetailsOutput');
const statusMessage = document.getElementById('statusMessage');

let predictedData = null;
window.complaintId = null;

function showStatus(message, type) {
  statusMessage.textContent = message;
  statusMessage.className = `alert ${type}`;
  statusMessage.style.display = 'block';
  setTimeout(() => (statusMessage.style.display = 'none'), 4000);
}

// Step 1: Analyze complaint
complaintForm.addEventListener('submit', async (e) => {
  e.preventDefault();
  const text = complaintTextarea.value.trim();
  if (!text) return showStatus('Please enter your complaint.', 'error');

  predictBtn.disabled = true;
  showStatus('Analyzing complaint...', 'success');
  predictionResult.style.display = 'none';

  try {
    const res = await fetch('/predict', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ complaint_text: text }),
    });
    const data = await res.json();

    if (res.ok) {
      predictedData = data;
      predictionOutput.textContent =
        `Assigned Department : ${data.assigned_to}\n` +
        `Estimated Resolution : ${data.eta_message}\n` +
        `Escalation Contact  : ${data.escalation_email || 'N/A'}`;
      predictionResult.style.display = 'block';
      showStatus('Analysis complete! Please confirm to submit.', 'success');
    } else showStatus(data.error || 'Failed to analyze.', 'error');
  } catch (err) {
    showStatus('Error: ' + err.message, 'error');
  } finally {
    predictBtn.disabled = false;
  }
});

// Step 2: Confirm submission
submitComplaintBtn.addEventListener('click', async () => {
  if (!predictedData) return;

  submitComplaintBtn.disabled = true;
  showStatus('Submitting complaint...', 'success');

  try {
    const res = await fetch('/submit', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        complaint_text: complaintTextarea.value,
        category: predictedData.category,
        subcategory: predictedData.subcategory,
        urgency: predictedData.urgency,
        assigned_to: predictedData.assigned_to,
      }),
    });
    const result = await res.json();

    if (res.ok) {
      window.complaintId = result.complaint_id;
      finalDetailsOutput.textContent =
        `Complaint ID            : ${result.complaint_id}\n` +
        `Submitted On            : ${new Date().toLocaleString()}\n\n` +
        `Status                  : Pending\n` +
        `Assigned Department     : ${predictedData.assigned_to}\n\n` +
        `Resolution ETA          : ${predictedData.eta_message}\n` +
        `Escalation Contact      : ${predictedData.escalation_email}`;

      predictionResult.style.display = 'none';
      confirmationSection.style.display = 'block';
      showStatus('Complaint submitted successfully!', 'success');
    } else showStatus(result.error || 'Submission failed.', 'error');
  } catch (err) {
    showStatus('Error: ' + err.message, 'error');
  } finally {
    submitComplaintBtn.disabled = false;
  }
});

document.addEventListener("DOMContentLoaded", () => {
  document.body.classList.add("fade-in");
});