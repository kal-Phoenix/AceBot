# Exam Questions - Easy JSON Format

## How to Add Questions

Simply edit the `sample-exams.json` file! No coding required.

### JSON Structure

```json
[
  {
    "title": "Exam Title",
    "description": "Brief description",
    "exam_type": "past",           // past, mock, or model
    "subject": "English",           // Subject name
    "stream": "natural",            // natural or social
    "year": 2017,                   // Year (for past exams)
    "duration_minutes": 45,         // Time limit
    "passing_score": 70,            // Minimum score to pass
    "questions": [
      {
        "question_text": "Your question here?",
        "option_a": "First option",
        "option_b": "Second option",
        "option_c": "Third option",
        "option_d": "Fourth option",
        "correct_answer": "B",      // A, B, C, or D
        "explanation": "Why this answer is correct",
        "points": 1                 // Points for this question
      }
    ]
  }
]
```

## Quick Start

### 1. Copy the Template

```json
{
  "title": "Math Basics 2015",
  "description": "Test your math fundamentals",
  "exam_type": "past",
  "subject": "Maths",
  "stream": "natural",
  "year": 2015,
  "duration_minutes": 60,
  "passing_score": 75,
  "questions": [
    {
      "question_text": "What is 5 + 3?",
      "option_a": "6",
      "option_b": "7",
      "option_c": "8",
      "option_d": "9",
      "correct_answer": "C",
      "explanation": "5 + 3 = 8. Basic addition.",
      "points": 1
    }
  ]
}
```

### 2. Add to Array

Just add your exam object to the array in `sample-exams.json`.

### 3. Restart Server

```bash
cd server
npm start
```

That's it! Your questions are now live.

## Field Descriptions

| Field | Required | Description | Example |
|-------|----------|-------------|---------|
| `title` | ✅ | Exam name | "English Grammar 2017" |
| `description` | ✅ | Short description | "Test your grammar skills" |
| `exam_type` | ✅ | Type of exam | "past", "mock", or "model" |
| `subject` | ✅ | Subject name | "English", "Maths", "Chemistry" |
| `stream` | ✅ | Learning stream | "natural" or "social" |
| `year` | ⚠️ | Year (for past exams) | 2017, 2016, 2015... |
| `duration_minutes` | ✅ | Time limit | 45, 60, 90 |
| `passing_score` | ✅ | Pass percentage | 70, 75, 80 |
| `questions` | ✅ | Array of questions | See below |

### Question Fields

| Field | Required | Description | Example |
|-------|----------|-------------|---------|
| `question_text` | ✅ | The question | "What is the capital of France?" |
| `option_a` | ✅ | First choice | "London" |
| `option_b` | ✅ | Second choice | "Paris" |
| `option_c` | ✅ | Third choice | "Berlin" |
| `option_d` | ✅ | Fourth choice | "Madrid" |
| `correct_answer` | ✅ | Right answer | "A", "B", "C", or "D" |
| `explanation` | ✅ | Why it's correct | "Paris is the capital of France" |
| `points` | ✅ | Points awarded | 1, 2, 3... |

## Subjects by Stream

### Natural Science
- English
- Maths
- SAT
- Chemistry
- Biology
- Physics

### Social Science
- English
- Maths
- SAT
- History
- Geography
- Economics

## Tips

### ✅ DO:
- Use clear, concise questions
- Provide detailed explanations
- Check spelling and grammar
- Test your exams after adding them
- Keep consistent formatting

### ❌ DON'T:
- Use special characters that break JSON (like unescaped quotes)
- Forget commas between objects
- Mix up correct_answer letters
- Leave fields empty

## Examples

### Simple Question
```json
{
  "question_text": "What is 2 + 2?",
  "option_a": "3",
  "option_b": "4",
  "option_c": "5",
  "option_d": "6",
  "correct_answer": "B",
  "explanation": "2 + 2 equals 4. Basic arithmetic.",
  "points": 1
}
```

### Complex Question
```json
{
  "question_text": "Which of the following best describes photosynthesis?",
  "option_a": "The process by which plants make food using sunlight",
  "option_b": "The process by which plants absorb water",
  "option_c": "The process by which plants release oxygen",
  "option_d": "The process by which plants grow roots",
  "correct_answer": "A",
  "explanation": "Photosynthesis is the process where plants convert light energy into chemical energy (food) using chlorophyll, water, and carbon dioxide.",
  "points": 2
}
```

## Validation

Before adding questions, make sure:
1. ✅ JSON is valid (use a JSON validator)
2. ✅ All required fields are present
3. ✅ Correct answer matches one of the options
4. ✅ Stream matches subject availability
5. ✅ Year is between 2000-2017 for past exams

## Need Help?

- Check `sample-exams.json` for examples
- Use a JSON validator: https://jsonlint.com
- Test in the app after adding

---

**That's it!** No programming knowledge needed. Just edit the JSON file and your questions are ready to use! 🎉
