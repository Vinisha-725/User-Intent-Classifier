import re
import json

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

INTENTS = {
    "leave": """
        leave annual leave casual leave sick leave medical leave
        vacation holiday day off leave balance leave request
        maternity leave paternity leave emergency leave
        absent due to illness take leave paid leave unpaid leave
    """,

    "payroll": """
        salary payroll payslip pay slip wages payment
        bonus tax deduction reimbursement allowance
        overtime salary credit monthly salary
        compensation income earnings payroll money
    """,

    "employee_onboarding": """
        onboarding joining new employee induction orientation
        offer letter joining formalities employee registration
        first day training company policies
        employee account setup id card
        access card documents verification
    """,

    "loan": """
        loan salary advance advance payment borrow money
        repayment installment emi interest rate
        company loan personal loan loan application
        loan balance outstanding loan no money
    """,

    "attendance": """
        attendance biometric check in check out
        clock in clock out timesheet working hours
        absent present late coming
        attendance record punch in punch out
        missed attendance
    """
}

intent_names = list(INTENTS.keys())
intent_texts = list(INTENTS.values())

vectorizer = TfidfVectorizer()

intent_vectors = vectorizer.fit_transform(intent_texts)

def preprocess(text):
    text = text.lower()

    text = re.sub(r"[^a-zA-Z0-9\s]", " ", text)

    text = re.sub(r"\s+", " ", text).strip()

    return text

def calculate_confidence(best_score):
    """
    Convert cosine similarity into a user-friendly confidence score.
    """

    confidence = 0.5 + (best_score * 0.5)

    confidence = max(0.50, min(confidence, 0.99))

    return round(confidence, 2)


def classify_intent(user_text):

    cleaned_text = preprocess(user_text)

    # Empty input edge case
    if not cleaned_text:
        return {
            "intent": "payroll",
            "confidence": 0.50
        }

    query_vector = vectorizer.transform([cleaned_text])

    similarities = cosine_similarity(
        query_vector,
        intent_vectors
    )[0]

    best_index = similarities.argmax()

    best_intent = intent_names[best_index]

    best_score = similarities[best_index]

    confidence = calculate_confidence(best_score)

    return {
        "intent": best_intent,
        "confidence": confidence
    }

print("=" * 50)
print("HR INTENT CLASSIFIER")
print("=" * 50)
print("Type 'exit' to quit.\n")

while True:

    user_input = input("Enter request: ")

    if user_input.lower() == "exit":
        print("Thank You!")
        break

    result = classify_intent(user_input)

    print(json.dumps(result, indent=4))
    print()