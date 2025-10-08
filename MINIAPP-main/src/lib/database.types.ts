export type Json =
  | string
  | number
  | boolean
  | null
  | { [key: string]: Json | undefined }
  | Json[]

export interface Database {
  public: {
    Tables: {
      users: {
        Row: {
          id: string
          telegram_user_id: number
          username: string
          first_name: string | null
          last_name: string | null
          total_exams_taken: number
          total_practice_questions: number
          overall_accuracy: number
          created_at: string
          updated_at: string
        }
        Insert: {
          id?: string
          telegram_user_id: number
          username: string
          first_name?: string | null
          last_name?: string | null
          total_exams_taken?: number
          total_practice_questions?: number
          overall_accuracy?: number
          created_at?: string
          updated_at?: string
        }
        Update: {
          id?: string
          telegram_user_id?: number
          username?: string
          first_name?: string | null
          last_name?: string | null
          total_exams_taken?: number
          total_practice_questions?: number
          overall_accuracy?: number
          created_at?: string
          updated_at?: string
        }
      }
      exam_attempts: {
        Row: {
          id: string
          user_id: string
          stream: 'Natural' | 'Social'
          subject: string
          grade: number
          year: number
          total_questions: number
          correct_answers: number
          accuracy: number
          time_taken_seconds: number
          time_limit_seconds: number
          is_first_attempt: boolean
          answers: Json
          created_at: string
        }
        Insert: {
          id?: string
          user_id: string
          stream: 'Natural' | 'Social'
          subject: string
          grade: number
          year: number
          total_questions: number
          correct_answers: number
          accuracy: number
          time_taken_seconds: number
          time_limit_seconds: number
          is_first_attempt?: boolean
          answers: Json
          created_at?: string
        }
        Update: {
          id?: string
          user_id?: string
          stream?: 'Natural' | 'Social'
          subject?: string
          grade?: number
          year?: number
          total_questions?: number
          correct_answers?: number
          accuracy?: number
          time_taken_seconds?: number
          time_limit_seconds?: number
          is_first_attempt?: boolean
          answers?: Json
          created_at?: string
        }
      }
      practice_sessions: {
        Row: {
          id: string
          user_id: string
          stream: 'Natural' | 'Social'
          subject: string
          grade: number
          difficulty: 'easy' | 'medium' | 'hard' | 'mixed' | null
          questions_answered: number
          correct_answers: number
          accuracy: number
          topics: string[] | null
          created_at: string
        }
        Insert: {
          id?: string
          user_id: string
          stream: 'Natural' | 'Social'
          subject: string
          grade: number
          difficulty?: 'easy' | 'medium' | 'hard' | 'mixed' | null
          questions_answered?: number
          correct_answers?: number
          accuracy?: number
          topics?: string[] | null
          created_at?: string
        }
        Update: {
          id?: string
          user_id?: string
          stream?: 'Natural' | 'Social'
          subject?: string
          grade?: number
          difficulty?: 'easy' | 'medium' | 'hard' | 'mixed' | null
          questions_answered?: number
          correct_answers?: number
          accuracy?: number
          topics?: string[] | null
          created_at?: string
        }
      }
      user_progress: {
        Row: {
          id: string
          user_id: string
          stream: 'Natural' | 'Social'
          subject: string
          grade: number
          exams_taken: number
          practice_questions: number
          total_correct: number
          total_questions: number
          accuracy: number
          updated_at: string
        }
        Insert: {
          id?: string
          user_id: string
          stream: 'Natural' | 'Social'
          subject: string
          grade: number
          exams_taken?: number
          practice_questions?: number
          total_correct?: number
          total_questions?: number
          accuracy?: number
          updated_at?: string
        }
        Update: {
          id?: string
          user_id?: string
          stream?: 'Natural' | 'Social'
          subject?: string
          grade?: number
          exams_taken?: number
          practice_questions?: number
          total_correct?: number
          total_questions?: number
          accuracy?: number
          updated_at?: string
        }
      }
      leaderboard: {
        Row: {
          id: string
          user_id: string
          username: string
          total_exams: number
          overall_accuracy: number
          rank: number | null
          badge: 'gold' | 'silver' | 'bronze' | null
          updated_at: string
        }
        Insert: {
          id?: string
          user_id: string
          username: string
          total_exams?: number
          overall_accuracy?: number
          rank?: number | null
          badge?: 'gold' | 'silver' | 'bronze' | null
          updated_at?: string
        }
        Update: {
          id?: string
          user_id?: string
          username?: string
          total_exams?: number
          overall_accuracy?: number
          rank?: number | null
          badge?: 'gold' | 'silver' | 'bronze' | null
          updated_at?: string
        }
      }
      question_reports: {
        Row: {
          id: string
          user_id: string
          question_id: string
          subject: string
          grade: number
          reason: string
          description: string | null
          status: 'pending' | 'reviewed' | 'resolved'
          created_at: string
        }
        Insert: {
          id?: string
          user_id: string
          question_id: string
          subject: string
          grade: number
          reason: string
          description?: string | null
          status?: 'pending' | 'reviewed' | 'resolved'
          created_at?: string
        }
        Update: {
          id?: string
          user_id?: string
          question_id?: string
          subject?: string
          grade?: number
          reason?: string
          description?: string | null
          status?: 'pending' | 'reviewed' | 'resolved'
          created_at?: string
        }
      }
    }
  }
}
