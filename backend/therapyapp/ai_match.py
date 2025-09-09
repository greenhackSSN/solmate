import requests

def get_ai_suggested_plan(patient):
    """
    Calls Vedha's AI service to get a suggested therapy plan for the patient.
    Replace URL and payload once Vedha provides her API.
    """
    url = "http://vedha-api-url/plan_suggestion"  # placeholder
    payload = {
        "patient_id": patient.id,
        "age": patient.age,
        "gender": patient.gender,
        "history": patient.history if hasattr(patient, 'history') else ""
    }

    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": "Failed to fetch plan suggestion"}
    except Exception as e:
        return {"error": str(e)}
