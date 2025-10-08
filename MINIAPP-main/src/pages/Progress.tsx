import { useEffect, useState } from 'react';
import { ChevronLeft, TrendingUp, BookOpen, Target, Award } from 'lucide-react';
import { Layout } from '../components/Layout';
import { Card } from '../components/Card';
import { useAuth } from '../contexts/AuthContext';
import { supabase } from '../lib/supabase';
import type { Database } from '../lib/database.types';

type UserProgress = Database['public']['Tables']['user_progress']['Row'];

interface ProgressProps {
  onBack: () => void;
}

export function Progress({ onBack }: ProgressProps) {
  const { user } = useAuth();
  const [progressData, setProgressData] = useState<UserProgress[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadProgress();
  }, [user]);

  async function loadProgress() {
    if (!user) return;

    setLoading(true);

    const { data, error } = await supabase
      .from('user_progress')
      .select('*')
      .eq('user_id', user.id)
      .order('accuracy', { ascending: false });

    if (error) {
      console.error('Error loading progress:', error);
    } else if (data) {
      setProgressData(data);
    }

    setLoading(false);
  }

  function getSubjectColor(accuracy: number) {
    if (accuracy >= 90) return 'bg-green-500';
    if (accuracy >= 80) return 'bg-blue-500';
    if (accuracy >= 70) return 'bg-yellow-500';
    if (accuracy >= 60) return 'bg-orange-500';
    return 'bg-red-500';
  }

  return (
    <Layout>
      <div className="space-y-6">
        <div className="flex items-center space-x-4">
          <button
            onClick={onBack}
            className="p-2 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-lg transition-colors"
          >
            <ChevronLeft className="w-6 h-6 text-gray-700 dark:text-gray-300" />
          </button>
          <div>
            <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
              My Progress
            </h1>
            <p className="text-sm text-gray-600 dark:text-gray-400">
              Track your performance across subjects
            </p>
          </div>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          <Card className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600 dark:text-gray-400">Overall Accuracy</p>
                <p className="text-2xl font-bold text-blue-600 dark:text-blue-400">
                  {user?.overall_accuracy.toFixed(1) || '0'}%
                </p>
              </div>
              <TrendingUp className="w-8 h-8 text-blue-600 dark:text-blue-400" />
            </div>
          </Card>

          <Card className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600 dark:text-gray-400">Total Exams</p>
                <p className="text-2xl font-bold text-green-600 dark:text-green-400">
                  {user?.total_exams_taken || 0}
                </p>
              </div>
              <Target className="w-8 h-8 text-green-600 dark:text-green-400" />
            </div>
          </Card>

          <Card className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600 dark:text-gray-400">Practice Questions</p>
                <p className="text-2xl font-bold text-purple-600 dark:text-purple-400">
                  {user?.total_practice_questions || 0}
                </p>
              </div>
              <BookOpen className="w-8 h-8 text-purple-600 dark:text-purple-400" />
            </div>
          </Card>

          <Card className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600 dark:text-gray-400">Subjects Studied</p>
                <p className="text-2xl font-bold text-orange-600 dark:text-orange-400">
                  {progressData.length}
                </p>
              </div>
              <Award className="w-8 h-8 text-orange-600 dark:text-orange-400" />
            </div>
          </Card>
        </div>

        {loading ? (
          <Card className="p-8 text-center">
            <p className="text-gray-600 dark:text-gray-400">Loading progress...</p>
          </Card>
        ) : progressData.length === 0 ? (
          <Card className="p-8 text-center">
            <BookOpen className="w-12 h-12 text-gray-400 mx-auto mb-3" />
            <p className="text-gray-600 dark:text-gray-400">
              No progress data yet. Start taking exams or practicing to see your progress!
            </p>
          </Card>
        ) : (
          <div className="space-y-4">
            <h2 className="text-xl font-semibold text-gray-900 dark:text-white">
              Subject Performance
            </h2>

            {progressData.map((progress) => (
              <Card key={progress.id} className="p-6">
                <div className="flex items-start justify-between mb-4">
                  <div>
                    <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
                      {progress.subject} - Grade {progress.grade}
                    </h3>
                    <p className="text-sm text-gray-600 dark:text-gray-400">
                      {progress.stream} Stream
                    </p>
                  </div>
                  <div className="text-right">
                    <p className="text-2xl font-bold text-gray-900 dark:text-white">
                      {progress.accuracy.toFixed(1)}%
                    </p>
                    <p className="text-sm text-gray-600 dark:text-gray-400">Accuracy</p>
                  </div>
                </div>

                <div className="space-y-3">
                  <div>
                    <div className="flex justify-between text-sm mb-1">
                      <span className="text-gray-600 dark:text-gray-400">Progress</span>
                      <span className="text-gray-900 dark:text-white font-medium">
                        {progress.total_correct} / {progress.total_questions} correct
                      </span>
                    </div>
                    <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                      <div
                        className={`h-2 rounded-full transition-all ${getSubjectColor(
                          progress.accuracy
                        )}`}
                        style={{ width: `${progress.accuracy}%` }}
                      />
                    </div>
                  </div>

                  <div className="grid grid-cols-3 gap-4 pt-3 border-t border-gray-200 dark:border-gray-700">
                    <div>
                      <p className="text-xs text-gray-600 dark:text-gray-400">Exams Taken</p>
                      <p className="text-lg font-semibold text-gray-900 dark:text-white">
                        {progress.exams_taken}
                      </p>
                    </div>
                    <div>
                      <p className="text-xs text-gray-600 dark:text-gray-400">Practice Qs</p>
                      <p className="text-lg font-semibold text-gray-900 dark:text-white">
                        {progress.practice_questions}
                      </p>
                    </div>
                    <div>
                      <p className="text-xs text-gray-600 dark:text-gray-400">Total Qs</p>
                      <p className="text-lg font-semibold text-gray-900 dark:text-white">
                        {progress.total_questions}
                      </p>
                    </div>
                  </div>
                </div>
              </Card>
            ))}
          </div>
        )}
      </div>
    </Layout>
  );
}
