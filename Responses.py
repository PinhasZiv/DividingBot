from datetime import datetime

def sample_responses(input_text):
    message_text = str(input_text).lower()

    if message_text in ('הוסף הוצאה'):
        return 'סבבה אחי'
    return 'מה אתה סתום??'