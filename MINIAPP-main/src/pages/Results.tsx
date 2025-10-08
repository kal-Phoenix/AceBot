import { useEffect, useState } from 'react';
import { Award, Clock, Target, TrendingUp, Flag, CheckCircle } from 'lucide-react';
import { Layout } from '../components/Layout';
import { Card } from '../components/Card';
import { Button } from '../components/Button';
import type { Question, UserAnswer } from '../types/question.types';

interface ResultsProps {
  questions: Question[];
  answers: UserAnswer[];
  timeSpent: number;
  isPracticeMode: boolean;
  onReview: () => void;
  onReturnHome: () => void;
}

export function Results({
  questions,
  answers,
  timeSpent,
  isPracticeMode,
  onReview,
  onReturnHome,
}: ResultsProps) {
  const [showConfetti, setShowConfetti] = useState(false);

  const correctCount = answers.filter((a) => a.isCorrect).length;
  const totalQuestions = questions.length;
  const accuracy = (correctCount / totalQuestions) * 100;
  const flaggedCount = answers.filter((a) => a.isFlagged).length;

  useEffect(() => {
    if (accuracy >= 90) {
      setShowConfetti(true);
      setTimeout(() => setShowConfetti(false), 3000);
    }
  }, [accuracy]);

  function formatTime(seconds: number): string {
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    const secs = seconds % 60;

    if (hours > 0) {
      return `${hours}h ${minutes}m ${secs}s`;
    } else if (minutes > 0) {
      return `${minutes}m ${secs}s`;
    } else {
      return `${secs}s`;
    }
  }

  function getPerformanceMessage(): { message: string; color: string } {
    if (accuracy >= 90) {
      return { message: 'Outstanding Performance!', color: 'text-green-600 dark:text-green-400' };
    } else if (accuracy >= 80) {
      return { message: 'Great Job!', color: 'text-blue-600 dark:text-blue-400' };
    } else if (accuracy >= 70) {
      return { message: 'Good Effort!', color: 'text-yellow-600 dark:text-yellow-400' };
    } else if (accuracy >= 60) {
      return { message: 'Keep Practicing!', color: 'text-orange-600 dark:text-orange-400' };
    } else {
      return { message: 'More Practice Needed', color: 'text-red-600 dark:text-red-400' };
    }
  }

  const performance = getPerformanceMessage();

  return (
    <Layout>
      <div className="space-y-6">
        {showConfetti && (
          <div className="fixed inset-0 pointer-events-none z-50 flex items-center justify-center">
            <div className="text-6xl animate-bounce">
              🎉
            </div>
          </div>
        )}

        <div className="text-center">
          <div className="inline-flex p-4 bg-blue-100 dark:bg-blue-900 rounded-full mb-4">
            <Award className="w-12 h-12 text-blue-600 dark:text-blue-400" />
          </div>
          <h1 className={`text-3xl font-bold mb-2 ${performance.color}`}>
            {performance.message}
          </h1>
          <p className="text-gray-600 dark:text-gray-400">
            {isPracticeMode ? 'Practice Session Complete' : 'Exam Complete'}
          </p>
        </div>

        <Card className="p-6">
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
            <div className="text-center">
              <div className="flex justify-center mb-2">
                <Target className="w-6 h-6 text-blue-600 dark:text-blue-400" />
              </div>
              <p className="text-sm text-gray-600 dark:text-gray-400">Score</p>
              <p className="text-2xl font-bold text-gray-900 dark:text-white">
                {correctCount}/{totalQuestions}
              </p>
            </div>

            <div className="text-center">
              <div className="flex justify-center mb-2">
                <TrendingUp className="w-6 h-6 text-green-600 dark:text-green-400" />
              </div>
              <p className="text-sm text-gray-600 dark:text-gray-400">Accuracy</p>
              <p className="text-2xl font-bold text-gray-900 dark:text-white">
                {accuracy.toFixed(1)}%
              </p>
            </div>

            <div className="text-center">
              <div className="flex justify-center mb-2">
                <Clock className="w-6 h-6 text-purple-600 dark:text-purple-400" />
              </div>
              <p className="text-sm text-gray-600 dark:text-gray-400">Time</p>
              <p className="text-2xl font-bold text-gray-900 dark:text-white">
                {formatTime(timeSpent)}
              </p>
            </div>

            <div className="text-center">
              <div className="flex justify-center mb-2">
                <Flag className="w-6 h-6 text-red-600 dark:text-red-400" />
              </div>
              <p className="text-sm text-gray-600 dark:text-gray-400">Flagged</p>
              <p className="text-2xl font-bold text-gray-900 dark:text-white">
                {flaggedCount}
              </p>
            </div>
          </div>
        </Card>

        <Card className="p-6">
          <h3 className="font-semibold text-gray-900 dark:text-white mb-4">
            Performance Breakdown
          </h3>
          <div className="space-y-3">
            <div>
              <div className="flex justify-between text-sm mb-1">
                <span className="text-gray-600 dark:text-gray-400">Correct Answers</span>
                <span className="text-green-600 dark:text-green-400 font-semibold">
                  {correctCount} ({accuracy.toFixed(1)}%)
                </span>
              </div>
              <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                <div
                  className="bg-green-500 h-2 rounded-full transition-all"
                  style={{ width: `${accuracy}%` }}
                />
              </div>
            </div>

            <div>
              <div className="flex justify-between text-sm mb-1">
                <span className="text-gray-600 dark:text-gray-400">Incorrect Answers</span>
                <span className="text-red-600 dark:text-red-400 font-semibold">
                  {totalQuestions - correctCount} ({(100 - accuracy).toFixed(1)}%)
                </span>
              </div>
              <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                <div
                  className="bg-red-500 h-2 rounded-full transition-all"
                  style={{ width: `${100 - accuracy}%` }}
                />
              </div>
            </div>
          </div>
        </Card>

        {!isPracticeMode && (
          <Card className="p-6 bg-blue-50 dark:bg-blue-900/20">
            <div className="flex items-start space-x-3">
              <CheckCircle className="w-6 h-6 text-blue-600 dark:text-blue-400 mt-0.5" />
              <div>
                <h3 className="font-semibold text-gray-900 dark:text-white mb-1">
                  Leaderboard Status
                </h3>
                <p className="text-sm text-gray-700 dark:text-gray-300">
                  Your first attempt score has been recorded and will appear on the leaderboard shortly.
                </p>
              </div>
            </div>
          </Card>
        )}

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <Button onClick={onReview} variant="secondary" fullWidth size="lg">
            Review Answers
          </Button>
          <Button onClick={onReturnHome} variant="primary" fullWidth size="lg">
            Return Home
          </Button>
        </div>
      </div>
    </Layout>
  );
}
