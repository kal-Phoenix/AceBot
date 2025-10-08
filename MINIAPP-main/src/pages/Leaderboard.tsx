import { useEffect, useState } from 'react';
import { ChevronLeft, Award, Trophy, Medal } from 'lucide-react';
import { Layout } from '../components/Layout';
import { Card } from '../components/Card';
import { useAuth } from '../contexts/AuthContext';
import { supabase } from '../lib/supabase';

interface LeaderboardEntry {
  id: string;
  user_id: string;
  username: string;
  total_exams: number;
  overall_accuracy: number;
  rank: number | null;
  badge: 'gold' | 'silver' | 'bronze' | null;
}

interface LeaderboardProps {
  onBack: () => void;
}

export function Leaderboard({ onBack }: LeaderboardProps) {
  const { user } = useAuth();
  const [leaderboard, setLeaderboard] = useState<LeaderboardEntry[]>([]);
  const [userEntry, setUserEntry] = useState<LeaderboardEntry | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadLeaderboard();
  }, [user]);

  async function loadLeaderboard() {
    setLoading(true);

    await supabase.rpc('update_leaderboard_rankings');

    const { data, error } = await supabase
      .from('leaderboard')
      .select('*')
      .order('rank', { ascending: true, nullsFirst: false })
      .limit(100);

    if (error) {
      console.error('Error loading leaderboard:', error);
    } else if (data) {
      setLeaderboard(data);

      if (user) {
        const currentUserEntry = data.find((entry) => entry.user_id === user.id);
        if (currentUserEntry) {
          setUserEntry(currentUserEntry);
        } else {
          const { data: userData } = await supabase
            .from('leaderboard')
            .select('*')
            .eq('user_id', user.id)
            .maybeSingle();

          if (userData) {
            setUserEntry(userData);
          }
        }
      }
    }

    setLoading(false);
  }

  function getBadgeIcon(badge: string | null) {
    if (badge === 'gold') return <Trophy className="w-5 h-5 text-yellow-500" />;
    if (badge === 'silver') return <Trophy className="w-5 h-5 text-gray-400" />;
    if (badge === 'bronze') return <Trophy className="w-5 h-5 text-orange-600" />;
    return null;
  }

  function getRankDisplay(rank: number | null) {
    if (rank === 1) return '🥇';
    if (rank === 2) return '🥈';
    if (rank === 3) return '🥉';
    return `#${rank}`;
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
              Leaderboard
            </h1>
            <p className="text-sm text-gray-600 dark:text-gray-400">
              Top performers globally
            </p>
          </div>
        </div>

        {userEntry && userEntry.rank && userEntry.rank > 100 && (
          <Card className="p-4 bg-blue-50 dark:bg-blue-900/20">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-3">
                <Award className="w-6 h-6 text-blue-600 dark:text-blue-400" />
                <div>
                  <p className="font-semibold text-gray-900 dark:text-white">
                    Your Position
                  </p>
                  <p className="text-sm text-gray-600 dark:text-gray-400">
                    {userEntry.username}
                  </p>
                </div>
              </div>
              <div className="text-right">
                <p className="text-2xl font-bold text-blue-600 dark:text-blue-400">
                  #{userEntry.rank}
                </p>
                <p className="text-sm text-gray-600 dark:text-gray-400">
                  {userEntry.overall_accuracy.toFixed(1)}%
                </p>
              </div>
            </div>
          </Card>
        )}

        {loading ? (
          <Card className="p-8 text-center">
            <p className="text-gray-600 dark:text-gray-400">Loading leaderboard...</p>
          </Card>
        ) : leaderboard.length === 0 ? (
          <Card className="p-8 text-center">
            <Medal className="w-12 h-12 text-gray-400 mx-auto mb-3" />
            <p className="text-gray-600 dark:text-gray-400">
              No entries yet. Be the first to take an exam!
            </p>
          </Card>
        ) : (
          <Card className="overflow-hidden">
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead className="bg-gray-100 dark:bg-gray-800">
                  <tr>
                    <th className="px-4 py-3 text-left text-sm font-semibold text-gray-700 dark:text-gray-300">
                      Rank
                    </th>
                    <th className="px-4 py-3 text-left text-sm font-semibold text-gray-700 dark:text-gray-300">
                      Username
                    </th>
                    <th className="px-4 py-3 text-center text-sm font-semibold text-gray-700 dark:text-gray-300">
                      Accuracy
                    </th>
                    <th className="px-4 py-3 text-center text-sm font-semibold text-gray-700 dark:text-gray-300">
                      Exams
                    </th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-200 dark:divide-gray-700">
                  {leaderboard.map((entry, index) => {
                    const isCurrentUser = user && entry.user_id === user.id;

                    return (
                      <tr
                        key={entry.id}
                        className={`${
                          isCurrentUser
                            ? 'bg-blue-50 dark:bg-blue-900/20'
                            : index % 2 === 0
                            ? 'bg-white dark:bg-gray-800'
                            : 'bg-gray-50 dark:bg-gray-800/50'
                        }`}
                      >
                        <td className="px-4 py-3">
                          <div className="flex items-center space-x-2">
                            <span className="text-lg font-bold text-gray-900 dark:text-white">
                              {getRankDisplay(entry.rank)}
                            </span>
                            {getBadgeIcon(entry.badge)}
                          </div>
                        </td>
                        <td className="px-4 py-3">
                          <span
                            className={`font-medium ${
                              isCurrentUser
                                ? 'text-blue-600 dark:text-blue-400'
                                : 'text-gray-900 dark:text-white'
                            }`}
                          >
                            {entry.username}
                            {isCurrentUser && (
                              <span className="ml-2 text-xs bg-blue-600 text-white px-2 py-0.5 rounded">
                                You
                              </span>
                            )}
                          </span>
                        </td>
                        <td className="px-4 py-3 text-center">
                          <span className="font-semibold text-gray-900 dark:text-white">
                            {entry.overall_accuracy.toFixed(1)}%
                          </span>
                        </td>
                        <td className="px-4 py-3 text-center">
                          <span className="text-gray-600 dark:text-gray-400">
                            {entry.total_exams}
                          </span>
                        </td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
          </Card>
        )}
      </div>
    </Layout>
  );
}
