import re
import json

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

def preprocess(text):
    text = text.lower()

    text = re.sub(r"[^a-zA-Z0-9\s]", " ", text)

    text = re.sub(r"\s+", " ", text).strip()

    return text

# Preprocess intents into keyword sets
intent_keywords = {}
for intent_name, intent_text in INTENTS.items():
    keywords = set(preprocess(intent_text).split())
    intent_keywords[intent_name] = keywords

def calculate_confidence(matched_count):
    """
    Calculate confidence based on keyword match count.
    """
    if matched_count == 0:
        return 0.0
    
    confidence = min(0.99, matched_count * 0.25)
    return round(confidence, 2)


def classify_intent(user_text):

    cleaned_text = preprocess(user_text)

    # Empty input edge case
    if not cleaned_text:
        return {
            "intent": "payroll",
            "confidence": 0.50
        }

    user_words = set(cleaned_text.split())
    
    best_intent = "payroll"
    best_matched = 0
    
    for intent_name, keywords in intent_keywords.items():
        matched = len(user_words & keywords)
        
        if matched > best_matched:
            best_matched = matched
            best_intent = intent_name
    
    confidence = calculate_confidence(best_matched)

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