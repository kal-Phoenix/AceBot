import { useEffect, useState } from 'react';
import { BookOpen, Target, TrendingUp, Award } from 'lucide-react';
import { useAuth } from '../contexts/AuthContext';
import { Layout } from '../components/Layout';
import { Card } from '../components/Card';
import { Button } from '../components/Button';
import { supabase } from '../lib/supabase';

interface HomeProps {
  onSelectMode: (mode: 'exam' | 'practice') => void;
  onViewLeaderboard: () => void;
  onViewProgress: () => void;
}

export function Home({ onSelectMode, onViewLeaderboard, onViewProgress }: HomeProps) {
  const { user } = useAuth();
  const [globalAverage, setGlobalAverage] = useState<number>(0);
  const [userRank, setUserRank] = useState<number | null>(null);

  useEffect(() => {
    loadStats();
  }, [user]);

  async function loadStats() {
    const { data: avgData } = await supabase
      .from('users')
      .select('overall_accuracy');

    if (avgData && avgData.length > 0) {
      const avg = avgData.reduce((sum, u) => sum + u.overall_accuracy, 0) / avgData.length;
      setGlobalAverage(avg);
    }

    if (user) {
      const { data: leaderboardData } = await supabase
        .from('leaderboard')
        .select('rank')
        .eq('user_id', user.id)
        .maybeSingle();

      if (leaderboardData?.rank) {
        setUserRank(leaderboardData.rank);
      }
    }
  }

  return (
    <Layout>
      <div className="space-y-6">
        <div className="text-center">
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
            Welcome, {user?.username || 'Student'}!
          </h1>
          <p className="text-gray-600 dark:text-gray-400">
            Ready to test your knowledge?
          </p>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
          <Card className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600 dark:text-gray-400">Your Accuracy</p>
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
                <p className="text-sm text-gray-600 dark:text-gray-400">Global Average</p>
                <p className="text-2xl font-bold text-gray-700 dark:text-gray-300">
                  {globalAverage.toFixed(1)}%
                </p>
              </div>
              <Target className="w-8 h-8 text-gray-600 dark:text-gray-400" />
            </div>
          </Card>

          <Card className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600 dark:text-gray-400">Your Rank</p>
                <p className="text-2xl font-bold text-green-600 dark:text-green-400">
                  {userRank ? `#${userRank}` : 'Unranked'}
                </p>
              </div>
              <Award className="w-8 h-8 text-green-600 dark:text-green-400" />
            </div>
          </Card>
        </div>

        <div className="space-y-4">
          <h2 className="text-xl font-semibold text-gray-900 dark:text-white">
            Choose Your Mode
          </h2>

          <Card hoverable onClick={() => onSelectMode('exam')} className="p-6">
            <div className="flex items-start space-x-4">
              <div className="p-3 bg-blue-100 dark:bg-blue-900 rounded-lg">
                <Target className="w-6 h-6 text-blue-600 dark:text-blue-400" />
              </div>
              <div className="flex-1">
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-1">
                  Exam Mode
                </h3>
                <p className="text-sm text-gray-600 dark:text-gray-400">
                  Take timed exams and compete on the leaderboard. Your first attempt counts!
                </p>
              </div>
            </div>
          </Card>

          <Card hoverable onClick={() => onSelectMode('practice')} className="p-6">
            <div className="flex items-start space-x-4">
              <div className="p-3 bg-green-100 dark:bg-green-900 rounded-lg">
                <BookOpen className="w-6 h-6 text-green-600 dark:text-green-400" />
              </div>
              <div className="flex-1">
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-1">
                  Practice Mode
                </h3>
                <p className="text-sm text-gray-600 dark:text-gray-400">
                  Practice at your own pace with immediate feedback. No time limits!
                </p>
              </div>
            </div>
          </Card>
        </div>

        <div className="grid grid-cols-2 gap-4">
          <Button variant="outline" onClick={onViewLeaderboard} fullWidth>
            <Award className="w-4 h-4 inline mr-2" />
            Leaderboard
          </Button>
          <Button variant="outline" onClick={onViewProgress} fullWidth>
            <TrendingUp className="w-4 h-4 inline mr-2" />
            My Progress
          </Button>
        </div>
      </div>
    </Layout>
  );
}
