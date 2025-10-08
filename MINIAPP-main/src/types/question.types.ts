export type Stream = 'Natural' | 'Social';

export type NaturalSubject = 'English' | 'Maths' | 'SAT' | 'Chemistry' | 'Biology' | 'Physics';
export type SocialSubject = 'English' | 'Maths' | 'SAT' | 'History' | 'Geography' | 'Economics';

export type Subject = NaturalSubject | SocialSubject;

export type Grade = 9 | 10 | 11 | 12;

export type Difficulty = 'easy' | 'medium' | 'hard';

export interface QuestionOption {
  text: string;
  image?: string;
}

export interface Question {
  id: string;
  stream: Stream;
  subject: Subject;
  grade: Grade;
  topic: string;
  year?: number;
  difficulty: Difficulty;
  questionText: string;
  questionImage?: string;
  options: QuestionOption[];
  correctAnswer: number;
  hint: string;
  explanation: string;
}

export interface UserAnswer {
  questionId: string;
  selectedAnswer: number | null;
  isCorrect: boolean;
  usedHint: boolean;
  isFlagged: boolean;
  timeSpent: number;
}

export interface ExamConfig {
  stream: Stream;
  subject: Subject;
  grade: Grade;
  year: number;
  timeLimitSeconds: number;
  totalQuestions: number;
}

export interface PracticeConfig {
  stream: Stream;
  subject: Subject;
  grade: Grade;
  topics?: string[];
  difficulty?: Difficulty | 'mixed';
  isPastExam: boolean;
  year?: number;
}

export const NATURAL_SUBJECTS: NaturalSubject[] = [
  'English',
  'Maths',
  'SAT',
  'Chemistry',
  'Biology',
  'Physics',
];

export const SOCIAL_SUBJECTS: SocialSubject[] = [
  'English',
  'Maths',
  'SAT',
  'History',
  'Geography',
  'Economics',
];

export const GRADES: Grade[] = [9, 10, 11, 12];

export const EXAM_YEARS = [2024, 2023, 2022, 2021, 2020];
