import { useEffect, useState } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { attemptsAPI } from '../lib/api';
import {
  Trophy,
  CheckCircle2,
  XCircle,
  RotateCcw,
  Home,
  AlertCircle,
} from 'lucide-react';

type ResultsPageProps = {
  attemptId: string;
  onBack: () => void;
  onNavigate?: (page: 'leaderboard') => void;
};

export function ResultsPage({ attemptId, onBack, onNavigate }: ResultsPageProps) {
  const { user } = useAuth();
  const [loading, setLoading] = useState(true);
  const [results, setResults] = useState<any>(null);

  useEffect(() => {
    loadResults();
  }, [attemptId]);

  const loadResults = async () => {
    try {
      setLoading(true);
      const attemptData = await attemptsAPI.getById(attemptId);
      
      if (!attemptData) {
        throw new Error('Attempt not found');
      }

      // Format the time spent
      const timeSpentMinutes = Math.floor(attemptData.time_spent_seconds / 60);
      const timeSpentSeconds = attemptData.time_spent_seconds % 60;
      const timeSpentFormatted = timeSpentMinutes > 0 
        ? `${timeSpentMinutes}m ${timeSpentSeconds}s`
        : `${timeSpentSeconds}s`;

      // Format the results data
      const formattedResults = {
        examTitle: attemptData.exam_title,
        score: attemptData.percentage || 0,
        totalPoints: attemptData.total_points || 0,
        maxPoints: attemptData.max_points || 0,
        timeSpent: timeSpentFormatted,
        completedAt: attemptData.completed_at,
        mode: attemptData.mode,
        examType: attemptData.exam_type,
        subject: attemptData.subject,
        answers: attemptData.answers.map((answer: any, index: number) => ({
          questionNumber: answer.question_number || (index + 1),
          questionId: answer.question_id,
          selectedAnswer: answer.selected_answer,
          correctAnswer: answer.correct_answer,
          isCorrect: answer.is_correct,
          pointsEarned: answer.points_earned,
          answeredAt: answer.answered_at,
        }))
      };

      setResults(formattedResults);
    } catch (error) {
      console.error('Error loading results:', error);
      setResults(null);
    } finally {
      setLoading(false);
    }
  };

  const getScoreColor = (score: number) => {
    if (score >= 80) return 'text-green-600';
    if (score >= 60) return 'text-yellow-600';
    return 'text-red-600';
  };

  const getScoreBgColor = (score: number) => {
    if (score >= 80) return 'bg-green-50 border-green-200';
    if (score >= 60) return 'bg-yellow-50 border-yellow-200';
    return 'bg-red-50 border-red-200';
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-slate-50 dark:bg-slate-900 flex items-center justify-center p-4">
        <div className="text-center">
          <div className="relative mb-6">
            <div className="animate-spin rounded-full h-16 w-16 sm:h-20 sm:w-20 border-4 border-green-200 border-t-green-600 mx-auto"></div>
            <div className="absolute inset-0 flex items-center justify-center">
              <Trophy className="w-6 h-6 sm:w-8 sm:h-8 text-green-600 animate-pulse" />
            </div>
          </div>
          <h2 className="text-xl sm:text-2xl font-bold text-slate-800 dark:text-white mb-2">Calculating Results</h2>
          <p className="text-slate-600 dark:text-slate-400 text-sm sm:text-base">Analyzing your answers...</p>
        </div>
      </div>
    );
  }

  if (!results) {
    return (
      <div className="min-h-screen bg-slate-50 dark:bg-slate-900 flex items-center justify-center p-4">
        <div className="max-w-md mx-auto text-center">
          <div className="w-16 h-16 sm:w-20 sm:h-20 bg-red-100 rounded-full flex items-center justify-center mx-auto mb-6">
            <AlertCircle className="text-red-600 w-8 h-8 sm:w-10 sm:h-10" />
          </div>
          <h2 className="text-xl sm:text-2xl font-bold text-slate-800 dark:text-white mb-2">Results Not Available</h2>
          <p className="text-slate-600 dark:text-slate-400 mb-6 text-sm sm:text-base">
            We're having trouble loading your results. Please try again.
          </p>
          <button
            onClick={onBack}
            className="px-6 py-3 bg-blue-600 text-white rounded-xl font-semibold hover:bg-blue-700 transition-colors touch-manipulation min-h-[48px]"
          >
            Return to Dashboard
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50 dark:from-slate-900 dark:via-slate-800 dark:to-slate-900">
      <div className="p-4 space-y-6">
        {/* Header */}
        <div className="bg-white dark:bg-slate-800 rounded-3xl shadow-xl border border-slate-200 dark:border-slate-700 p-6">
          <div className="flex items-center justify-between mb-6">
            <div>
              <h1 className="text-2xl font-bold text-slate-800 dark:text-white mb-1">Exam Results</h1>
              <p className="text-slate-600 dark:text-slate-400">{results.examType} • {results.subject}</p>
            </div>
            <button
              onClick={onBack}
              className="w-12 h-12 rounded-full bg-slate-100 dark:bg-slate-700 flex items-center justify-center hover:bg-slate-200 dark:hover:bg-slate-600 transition-colors"
            >
              <Home size={20} className="text-slate-600 dark:text-slate-400" />
            </button>
          </div>

          {/* Score Overview */}
          <div className={`border-2 rounded-2xl p-6 ${getScoreBgColor(results.score)} relative overflow-hidden`}>
            <div className="relative z-10">
              <div className="flex items-center justify-between mb-4">
                <div>
                  <h2 className="text-xl font-bold text-slate-800 dark:text-white">{results.examTitle}</h2>
                  <p className="text-sm text-slate-600 dark:text-slate-400 capitalize">
                    {results.mode} Mode • {results.timeSpent}
                  </p>
                </div>
                <div className={`text-4xl font-bold ${getScoreColor(results.score)}`}>
                  {results.score}%
                </div>
              </div>

              <div className="grid grid-cols-3 gap-4">
                <div className="text-center">
                  <div className="text-2xl font-bold text-slate-800 dark:text-white">{results.totalPoints}</div>
                  <div className="text-xs text-slate-600 dark:text-slate-400">Points Earned</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-slate-800 dark:text-white">{results.maxPoints}</div>
                  <div className="text-xs text-slate-600 dark:text-slate-400">Max Points</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-slate-800 dark:text-white">{results.answers.length}</div>
                  <div className="text-xs text-slate-600 dark:text-slate-400">Questions</div>
                </div>
              </div>
            </div>
            
            {/* Background decoration */}
            <div className="absolute top-4 right-4 opacity-10">
              <Trophy size={48} className="text-slate-600" />
            </div>
          </div>
        </div>

        {/* Answer Review */}
        <div className="bg-white dark:bg-slate-800 rounded-3xl shadow-xl border border-slate-200 dark:border-slate-700 p-6">
          <h3 className="text-lg font-bold text-slate-800 dark:text-white mb-6 flex items-center gap-2">
            <CheckCircle2 size={20} />
            Answer Review
          </h3>

          <div className="space-y-4">
            {results.answers.map((answer: any, index: number) => (
              <div key={answer.questionId || index} className={`border-2 rounded-2xl p-4 transition-all ${
                answer.isCorrect 
                  ? 'border-green-200 bg-green-50 dark:bg-green-900/20 dark:border-green-700' 
                  : 'border-red-200 bg-red-50 dark:bg-red-900/20 dark:border-red-700'
              }`}>
                <div className="flex items-start gap-4">
                  <div className={`flex-shrink-0 w-10 h-10 rounded-2xl flex items-center justify-center font-bold text-sm shadow-lg ${
                    answer.isCorrect
                      ? 'bg-green-500 text-white'
                      : 'bg-red-500 text-white'
                  }`}>
                    {answer.isCorrect ? <CheckCircle2 size={16} /> : <XCircle size={16} />}
                  </div>
                  <div className="flex-1">
                    <div className="flex items-center gap-2 mb-2">
                      <span className="text-sm font-semibold text-slate-700 dark:text-slate-300">
                        Question {answer.questionNumber}
                      </span>
                      <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                        answer.isCorrect
                          ? 'bg-green-100 text-green-700 dark:bg-green-800 dark:text-green-200'
                          : 'bg-red-100 text-red-700 dark:bg-red-800 dark:text-red-200'
                      }`}>
                        {answer.pointsEarned} pts
                      </span>
                    </div>
                    
                    <div className="flex flex-wrap items-center gap-2">
                      <span className={`px-3 py-1 rounded-full text-sm font-medium ${
                        answer.isCorrect
                          ? 'bg-green-100 text-green-700 dark:bg-green-800 dark:text-green-200'
                          : 'bg-red-100 text-red-700 dark:bg-red-800 dark:text-red-200'
                      }`}>
                        Your answer: {answer.selectedAnswer}
                      </span>
                      {!answer.isCorrect && (
                        <span className="px-3 py-1 rounded-full text-sm font-medium bg-slate-100 text-slate-700 dark:bg-slate-700 dark:text-slate-300">
                          Correct: {answer.correctAnswer}
                        </span>
                      )}
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>

          {/* Action Buttons */}
          <div className="flex flex-col sm:flex-row gap-3 mt-8 pt-6 border-t border-slate-200 dark:border-slate-700">
            <button
              onClick={onBack}
              className="flex-1 flex items-center justify-center gap-2 px-6 py-4 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-2xl font-bold hover:shadow-xl transition-all duration-300 hover:scale-[1.02] active:scale-98"
            >
              <RotateCcw size={20} />
              Take Another Exam
            </button>
            <button 
              onClick={() => onNavigate ? onNavigate('leaderboard') : onBack()}
              className="flex-1 flex items-center justify-center gap-2 px-6 py-4 border-2 border-slate-200 dark:border-slate-700 text-slate-700 dark:text-slate-300 rounded-2xl font-bold hover:bg-slate-50 dark:hover:bg-slate-700 transition-all duration-300 active:scale-98"
            >
              <Trophy size={20} />
              View Leaderboard
            </button>
          </div>
        </div>

        {/* Bottom Padding */}
        <div className="h-4"></div>
      </div>
    </div>
  );
}