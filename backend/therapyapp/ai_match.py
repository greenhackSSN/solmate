from usermgmt.models import CustomUser
import random

def match_patient_to_therapist(patient, therapists):
    """
    Temporary placeholder until Vedha provides AI API.
    Just randomly selects a therapist from the list.
    """
    if not therapists:
        return None
    return random.choice(therapists)
