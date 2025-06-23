'''from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# 🧠 Fake database with full info (including validation fields)
fake_db = {
    "12345": {
        "applicationId": "APP123",
        "dob": "01-01-2000",
        "domicile": "Uttar Pradesh",
        "status": "Application Approved",
        "schedule": "15 June 2025 at 10:00 AM",
        "center": "KNIT Sultanpur",
        "admit_card": "https://example.com/admit/12345",
        "result": "Not declared yet",
        "fee": "Paid on 10 May 2025",
        "documents": "Photo, Signature, ID proof"
    },
    "54321": {
        "applicationId": "APP543",
        "dob": "15-02-2001",
        "domicile": "Delhi",
        "status": "Pending Verification",
        "schedule": "20 June 2025 at 2:00 PM",
        "center": "Lucknow Exam Center",
        "admit_card": "https://example.com/admit/54321",
        "result": "Not declared yet",
        "fee": "Unpaid",
        "documents": "Signature missing"
    }
}

@app.route('/api/verify-applicant', methods=['POST'])
def verify_applicant():
    data = request.get_json()
    otr = data.get("otr")
    app_id = data.get("applicationId")
    dob = data.get("dob")
    domicile = data.get("domicile")

    print("Received input:", data)

    if not (otr and app_id and dob and domicile):
        return jsonify({"success": False, "error": "Missing fields"}), 400

    record = fake_db.get(otr)

    if not record:
        return jsonify({"success": False, "error": "OTR not found"}), 404

    if (
        record["applicationId"] == app_id
        and record["dob"] == dob
        and record["domicile"].lower() == domicile.lower()
    ):
        return jsonify({"success": True, "data": record})
    else:
        return jsonify({
            "success": False,
            "error": "One or more details do not match our records"
        }), 401


if __name__ == '__main__':
    print("🔥 Flask backend running on http://localhost:5000")
    app.run(debug=True, port=5000)'''

from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# 🧠 Fake database (simulating a backend data store)
fake_db = {
    "12345": {
        "applicationId": "APP123",
        "dob": "01-01-2000",
        "domicile": "Uttar Pradesh",
        "status": "Application Approved",
        "schedule": "15 June 2025 at 10:00 AM",
        "center": "KNIT Sultanpur",
        "admit_card": "https://example.com/admit/12345",
        "result": "Not declared yet",
        "fee": "Paid on 10 May 2025",
        "documents": "Photo, Signature, ID proof"
    },
    "54321": {
        "applicationId": "APP543",
        "dob": "15-02-2001",
        "domicile": "Delhi",
        "status": "Pending Verification",
        "schedule": "20 June 2025 at 2:00 PM",
        "center": "Lucknow Exam Center",
        "admit_card": "https://example.com/admit/54321",
        "result": "Not declared yet",
        "fee": "Unpaid",
        "documents": "Signature missing"
    }
}

# 📦 Data access functions (easily swappable with DB calls later)
def get_applicant_record_by_otr(otr):
    return fake_db.get(otr)

def validate_application_id(record, application_id):
    return record.get("applicationId") == application_id

def validate_dob(record, dob):
    return record.get("dob") == dob

def validate_domicile(record, domicile):
    return record.get("domicile", "").lower() == domicile.lower()


@app.route('/api/verify-applicant', methods=['POST'])
def verify_applicant():
    data = request.get_json()
    otr = data.get("otr")
    app_id = data.get("applicationId")
    dob = data.get("dob")
    domicile = data.get("domicile")

    print("📩 Received input:", data)

    if not (otr and app_id and dob and domicile):
        return jsonify({"success": False, "error": "Missing fields"}), 400

    record = get_applicant_record_by_otr(otr)

    if not record:
        return jsonify({"success": False, "error": "OTR not found"}), 404

    if (
        validate_application_id(record, app_id)
        and validate_dob(record, dob)
        and validate_domicile(record, domicile)
    ):
        return jsonify({"success": True, "data": record})
    else:
        return jsonify({
            "success": False,
            "error": "One or more details do not match our records"
        }), 401


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)



