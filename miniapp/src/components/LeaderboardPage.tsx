import { useState, useEffect } from 'react';
import { ArrowLeft, Trophy, Medal, Award, Users, TrendingUp, Filter } from 'lucide-react';
import { useAuth } from '../contexts/AuthContext';
import { userAPI } from '../lib/api';

interface LeaderboardUser {
  _id: string;
  rank: number;
  full_name: string;
  username?: string;
  profile_picture?: string;
  stream: 'natural' | 'social';
  stats: {
    total_exams_taken: number;
    average_score: number;
    total_practice_sessions: number;
  };
  leaderboard_score: number;
}

interface UserRank {
  rank: number | null;
  total_users: number;
  score: number;
  message?: string;
}

interface LeaderboardPageProps {
  onBack: () => void;
}

export function LeaderboardPage({ onBack }: LeaderboardPageProps) {
  const { user } = useAuth();
  const [leaderboard, setLeaderboard] = useState<LeaderboardUser[]>([]);
  const [userRank, setUserRank] = useState<UserRank | null>(null);
  const [loading, setLoading] = useState(true);
  const [selectedStream, setSelectedStream] = useState<'all' | 'natural' | 'social'>('all');
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadLeaderboard();
    loadUserRank();
  }, [selectedStream]);

  const loadLeaderboard = async () => {
    try {
      setLoading(true);
      setError(null);
      
      const stream = selectedStream === 'all' ? undefined : selectedStream;
      const data = await userAPI.getLeaderboard(stream, 20);
      setLeaderboard(data);
    } catch (error) {
      console.error('Error loading leaderboard:', error);
      setError('Failed to load leaderboard');
    } finally {
      setLoading(false);
    }
  };

  const loadUserRank = async () => {
    try {
      const data = await userAPI.getUserRank();
      setUserRank(data);
    } catch (error) {
      console.error('Error loading user rank:', error);
    }
  };

  const getRankIcon = (rank: number) => {
    if (rank === 1) return <Trophy className="w-6 h-6 text-yellow-500" />;
    if (rank === 2) return <Medal className="w-6 h-6 text-gray-400" />;
    if (rank === 3) return <Award className="w-6 h-6 text-amber-600" />;
    return <span className="w-6 h-6 flex items-center justify-center text-slate-600 font-bold text-sm">#{rank}</span>;
  };

  const getRankBadgeColor = (rank: number) => {
    if (rank === 1) return 'bg-gradient-to-r from-yellow-400 to-yellow-600';
    if (rank === 2) return 'bg-gradient-to-r from-gray-300 to-gray-500';
    if (rank === 3) return 'bg-gradient-to-r from-amber-400 to-amber-600';
    return 'bg-gradient-to-r from-slate-400 to-slate-600';
  };

  const formatScore = (score: number) => {
    return Math.round(score * 10) / 10;
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50 dark:from-slate-900 dark:to-slate-800">
      {/* Header */}
      <div className="bg-gradient-to-r from-purple-600 via-blue-600 to-indigo-600 text-white p-4 pb-6">
        <div className="flex items-center justify-between mb-4">
          <button
            onClick={onBack}
            className="w-10 h-10 flex items-center justify-center rounded-full bg-white/20 hover:bg-white/30 transition-colors backdrop-blur-sm"
          >
            <ArrowLeft className="w-5 h-5" />
          </button>
          <h1 className="text-xl font-bold">Leaderboard</h1>
          <div className="w-10"></div>
        </div>

        {/* Stream Filter */}
        <div className="flex gap-2">
          <button
            onClick={() => setSelectedStream('all')}
            className={`px-4 py-2 rounded-full text-sm font-medium transition-all ${
              selectedStream === 'all'
                ? 'bg-white text-purple-600 shadow-lg'
                : 'bg-white/20 text-white hover:bg-white/30'
            }`}
          >
            <Users className="w-4 h-4 inline mr-2" />
            All
          </button>
          <button
            onClick={() => setSelectedStream('natural')}
            className={`px-4 py-2 rounded-full text-sm font-medium transition-all ${
              selectedStream === 'natural'
                ? 'bg-white text-purple-600 shadow-lg'
                : 'bg-white/20 text-white hover:bg-white/30'
            }`}
          >
            Natural
          </button>
          <button
            onClick={() => setSelectedStream('social')}
            className={`px-4 py-2 rounded-full text-sm font-medium transition-all ${
              selectedStream === 'social'
                ? 'bg-white text-purple-600 shadow-lg'
                : 'bg-white/20 text-white hover:bg-white/30'
            }`}
          >
            Social
          </button>
        </div>
      </div>

      <div className="p-4 space-y-4">
        {/* User's Rank Card */}
        {userRank && (
          <div className="bg-white dark:bg-slate-800 rounded-2xl p-6 shadow-lg border border-slate-200 dark:border-slate-700">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-lg font-bold text-slate-800 dark:text-white">Your Rank</h2>
              <TrendingUp className="w-5 h-5 text-blue-600" />
            </div>
            
            {userRank.rank ? (
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-4">
                  {getRankIcon(userRank.rank)}
                  <div>
                    <p className="text-2xl font-bold text-slate-800 dark:text-white">#{userRank.rank}</p>
                    <p className="text-sm text-slate-600 dark:text-slate-400">
                      out of {userRank.total_users} users
                    </p>
                  </div>
                </div>
                <div className="text-right">
                  <p className="text-lg font-semibold text-blue-600">{formatScore(userRank.score)}</p>
                  <p className="text-xs text-slate-500">Score</p>
                </div>
              </div>
            ) : (
              <div className="text-center py-4">
                <p className="text-slate-600 dark:text-slate-400 mb-2">
                  {userRank.message || "You haven't taken any exams yet"}
                </p>
                <p className="text-sm text-slate-500">Start taking exams to see your rank!</p>
              </div>
            )}
          </div>
        )}

        {/* Leaderboard */}
        <div className="bg-white dark:bg-slate-800 rounded-2xl shadow-lg border border-slate-200 dark:border-slate-700 overflow-hidden">
          <div className="p-4 border-b border-slate-200 dark:border-slate-700">
            <h2 className="text-lg font-bold text-slate-800 dark:text-white flex items-center gap-2">
              <Trophy className="w-5 h-5 text-yellow-500" />
              Top Performers
            </h2>
          </div>

          {loading ? (
            <div className="p-8 text-center">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto mb-4"></div>
              <p className="text-slate-600 dark:text-slate-400">Loading leaderboard...</p>
            </div>
          ) : error ? (
            <div className="p-8 text-center">
              <p className="text-red-600 mb-4">{error}</p>
              <button
                onClick={loadLeaderboard}
                className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
              >
                Try Again
              </button>
            </div>
          ) : leaderboard.length === 0 ? (
            <div className="p-8 text-center">
              <Users className="w-12 h-12 text-slate-400 mx-auto mb-4" />
              <p className="text-slate-600 dark:text-slate-400 mb-2">No users found</p>
              <p className="text-sm text-slate-500">
                {selectedStream === 'all' 
                  ? 'No users have taken exams yet' 
                  : `No ${selectedStream} stream users have taken exams yet`
                }
              </p>
            </div>
          ) : (
            <div className="divide-y divide-slate-200 dark:divide-slate-700">
              {leaderboard.map((user, index) => (
                <div
                  key={user._id}
                  className={`p-4 flex items-center gap-4 ${
                    user._id === user?.id ? 'bg-blue-50 dark:bg-blue-900/20' : 'hover:bg-slate-50 dark:hover:bg-slate-700/50'
                  } transition-colors`}
                >
                  {/* Rank Badge */}
                  <div className={`w-10 h-10 rounded-full ${getRankBadgeColor(user.rank)} flex items-center justify-center text-white font-bold text-sm shadow-lg`}>
                    {user.rank <= 3 ? getRankIcon(user.rank) : user.rank}
                  </div>

                  {/* Profile Picture */}
                  <div className="w-12 h-12 rounded-full overflow-hidden border-2 border-white shadow-md">
                    <img
                      src={user.profile_picture || `https://ui-avatars.com/api/?name=${encodeURIComponent(user.full_name)}&size=128&background=3b82f6&color=fff&bold=true`}
                      alt={user.full_name}
                      className="w-full h-full object-cover"
                      onError={(e) => {
                        e.currentTarget.src = `https://ui-avatars.com/api/?name=${encodeURIComponent(user.full_name)}&size=128&background=3b82f6&color=fff&bold=true`;
                      }}
                    />
                  </div>

                  {/* User Info */}
                  <div className="flex-1 min-w-0">
                    <h3 className="font-semibold text-slate-800 dark:text-white truncate">
                      {user.full_name}
                    </h3>
                    {user.username && (
                      <p className="text-sm text-slate-500 truncate">@{user.username}</p>
                    )}
                    <div className="flex items-center gap-4 mt-1">
                      <span className="text-xs bg-slate-100 dark:bg-slate-700 text-slate-600 dark:text-slate-300 px-2 py-1 rounded-full">
                        {user.stream === 'natural' ? 'Natural Science' : 'Social Science'}
                      </span>
                      <span className="text-xs text-slate-500">
                        {user.stats.total_exams_taken} exams
                      </span>
                    </div>
                  </div>

                  {/* Score */}
                  <div className="text-right">
                    <p className="text-lg font-bold text-slate-800 dark:text-white">
                      {formatScore(user.leaderboard_score)}
                    </p>
                    <p className="text-xs text-slate-500">Score</p>
                    <p className="text-xs text-slate-500">
                      {user.stats.average_score}% avg
                    </p>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Bottom Padding */}
        <div className="h-4"></div>
      </div>
    </div>
  );
}
