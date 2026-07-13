# HR Intent Classifier

A simple keyword-based intent classifier for HR-related requests.

## Features

- Classifies user input into 5 HR intent categories:
  - **leave**: Leave requests, vacation, sick leave
  - **payroll**: Salary, payslips, bonuses, tax
  - **employee_onboarding**: New employee induction, orientation
  - **loan**: Salary advances, loan applications
  - **attendance**: Check-in/out, timesheet, working hours

## How It Works

The classifier uses keyword matching:
- Extracts keywords from user input
- Matches against predefined intent keywords
- Returns the best matching intent with confidence score
- Confidence: 0.0 (no matches) to 0.99 (4+ matches)

## Usage

Run the classifier:
```bash
python classifier.py
```

Enter your HR request and get the classified intent with confidence score.

## Example

```
Enter request: i need to borrow money
{
    "intent": "loan",
    "confidence": 0.25
}
```
