const video = document.getElementById('webcam');
const canvas = document.getElementById('overlay');
const resultBox = document.getElementById('result-box');
const tbody = document.getElementById('attendance-body');

// START WEBCAM
async function startWebcam() {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: true });
        video.srcObject = stream;
    } catch (err) {
        console.error("Error accessing webcam:", err);
        showResult("Camera access denied or device not found.", "error");
    }
}

// CAPTURE & RECOGNIZE
async function captureAndRecognize() {
    const btn = document.getElementById('scan-btn');
    btn.innerText = "Scanning Face...";
    btn.disabled = true;

    // UI Feedback: Show scanner line
    document.querySelector('.video-wrapper').classList.add('scannable');

    // Draw video frame to canvas
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    canvas.getContext('2d').drawImage(video, 0, 0, canvas.width, canvas.height);

    // Convert to Blob
    canvas.toBlob(async (blob) => {
        const formData = new FormData();
        formData.append("image", blob, "capture.jpg");

        try {
            const response = await fetch('/api/recognize', {
                method: 'POST',
                body: formData
            });
            const data = await response.json();

            if (response.ok) {
                showResult(`Welcome, ${data.student}! ✓<br><small>${data.message}</small>`, "success");
                fetchRecords(); // Refresh table
            } else {
                showResult(`Recognition Failed: ${data.message}`, "error");
            }
        } catch (err) {
            showResult("Server error. Ensure backend is running.", "error");
            console.error(err);
        } finally {
            btn.innerText = "Capture & Mark Attendance";
            btn.disabled = false;
            document.querySelector('.video-wrapper').classList.remove('scannable');
            // Hide result after 5s
            setTimeout(() => { resultBox.classList.add('hidden'); }, 5000);
        }
    }, 'image/jpeg');
}

// RESULT UI
function showResult(msg, type) {
    resultBox.classList.remove('hidden', 'result-success', 'result-error');
    resultBox.innerHTML = msg;
    resultBox.classList.add(type === 'success' ? 'result-success' : 'result-error');
}

// TRAIN MODEL
async function trainModel() {
    const btn = document.getElementById('train-btn');
    btn.innerText = "Training...";
    btn.disabled = true;

    try {
        const response = await fetch('/api/train', { method: 'POST' });
        const data = await response.json();
        alert(data.message);
    } catch (e) {
        alert("Training failed due to server error");
    } finally {
        btn.innerText = "Model Training";
        btn.disabled = false;
    }
}

// FETCH ATTENDANCE RECORDS
async function fetchRecords() {
    try {
        const response = await fetch('/api/attendance');
        const data = await response.json();

        tbody.innerHTML = '';
        if (data.records && data.records.length > 0) {
            data.records.forEach((record, index) => {
                const tr = document.createElement('tr');
                let badgeClass = record.status.includes('Already') ? 'status-already' : 'status-present';
                let statusLabel = record.status.includes('Already') ? 'Already Marked' : 'Present';

                tr.innerHTML = `
                    <td>${index + 1}</td>
                    <td>${record.register_number}</td>
                    <td>${record.enroll_number}</td>
                    <td><strong>${record.name}</strong></td>
                    <td>${record.date}</td>
                    <td>${record.time}</td>
                    <td><span class="status-badge ${badgeClass}">${statusLabel}</span></td>
                `;
                tbody.appendChild(tr);
            });
        } else {
            tbody.innerHTML = '<tr><td colspan="7" style="text-align:center;">No attendance records found for today.</td></tr>';
        }
    } catch (e) {
        console.error("Error fetching records", e);
    }
}

// ON LOAD
window.onload = () => {
    startWebcam();
    fetchRecords();
};

// CLEAR ATTENDANCE RECORDS
async function clearAttendance() {
    if (!confirm("Are you sure you want to delete all attendance records for the next day?")) return;

    try {
        const response = await fetch('/api/clear_attendance', { method: 'DELETE' });
        const data = await response.json();
        alert(data.message);
        fetchRecords(); // Refresh table
    } catch (e) {
        alert("Failed to clear records.");
        console.error(e);
    }
}
