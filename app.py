from flask import Flask, request, jsonify, render_template, send_from_directory, Response
import cv2
import numpy as np
import os
import face_utils
import database

app = Flask(__name__, static_folder='static', template_folder='templates')

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/train", methods=["POST"])
def train():
    try:
        success = face_utils.train_system("dataset")
        if success:
            return jsonify({"message": "Training complete. Embeddings generated successfully!"}), 200
        else:
            return jsonify({"message": "Dataset folder is empty or improperly structured."}), 400
    except Exception as e:
        return jsonify({"message": f"Error occurred during training: {str(e)}"}), 500

@app.route("/api/recognize", methods=["POST"])
def recognize():
    file = request.files.get("image")
    if not file:
        return jsonify({"message": "No image uploaded"}), 400
        
    try:
        # Convert image bytes to numpy array
        img_array = np.frombuffer(file.read(), np.uint8)
        image = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
        
        if image is None:
            return jsonify({"message": "Invalid image format"}), 400
            
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Recognize face
        result = face_utils.recognize_face(image)
        
        # Unpack result
        if isinstance(result, tuple):
            name, dist_or_err = result
        else:
            return jsonify({"message": "Unexpected error"}), 500
        
        if name is None:
            return jsonify({"message": dist_or_err}), 400
            
        if name == "Unknown":
            return jsonify({"message": "Unknown person detected. Similarity check failed.", "similarity_dist": float(dist_or_err)}), 404
            
        # Valid person
        marked = database.mark_attendance(name)
        status = "Attendance marked successfully" if marked else "Attendance already marked for today"
        
        display_name = name.split('_')[0]
        
        return jsonify({
            "message": status,
            "student": display_name,
            "distance": float(dist_or_err)
        }), 200
    except Exception as e:
        return jsonify({"message": f"Server Error: {str(e)}"}), 500

@app.route("/api/attendance", methods=["GET"])
def get_records():
    records = database.get_attendance()
    return jsonify({"records": records}), 200

@app.route("/api/download_csv", methods=["GET"])
def download_csv():
    records = database.get_attendance()
    
    def generate():
        yield 'S.No,Register Number,Enroll Number,Student Name,Date,Time,Status\n'
        for i, row in enumerate(records, 1):
            yield f"{i},{row['register_number']},{row['enroll_number']},{row['name']},{row['date']},{row['time']},{row['status']}\n"
            
    return Response(generate(), mimetype='text/csv', headers={'Content-Disposition': 'attachment; filename=Attendance_Report.csv'})

@app.route("/api/clear_attendance", methods=["DELETE"])
def clear_attendance():
    try:
        database.clear_attendance()
        return jsonify({"message": "Attendance records cleared for the next day!"}), 200
    except Exception as e:
        return jsonify({"message": f"Server Error: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
