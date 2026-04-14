import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

/**
 * Load exams from JSON files
 * This makes it easy to manage exam questions without touching code
 */
export function loadExamsFromJSON() {
  try {
    const examsPath = path.join(__dirname, '../data/exams/sample-exams.json');
    const fileContent = fs.readFileSync(examsPath, 'utf-8');
    const exams = JSON.parse(fileContent);
    
    console.log(`✅ Loaded ${exams.length} exams from JSON`);
    return exams;
  } catch (error) {
    console.error('❌ Error loading exams from JSON:', error.message);
    return [];
  }
}

/**
 * Get exams filtered by criteria
 */
export function getFilteredExams(allExams, filters = {}) {
  let filtered = [...allExams];

  if (filters.exam_type) {
    filtered = filtered.filter(exam => exam.exam_type === filters.exam_type);
  }

  if (filters.subject) {
    filtered = filtered.filter(exam => exam.subject === filters.subject);
  }

  if (filters.stream) {
    filtered = filtered.filter(exam => exam.stream === filters.stream);
  }

  if (filters.year) {
    filtered = filtered.filter(exam => exam.year === parseInt(filters.year));
  }

  return filtered;
}

/**
 * Get a single exam by ID (index in array)
 */
export function getExamById(allExams, examId) {
  const index = parseInt(examId);
  return allExams[index] || null;
}

/**
 * Get questions for an exam
 */
export function getQuestionsForExam(exam) {
  if (!exam || !exam.questions) return [];
  
  return exam.questions.map((q, index) => ({
    question_id: `${exam.title}-q${index + 1}`,
    question_number: index + 1,
    question_text: q.question_text,
    options: {
      a: q.option_a,
      b: q.option_b,
      c: q.option_c,
      d: q.option_d,
    },
    correct_answer: q.correct_answer,
    explanation: q.explanation,
    points: q.points || 1,
    has_image: q.has_image || false,
    image_url: q.image_url || null,
  }));
}
