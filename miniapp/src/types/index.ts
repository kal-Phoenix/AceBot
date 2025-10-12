// Telegram Types
export interface TelegramUser {
  id: number;
  first_name: string;
  last_name?: string;
  username?: string;
  photo_url?: string;
  language_code?: string;
}

// User Types
export interface UserStats {
  total_exams_taken: number;
  total_practice_sessions: number;
  average_score: number;
  best_subject: string | null;
  weakest_subject: string | null;
  total_time_spent: number;
}

export interface User {
  id: string;
  telegram_id?: string;
  username?: string;
  full_name: string;
  profile_picture?: string | null;
  created_at?: string;
  stream?: 'natural' | 'social' | null;
  stats?: UserStats;
}

// Exam Types
export type ExamType = 'past' | 'mock' | 'model';
export type ExamMode = 'practice' | 'exam';
export type Stream = 'natural' | 'social';
export type OrganizationType = 'year' | 'topic';

export interface Exam {
  _id: string;
  title: string;
  description?: string;
  exam_type: ExamType;
  subject: string;
  stream: Stream;
  year?: number;
  topic?: string;
  duration_minutes: number;
  passing_score: number;
  total_questions: number;
  difficulty?: string;
  created_at?: string;
}

export interface Question {
  question_id: string;
  question_number: number;
  question_text: string;
  option_a: string;
  option_b: string;
  option_c: string;
  option_d: string;
  correct_answer: 'A' | 'B' | 'C' | 'D';
  explanation?: string;
  points: number;
  has_image?: boolean;
  image_url?: string | null;
}

export interface Answer {
  question_id: string;
  question_number: number;
  selected_answer: 'A' | 'B' | 'C' | 'D';
  correct_answer: 'A' | 'B' | 'C' | 'D';
  is_correct: boolean;
  points_earned: number;
  answered_at: string;
}

export interface ExamAttempt {
  _id: string;
  user_id: string;
  exam_id: string;
  exam_title: string;
  exam_type: ExamType;
  subject: string;
  mode: ExamMode;
  started_at: string;
  completed_at?: string | null;
  score?: number | null;
  total_points?: number | null;
  max_points: number;
  status: 'in_progress' | 'completed' | 'abandoned';
  time_spent_seconds?: number | null;
  answers: Answer[];
}

// API Response Types
export interface AuthResponse {
  token: string;
  user: User;
}

export interface ApiError {
  error: string;
  message?: string;
  code?: number;
}

// Page Types
export type PageType = 
  | 'welcome' 
  | 'stream-selection' 
  | 'dashboard' 
  | 'organization-selection'
  | 'subject-selection'
  | 'year-selection'
  | 'exam-list' 
  | 'mode-selection'
  | 'exam' 
  | 'results' 
  | 'progress' 
  | 'settings';
