import { useAuth } from '../contexts/AuthContext';
import {
  Award,
  TrendingUp,
  Clock,
  ChevronRight,
  LogOut,
  Lock,
  HelpCircle,
  Download,
  Share2,
  ArrowLeft,
} from 'lucide-react';

interface ProfilePageProps {
  onBack?: () => void;
  onNavigate?: (page: 'progress' | 'leaderboard' | 'settings') => void;
}

export function ProfilePage({ onBack, onNavigate }: ProfilePageProps = {}) {
  const { user, signOut } = useAuth();

  console.log('ProfilePage - User data:', user);
  console.log('ProfilePage - Profile picture URL:', user?.profile_picture);

  if (!user) {
    return (
      <div className="min-h-screen bg-slate-50 dark:bg-slate-900 flex items-center justify-center p-4">
        <p className="text-slate-600 dark:text-slate-400">Please log in to view your profile.</p>
      </div>
    );
  }

  const stats = user.stats || {
    total_exams_taken: 0,
    total_practice_sessions: 0,
    average_score: 0,
    best_subject: null,
    weakest_subject: null,
    total_time_spent: 0,
  };

  const formatTime = (seconds: number) => {
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    if (hours > 0) return `${hours}h ${minutes}m`;
    if (minutes > 0) return `${minutes}m`;
    return `${seconds}s`;
  };

  const handleSignOut = async () => {
    if (confirm('Are you sure you want to sign out?')) {
      await signOut();
    }
  };

  return (
    <div className="min-h-screen bg-slate-50 dark:bg-slate-900">
      {/* LinkedIn-style Header Card */}
      <div className="bg-white dark:bg-slate-800 border-b border-slate-200 dark:border-slate-700">
        {/* Cover Photo with Back Button */}
        <div className="h-32 bg-gradient-to-r from-blue-600 to-blue-500 relative z-0">
          {onBack && (
            <button
              onClick={onBack}
              className="absolute top-4 left-4 w-10 h-10 flex items-center justify-center rounded-full bg-white/20 hover:bg-white/30 transition-colors backdrop-blur-sm"
            >
              <ArrowLeft className="w-5 h-5 text-white" />
            </button>
          )}
        </div>
        
        {/* Profile Info */}
        <div className="px-4 pb-6">
          <div className="flex items-end justify-between -mt-20 mb-4">
            <div className="flex items-end gap-4 relative z-20">
              <img
                src={user.profile_picture || `https://ui-avatars.com/api/?name=${encodeURIComponent(user.full_name)}&size=256&background=0ea5e9&color=fff&bold=true`}
                alt={user.full_name}
                className="w-32 h-32 rounded-lg object-contain border-4 border-white dark:border-slate-800 shadow-lg"
                onLoad={(e) => {
                  console.log('Profile picture loaded successfully:', e.currentTarget.src);
                }}
                onError={(e) => {
                  console.log('Profile picture failed to load, using fallback:', e.currentTarget.src);
                  // Fallback if image fails to load
                  e.currentTarget.src = `https://ui-avatars.com/api/?name=${encodeURIComponent(user.full_name)}&size=256&background=0ea5e9&color=fff&bold=true`;
                }}
              />
            </div>
            <button
              onClick={() => alert('Edit profile functionality not implemented yet.')}
              className="px-4 py-2 border border-blue-600 text-blue-600 dark:text-blue-400 dark:border-blue-400 rounded-full font-semibold hover:bg-blue-50 dark:hover:bg-blue-900/20 transition-colors"
            >
              Edit profile
            </button>
          </div>

          <div className="mb-4">
            <h1 className="text-2xl font-bold text-slate-900 dark:text-white mb-1">{user.full_name}</h1>
            {user.stream && (
              <div className="flex items-center gap-2 mb-2">
                <p className="text-slate-600 dark:text-slate-400">
                  {user.stream === 'natural' ? '🧬 Natural Sciences Stream' : '📚 Social Sciences Stream'}
                </p>
                <div className="w-4 h-4 bg-amber-500 rounded-full flex items-center justify-center" title="Permanent Selection">
                  <span className="text-white text-xs font-bold">!</span>
                </div>
              </div>
            )}
            {user.username && (
              <p className="text-sm text-slate-500 dark:text-slate-500">@{user.username}</p>
            )}
          </div>

          {/* Stats Row */}
          <div className="flex items-center gap-6 text-sm">
            <div>
              <span className="font-semibold text-slate-900 dark:text-white">{stats.total_exams_taken}</span>
              <span className="text-slate-600 dark:text-slate-400 ml-1">exams</span>
            </div>
            <div>
              <span className="font-semibold text-slate-900 dark:text-white">{stats.total_practice_sessions}</span>
              <span className="text-slate-600 dark:text-slate-400 ml-1">practice sessions</span>
            </div>
          </div>
        </div>
      </div>

      {/* Analytics Card */}
      <div className="p-4">
        <div className="bg-white dark:bg-slate-800 rounded-lg border border-slate-200 dark:border-slate-700 p-6 mb-4">
          <h2 className="text-lg font-semibold text-slate-900 dark:text-white mb-4">Analytics</h2>
          
          <div className="grid grid-cols-2 gap-4">
            <div className="text-center p-4 bg-slate-50 dark:bg-slate-700/50 rounded-lg">
              <div className="flex justify-center mb-2">
                <TrendingUp className="text-green-600 dark:text-green-400" size={24} />
              </div>
              <p className="text-2xl font-bold text-slate-900 dark:text-white mb-1">
                {stats.average_score > 0 ? `${Math.round(stats.average_score)}%` : '—'}
              </p>
              <p className="text-sm text-slate-600 dark:text-slate-400">Average Score</p>
            </div>

            <div className="text-center p-4 bg-slate-50 dark:bg-slate-700/50 rounded-lg">
              <div className="flex justify-center mb-2">
                <Clock className="text-blue-600 dark:text-blue-400" size={24} />
              </div>
              <p className="text-2xl font-bold text-slate-900 dark:text-white mb-1">
                {formatTime(stats.total_time_spent)}
              </p>
              <p className="text-sm text-slate-600 dark:text-slate-400">Study Time</p>
            </div>
          </div>

          {(stats.best_subject || stats.weakest_subject) && (
            <div className="mt-4 pt-4 border-t border-slate-200 dark:border-slate-700">
              {stats.best_subject && (
                <div className="flex items-center justify-between mb-2">
                  <span className="text-sm text-slate-600 dark:text-slate-400">Best subject</span>
                  <span className="text-sm font-semibold text-slate-900 dark:text-white">{stats.best_subject}</span>
                </div>
              )}
              {stats.weakest_subject && (
                <div className="flex items-center justify-between">
                  <span className="text-sm text-slate-600 dark:text-slate-400">Focus area</span>
                  <span className="text-sm font-semibold text-slate-900 dark:text-white">{stats.weakest_subject}</span>
                </div>
              )}
            </div>
          )}
        </div>

        {/* Achievements */}
        {stats.total_exams_taken > 0 && (
          <div className="bg-white dark:bg-slate-800 rounded-lg border border-slate-200 dark:border-slate-700 p-6 mb-4">
            <h2 className="text-lg font-semibold text-slate-900 dark:text-white mb-4">Achievements</h2>
            
            <div className="space-y-3">
              <div className="flex items-center gap-3">
                <div className="w-12 h-12 bg-blue-100 dark:bg-blue-900/30 rounded-lg flex items-center justify-center">
                  <Award className="text-blue-600 dark:text-blue-400" size={20} />
                </div>
                <div>
                  <p className="font-medium text-slate-900 dark:text-white">First Exam Completed</p>
                  <p className="text-sm text-slate-600 dark:text-slate-400">Started your learning journey</p>
                </div>
              </div>

              {stats.average_score >= 80 && (
                <div className="flex items-center gap-3">
                  <div className="w-12 h-12 bg-green-100 dark:bg-green-900/30 rounded-lg flex items-center justify-center">
                    <Award className="text-green-600 dark:text-green-400" size={20} />
                  </div>
                  <div>
                    <p className="font-medium text-slate-900 dark:text-white">High Achiever</p>
                    <p className="text-sm text-slate-600 dark:text-slate-400">Maintained 80%+ average</p>
                  </div>
                </div>
              )}
            </div>
          </div>
        )}

        {/* Stream Information */}
        {user.stream && (
          <div className="bg-white dark:bg-slate-800 rounded-lg border border-slate-200 dark:border-slate-700 mb-4 overflow-hidden">
            <div className="px-6 py-4 border-b border-slate-200 dark:border-slate-700">
              <h2 className="text-lg font-semibold text-slate-900 dark:text-white">Academic Stream</h2>
            </div>

            <div className="px-6 py-4">
              <div className="flex items-center gap-3 mb-3">
                <div className="w-12 h-12 bg-blue-100 dark:bg-blue-900/30 rounded-lg flex items-center justify-center">
                  {user.stream === 'natural' ? (
                    <span className="text-2xl">🧬</span>
                  ) : (
                    <span className="text-2xl">📚</span>
                  )}
                </div>
                <div>
                  <p className="font-semibold text-slate-900 dark:text-white">
                    {user.stream === 'natural' ? 'Natural Sciences' : 'Social Sciences'}
                  </p>
                  <p className="text-sm text-slate-600 dark:text-slate-400">Your selected stream</p>
                </div>
              </div>
              
              <div className="bg-amber-50 dark:bg-amber-900/20 border border-amber-200 dark:border-amber-700 rounded-lg p-3">
                <div className="flex items-start gap-2">
                  <div className="w-5 h-5 bg-amber-500 rounded-full flex items-center justify-center flex-shrink-0 mt-0.5">
                    <span className="text-white text-xs font-bold">!</span>
                  </div>
                  <div>
                    <p className="text-sm font-medium text-amber-800 dark:text-amber-200 mb-1">
                      Permanent Selection
                    </p>
                    <p className="text-xs text-amber-700 dark:text-amber-300">
                      This stream selection cannot be changed. Contact admin if you need assistance.
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Settings */}
        <div className="bg-white dark:bg-slate-800 rounded-lg border border-slate-200 dark:border-slate-700 mb-4 overflow-hidden">
          <div className="px-6 py-4 border-b border-slate-200 dark:border-slate-700">
            <h2 className="text-lg font-semibold text-slate-900 dark:text-white">Settings</h2>
          </div>

          <button
            onClick={() => onNavigate?.('progress')}
            className="w-full px-6 py-4 flex items-center justify-between hover:bg-slate-50 dark:hover:bg-slate-700/50 transition-colors border-b border-slate-200 dark:border-slate-700"
          >
            <div className="flex items-center gap-3">
              <Lock className="text-slate-600 dark:text-slate-400" size={20} />
              <div className="text-left">
                <p className="font-medium text-slate-900 dark:text-white">Privacy</p>
                <p className="text-sm text-slate-600 dark:text-slate-400">Control your data</p>
              </div>
            </div>
            <ChevronRight size={20} className="text-slate-400" />
          </button>

          <button
            onClick={() => onNavigate?.('leaderboard')}
            className="w-full px-6 py-4 flex items-center justify-between hover:bg-slate-50 dark:hover:bg-slate-700/50 transition-colors"
          >
            <div className="flex items-center gap-3">
              <HelpCircle className="text-slate-600 dark:text-slate-400" size={20} />
              <div className="text-left">
                <p className="font-medium text-slate-900 dark:text-white">Help & Support</p>
                <p className="text-sm text-slate-600 dark:text-slate-400">Get assistance</p>
              </div>
            </div>
            <ChevronRight size={20} className="text-slate-400" />
          </button>
        </div>

        {/* Actions */}
        <div className="bg-white dark:bg-slate-800 rounded-lg border border-slate-200 dark:border-slate-700 mb-4 overflow-hidden">
          <button
            onClick={() => alert('Download functionality not implemented yet.')}
            className="w-full px-6 py-4 flex items-center justify-between hover:bg-slate-50 dark:hover:bg-slate-700/50 transition-colors border-b border-slate-200 dark:border-slate-700"
          >
            <div className="flex items-center gap-3">
              <Download className="text-slate-600 dark:text-slate-400" size={20} />
              <p className="font-medium text-slate-900 dark:text-white">Download your data</p>
            </div>
            <ChevronRight size={20} className="text-slate-400" />
          </button>

          <button
            onClick={() => {
              if (navigator.share) {
                navigator.share({
                  title: 'My Profile',
                  url: window.location.href,
                });
              } else {
                navigator.clipboard.writeText(window.location.href);
                alert('Profile link copied to clipboard!');
              }
            }}
            className="w-full px-6 py-4 flex items-center justify-between hover:bg-slate-50 dark:hover:bg-slate-700/50 transition-colors"
          >
            <div className="flex items-center gap-3">
              <Share2 className="text-slate-600 dark:text-slate-400" size={20} />
              <p className="font-medium text-slate-900 dark:text-white">Share profile</p>
            </div>
            <ChevronRight size={20} className="text-slate-400" />
          </button>
        </div>

        {/* Sign Out */}
        <button
          onClick={handleSignOut}
          className="w-full px-6 py-3 bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-lg font-semibold text-slate-700 dark:text-slate-300 hover:bg-slate-50 dark:hover:bg-slate-700/50 transition-colors flex items-center justify-center gap-2"
        >
          <LogOut size={18} />
          Sign out
        </button>

        {/* Footer */}
        <div className="text-center mt-6 pb-6">
          <p className="text-xs text-slate-500 dark:text-slate-500">
            Member since {user.created_at ? new Date(user.created_at).toLocaleDateString('en-US', { month: 'long', year: 'numeric' }) : 'Recently'}
          </p>
        </div>
      </div>
    </div>
  );
}
