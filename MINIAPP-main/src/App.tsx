import { useState } from 'react';
import { AuthProvider, useAuth } from './contexts/AuthContext';
import { ThemeProvider } from './contexts/ThemeContext';
import { Home } from './pages/Home';
import { ExamSelection } from './pages/ExamSelection';
import { PracticeSelection } from './pages/PracticeSelection';
import { QuestionInterface } from './pages/QuestionInterface';
import { Results } from './pages/Results';
import { ReviewAnswers } from './pages/ReviewAnswers';
import { Leaderboard } from './pages/Leaderboard';
import { Progress } from './pages/Progress';
import { ReportModal } from './components/ReportModal';
import { supabase } from './lib/supabase';
import type { Question, UserAnswer, ExamConfig, PracticeConfig } from './types/question.types';
import { getQuestionsByConfig, getRandomQuestions } from './data/sampleQuestions';

type Screen =
  | 'home'
  | 'exam-selection'
  | 'practice-selection'
  | 'questions'
  | 'results'
  | 'review'
  | 'leaderboard'
  | 'progress';

function AppContent() {
  const { user, loading } = useAuth();
  const [screen, setScreen] = useState<Screen>('home');
  const [currentQuestions, setCurrentQuestions] = useState<Question[]>([]);
  const [currentAnswers, setCurrentAnswers] = useState<UserAnswer[]>([]);
  const [currentConfig, setCurrentConfig] = useState<ExamConfig | PracticeConfig | null>(null);
  const [isPracticeMode, setIsPracticeMode] = useState(false);
  const [timeSpent, setTimeSpent] = useState(0);
  const [reportingQuestion, setReportingQuestion] = useState<Question | null>(null);

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 dark:bg-gray-900 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600 dark:text-gray-400">Loading...</p>
        </div>
      </div>
    );
  }

  if (!user) {
    return (
      <div className="min-h-screen bg-gray-50 dark:bg-gray-900 flex items-center justify-center">
        <div className="text-center p-6">
          <h1 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">
            Welcome to Exam Platform
          </h1>
          <p className="text-gray-600 dark:text-gray-400">
            Please open this app in Telegram to continue
          </p>
        </div>
      </div>
    );
  }

  function handleSelectMode(mode: 'exam' | 'practice') {
    setIsPracticeMode(mode === 'practice');
    setScreen(mode === 'exam' ? 'exam-selection' : 'practice-selection');
  }

  function handleStartExam(config: ExamConfig) {
    const questions = getQuestionsByConfig({
      stream: config.stream,
      subject: config.subject,
      grade: config.grade,
      year: config.year,
    });

    const selectedQuestions = getRandomQuestions(questions, Math.min(config.totalQuestions, questions.length));

    setCurrentQuestions(selectedQuestions);
    setCurrentConfig(config);
    setScreen('questions');
  }

  function handleStartPractice(config: PracticeConfig) {
    let questions: Question[];

    if (config.isPastExam && config.year) {
      questions = getQuestionsByConfig({
        stream: config.stream,
        subject: config.subject,
        grade: config.grade,
        year: config.year,
      });
    } else {
      questions = getQuestionsByConfig({
        stream: config.stream,
        subject: config.subject,
        grade: config.grade,
        difficulty: config.difficulty === 'mixed' ? undefined : config.difficulty,
      });
    }

    const selectedQuestions = getRandomQuestions(questions, Math.min(50, questions.length));

    setCurrentQuestions(selectedQuestions);
    setCurrentConfig(config);
    setScreen('questions');
  }

  async function handleCompleteQuestions(answers: UserAnswer[], time: number) {
    setCurrentAnswers(answers);
    setTimeSpent(time);

    if (!isPracticeMode && currentConfig && 'year' in currentConfig) {
      await saveExamAttempt(answers, time, currentConfig);
    } else if (isPracticeMode && currentConfig) {
      await savePracticeSession(answers, currentConfig);
    }

    setScreen('results');
  }

  async function saveExamAttempt(answers: UserAnswer[], time: number, config: ExamConfig) {
    if (!user) return;

    const correctCount = answers.filter((a) => a.isCorrect).length;
    const accuracy = (correctCount / answers.length) * 100;

    const { data: existingAttempts } = await supabase
      .from('exam_attempts')
      .select('id')
      .eq('user_id', user.id)
      .eq('stream', config.stream)
      .eq('subject', config.subject)
      .eq('grade', config.grade)
      .eq('year', config.year);

    const isFirstAttempt = !existingAttempts || existingAttempts.length === 0;

    await supabase.from('exam_attempts').insert({
      user_id: user.id,
      stream: config.stream,
      subject: config.subject,
      grade: config.grade,
      year: config.year,
      total_questions: answers.length,
      correct_answers: correctCount,
      accuracy,
      time_taken_seconds: time,
      time_limit_seconds: config.timeLimitSeconds,
      is_first_attempt: isFirstAttempt,
      answers: answers as any,
    });
  }

  async function savePracticeSession(answers: UserAnswer[], config: PracticeConfig) {
    if (!user) return;

    const correctCount = answers.filter((a) => a.isCorrect).length;
    const accuracy = (correctCount / answers.length) * 100;

    const { data: session } = await supabase
      .from('practice_sessions')
      .insert({
        user_id: user.id,
        stream: config.stream,
        subject: config.subject,
        grade: config.grade,
        difficulty: config.difficulty === 'mixed' ? null : config.difficulty,
        questions_answered: answers.length,
        correct_answers: correctCount,
        accuracy,
        topics: config.topics || null,
      })
      .select()
      .single();

    if (session) {
      const { data: existingProgress } = await supabase
        .from('user_progress')
        .select('*')
        .eq('user_id', user.id)
        .eq('stream', config.stream)
        .eq('subject', config.subject)
        .eq('grade', config.grade)
        .maybeSingle();

      if (existingProgress) {
        const newTotalCorrect = existingProgress.total_correct + correctCount;
        const newTotalQuestions = existingProgress.total_questions + answers.length;
        const newAccuracy = (newTotalCorrect / newTotalQuestions) * 100;

        await supabase
          .from('user_progress')
          .update({
            practice_questions: existingProgress.practice_questions + answers.length,
            total_correct: newTotalCorrect,
            total_questions: newTotalQuestions,
            accuracy: newAccuracy,
            updated_at: new Date().toISOString(),
          })
          .eq('id', existingProgress.id);
      } else {
        await supabase.from('user_progress').insert({
          user_id: user.id,
          stream: config.stream,
          subject: config.subject,
          grade: config.grade,
          practice_questions: answers.length,
          total_correct: correctCount,
          total_questions: answers.length,
          accuracy,
        });
      }

      await supabase
        .from('users')
        .update({
          total_practice_questions: user.total_practice_questions + answers.length,
          updated_at: new Date().toISOString(),
        })
        .eq('id', user.id);
    }
  }

  function handleReview() {
    setScreen('review');
  }

  function handleReportQuestion(questionId: string) {
    const question = currentQuestions.find((q) => q.id === questionId);
    if (question) {
      setReportingQuestion(question);
    }
  }

  function handleReturnHome() {
    setScreen('home');
    setCurrentQuestions([]);
    setCurrentAnswers([]);
    setCurrentConfig(null);
    setTimeSpent(0);
  }

  return (
    <>
      {screen === 'home' && (
        <Home
          onSelectMode={handleSelectMode}
          onViewLeaderboard={() => setScreen('leaderboard')}
          onViewProgress={() => setScreen('progress')}
        />
      )}

      {screen === 'exam-selection' && (
        <ExamSelection
          onBack={handleReturnHome}
          onStartExam={handleStartExam}
        />
      )}

      {screen === 'practice-selection' && (
        <PracticeSelection
          onBack={handleReturnHome}
          onStartPractice={handleStartPractice}
        />
      )}

      {screen === 'questions' && currentConfig && (
        <QuestionInterface
          questions={currentQuestions}
          config={currentConfig}
          isPracticeMode={isPracticeMode}
          onComplete={handleCompleteQuestions}
          onBack={handleReturnHome}
        />
      )}

      {screen === 'results' && (
        <Results
          questions={currentQuestions}
          answers={currentAnswers}
          timeSpent={timeSpent}
          isPracticeMode={isPracticeMode}
          onReview={handleReview}
          onReturnHome={handleReturnHome}
        />
      )}

      {screen === 'review' && (
        <ReviewAnswers
          questions={currentQuestions}
          answers={currentAnswers}
          onReportQuestion={handleReportQuestion}
          onBack={() => setScreen('results')}
        />
      )}

      {screen === 'leaderboard' && (
        <Leaderboard onBack={handleReturnHome} />
      )}

      {screen === 'progress' && (
        <Progress onBack={handleReturnHome} />
      )}

      {reportingQuestion && (
        <ReportModal
          question={reportingQuestion}
          onClose={() => setReportingQuestion(null)}
        />
      )}
    </>
  );
}

function App() {
  return (
    <ThemeProvider>
      <AuthProvider>
        <AppContent />
      </AuthProvider>
    </ThemeProvider>
  );
}

export default App;
