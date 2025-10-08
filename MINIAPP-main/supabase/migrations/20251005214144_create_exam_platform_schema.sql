/*
  # Exam Platform Database Schema

  ## Overview
  Creates the complete database schema for a Telegram-based exam and practice platform
  supporting 10,000+ concurrent users with 1M+ questions.

  ## Tables Created

  ### 1. users
  Stores user profile and aggregate statistics
  - `id` (uuid, primary key) - Internal user ID
  - `telegram_user_id` (bigint, unique) - Telegram user identifier
  - `username` (text) - Display name from Telegram
  - `first_name` (text) - User's first name
  - `last_name` (text) - User's last name
  - `total_exams_taken` (integer) - Count of completed exams
  - `total_practice_questions` (integer) - Count of practice questions answered
  - `overall_accuracy` (numeric) - Overall accuracy percentage
  - `created_at` (timestamptz) - Account creation timestamp
  - `updated_at` (timestamptz) - Last update timestamp

  ### 2. exam_attempts
  Tracks all exam submissions with scores
  - `id` (uuid, primary key) - Attempt identifier
  - `user_id` (uuid, foreign key) - References users
  - `stream` (text) - Natural or Social
  - `subject` (text) - Subject name
  - `grade` (integer) - Grade level (9-12)
  - `year` (integer) - Exam year
  - `total_questions` (integer) - Number of questions
  - `correct_answers` (integer) - Number correct
  - `accuracy` (numeric) - Percentage score
  - `time_taken_seconds` (integer) - Time spent
  - `time_limit_seconds` (integer) - Allowed time
  - `is_first_attempt` (boolean) - Counts for leaderboard
  - `answers` (jsonb) - User's answers with flags/hints
  - `created_at` (timestamptz) - Submission timestamp

  ### 3. practice_sessions
  Tracks practice mode activity
  - `id` (uuid, primary key) - Session identifier
  - `user_id` (uuid, foreign key) - References users
  - `stream` (text) - Natural or Social
  - `subject` (text) - Subject name
  - `grade` (integer) - Grade level (9-12)
  - `difficulty` (text) - easy, medium, hard, or mixed
  - `questions_answered` (integer) - Total answered
  - `correct_answers` (integer) - Number correct
  - `accuracy` (numeric) - Percentage score
  - `topics` (text[]) - Array of topics practiced
  - `created_at` (timestamptz) - Session start

  ### 4. user_progress
  Subject and grade-specific analytics
  - `id` (uuid, primary key) - Progress record ID
  - `user_id` (uuid, foreign key) - References users
  - `stream` (text) - Natural or Social
  - `subject` (text) - Subject name
  - `grade` (integer) - Grade level (9-12)
  - `exams_taken` (integer) - Count for this subject/grade
  - `practice_questions` (integer) - Practice count
  - `total_correct` (integer) - Correct answers
  - `total_questions` (integer) - Total questions attempted
  - `accuracy` (numeric) - Subject-specific accuracy
  - `updated_at` (timestamptz) - Last activity

  ### 5. leaderboard
  Cached top 100 performers for fast retrieval
  - `id` (uuid, primary key) - Leaderboard entry ID
  - `user_id` (uuid, foreign key) - References users
  - `username` (text) - Display name
  - `total_exams` (integer) - Total exams taken
  - `overall_accuracy` (numeric) - Global accuracy
  - `rank` (integer) - Current rank position
  - `badge` (text) - gold, silver, bronze, or null
  - `updated_at` (timestamptz) - Last rank update

  ### 6. question_reports
  User-reported question errors
  - `id` (uuid, primary key) - Report ID
  - `user_id` (uuid, foreign key) - References users
  - `question_id` (text) - Question identifier
  - `subject` (text) - Question subject
  - `grade` (integer) - Question grade
  - `reason` (text) - Report reason
  - `description` (text) - Detailed description
  - `status` (text) - pending, reviewed, resolved
  - `created_at` (timestamptz) - Report timestamp

  ## Security
  - RLS enabled on all tables
  - Users can only access their own data
  - Leaderboard is publicly readable
  - Question reports are user-specific

  ## Indexes
  - Optimized for telegram_user_id lookups
  - Fast exam attempt queries by user and date
  - Efficient leaderboard ranking
  - Quick progress tracking by subject/grade
*/

-- Create users table
CREATE TABLE IF NOT EXISTS users (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  telegram_user_id bigint UNIQUE NOT NULL,
  username text NOT NULL,
  first_name text,
  last_name text,
  total_exams_taken integer DEFAULT 0,
  total_practice_questions integer DEFAULT 0,
  overall_accuracy numeric(5,2) DEFAULT 0.00,
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now()
);

-- Create exam_attempts table
CREATE TABLE IF NOT EXISTS exam_attempts (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id uuid REFERENCES users(id) ON DELETE CASCADE NOT NULL,
  stream text NOT NULL CHECK (stream IN ('Natural', 'Social')),
  subject text NOT NULL,
  grade integer NOT NULL CHECK (grade >= 9 AND grade <= 12),
  year integer NOT NULL,
  total_questions integer NOT NULL,
  correct_answers integer NOT NULL,
  accuracy numeric(5,2) NOT NULL,
  time_taken_seconds integer NOT NULL,
  time_limit_seconds integer NOT NULL,
  is_first_attempt boolean DEFAULT false,
  answers jsonb NOT NULL,
  created_at timestamptz DEFAULT now()
);

-- Create practice_sessions table
CREATE TABLE IF NOT EXISTS practice_sessions (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id uuid REFERENCES users(id) ON DELETE CASCADE NOT NULL,
  stream text NOT NULL CHECK (stream IN ('Natural', 'Social')),
  subject text NOT NULL,
  grade integer NOT NULL CHECK (grade >= 9 AND grade <= 12),
  difficulty text CHECK (difficulty IN ('easy', 'medium', 'hard', 'mixed')),
  questions_answered integer DEFAULT 0,
  correct_answers integer DEFAULT 0,
  accuracy numeric(5,2) DEFAULT 0.00,
  topics text[],
  created_at timestamptz DEFAULT now()
);

-- Create user_progress table
CREATE TABLE IF NOT EXISTS user_progress (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id uuid REFERENCES users(id) ON DELETE CASCADE NOT NULL,
  stream text NOT NULL CHECK (stream IN ('Natural', 'Social')),
  subject text NOT NULL,
  grade integer NOT NULL CHECK (grade >= 9 AND grade <= 12),
  exams_taken integer DEFAULT 0,
  practice_questions integer DEFAULT 0,
  total_correct integer DEFAULT 0,
  total_questions integer DEFAULT 0,
  accuracy numeric(5,2) DEFAULT 0.00,
  updated_at timestamptz DEFAULT now(),
  UNIQUE(user_id, stream, subject, grade)
);

-- Create leaderboard table
CREATE TABLE IF NOT EXISTS leaderboard (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id uuid REFERENCES users(id) ON DELETE CASCADE NOT NULL UNIQUE,
  username text NOT NULL,
  total_exams integer DEFAULT 0,
  overall_accuracy numeric(5,2) DEFAULT 0.00,
  rank integer,
  badge text CHECK (badge IN ('gold', 'silver', 'bronze')),
  updated_at timestamptz DEFAULT now()
);

-- Create question_reports table
CREATE TABLE IF NOT EXISTS question_reports (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id uuid REFERENCES users(id) ON DELETE CASCADE NOT NULL,
  question_id text NOT NULL,
  subject text NOT NULL,
  grade integer NOT NULL CHECK (grade >= 9 AND grade <= 12),
  reason text NOT NULL,
  description text,
  status text DEFAULT 'pending' CHECK (status IN ('pending', 'reviewed', 'resolved')),
  created_at timestamptz DEFAULT now()
);

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_users_telegram_id ON users(telegram_user_id);
CREATE INDEX IF NOT EXISTS idx_exam_attempts_user_id ON exam_attempts(user_id, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_exam_attempts_first_attempt ON exam_attempts(user_id, is_first_attempt) WHERE is_first_attempt = true;
CREATE INDEX IF NOT EXISTS idx_practice_sessions_user_id ON practice_sessions(user_id, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_user_progress_lookup ON user_progress(user_id, stream, subject, grade);
CREATE INDEX IF NOT EXISTS idx_leaderboard_rank ON leaderboard(rank) WHERE rank IS NOT NULL;
CREATE INDEX IF NOT EXISTS idx_question_reports_status ON question_reports(status, created_at DESC);

-- Enable Row Level Security
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE exam_attempts ENABLE ROW LEVEL SECURITY;
ALTER TABLE practice_sessions ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_progress ENABLE ROW LEVEL SECURITY;
ALTER TABLE leaderboard ENABLE ROW LEVEL SECURITY;
ALTER TABLE question_reports ENABLE ROW LEVEL SECURITY;

-- RLS Policies for users table
CREATE POLICY "Users can view own profile"
  ON users FOR SELECT
  TO authenticated
  USING (auth.uid() = id);

CREATE POLICY "Users can update own profile"
  ON users FOR UPDATE
  TO authenticated
  USING (auth.uid() = id)
  WITH CHECK (auth.uid() = id);

CREATE POLICY "Users can insert own profile"
  ON users FOR INSERT
  TO authenticated
  WITH CHECK (auth.uid() = id);

-- RLS Policies for exam_attempts table
CREATE POLICY "Users can view own exam attempts"
  ON exam_attempts FOR SELECT
  TO authenticated
  USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own exam attempts"
  ON exam_attempts FOR INSERT
  TO authenticated
  WITH CHECK (auth.uid() = user_id);

-- RLS Policies for practice_sessions table
CREATE POLICY "Users can view own practice sessions"
  ON practice_sessions FOR SELECT
  TO authenticated
  USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own practice sessions"
  ON practice_sessions FOR INSERT
  TO authenticated
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own practice sessions"
  ON practice_sessions FOR UPDATE
  TO authenticated
  USING (auth.uid() = user_id)
  WITH CHECK (auth.uid() = user_id);

-- RLS Policies for user_progress table
CREATE POLICY "Users can view own progress"
  ON user_progress FOR SELECT
  TO authenticated
  USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own progress"
  ON user_progress FOR INSERT
  TO authenticated
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own progress"
  ON user_progress FOR UPDATE
  TO authenticated
  USING (auth.uid() = user_id)
  WITH CHECK (auth.uid() = user_id);

-- RLS Policies for leaderboard table (publicly readable)
CREATE POLICY "Anyone can view leaderboard"
  ON leaderboard FOR SELECT
  TO authenticated
  USING (true);

-- RLS Policies for question_reports table
CREATE POLICY "Users can view own reports"
  ON question_reports FOR SELECT
  TO authenticated
  USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own reports"
  ON question_reports FOR INSERT
  TO authenticated
  WITH CHECK (auth.uid() = user_id);

-- Function to update user statistics after exam
CREATE OR REPLACE FUNCTION update_user_stats_after_exam()
RETURNS TRIGGER AS $$
BEGIN
  -- Update users table
  UPDATE users
  SET 
    total_exams_taken = total_exams_taken + 1,
    overall_accuracy = (
      SELECT AVG(accuracy)
      FROM exam_attempts
      WHERE user_id = NEW.user_id
    ),
    updated_at = now()
  WHERE id = NEW.user_id;
  
  -- Update or insert user_progress
  INSERT INTO user_progress (user_id, stream, subject, grade, exams_taken, total_correct, total_questions, accuracy)
  VALUES (
    NEW.user_id,
    NEW.stream,
    NEW.subject,
    NEW.grade,
    1,
    NEW.correct_answers,
    NEW.total_questions,
    NEW.accuracy
  )
  ON CONFLICT (user_id, stream, subject, grade)
  DO UPDATE SET
    exams_taken = user_progress.exams_taken + 1,
    total_correct = user_progress.total_correct + NEW.correct_answers,
    total_questions = user_progress.total_questions + NEW.total_questions,
    accuracy = ((user_progress.total_correct + NEW.correct_answers)::numeric / (user_progress.total_questions + NEW.total_questions)::numeric) * 100,
    updated_at = now();
  
  -- Update leaderboard if first attempt
  IF NEW.is_first_attempt THEN
    INSERT INTO leaderboard (user_id, username, total_exams, overall_accuracy)
    SELECT u.id, u.username, u.total_exams_taken, u.overall_accuracy
    FROM users u
    WHERE u.id = NEW.user_id
    ON CONFLICT (user_id)
    DO UPDATE SET
      total_exams = EXCLUDED.total_exams,
      overall_accuracy = EXCLUDED.overall_accuracy,
      updated_at = now();
  END IF;
  
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger for exam attempts
CREATE TRIGGER trigger_update_user_stats_after_exam
AFTER INSERT ON exam_attempts
FOR EACH ROW
EXECUTE FUNCTION update_user_stats_after_exam();

-- Function to update leaderboard rankings
CREATE OR REPLACE FUNCTION update_leaderboard_rankings()
RETURNS void AS $$
BEGIN
  -- Update ranks based on accuracy (highest first)
  WITH ranked_users AS (
    SELECT 
      user_id,
      ROW_NUMBER() OVER (ORDER BY overall_accuracy DESC, total_exams DESC, updated_at ASC) as new_rank
    FROM leaderboard
    WHERE overall_accuracy > 0
  )
  UPDATE leaderboard l
  SET 
    rank = r.new_rank,
    badge = CASE
      WHEN r.new_rank = 1 THEN 'gold'
      WHEN r.new_rank = 2 THEN 'silver'
      WHEN r.new_rank = 3 THEN 'bronze'
      ELSE NULL
    END
  FROM ranked_users r
  WHERE l.user_id = r.user_id;
END;
$$ LANGUAGE plpgsql;
