import { BookOpen, FileText, ClipboardList, TrendingUp, Settings, Trophy, Award } from 'lucide-react';
import { useAuth } from '../contexts/AuthContext';
import { ThemeToggle } from './ThemeToggle';

interface DashboardNewProps {
  onSelectExamType: (type: 'past' | 'mock' | 'model') => void;
  onNavigate: (page: 'progress' | 'leaderboard' | 'settings') => void;
}

export function Dashboard({ onSelectExamType, onNavigate }: DashboardNewProps) {
  const { user } = useAuth();

  const examTypes = [
    {
      id: 'past' as const,
      title: 'Past Exams',
      description: 'Previous examination papers',
      icon: BookOpen,
      color: 'from-blue-500 to-blue-600',
      bgColor: 'bg-blue-50',
      borderColor: 'border-blue-200',
    },
    {
      id: 'mock' as const,
      title: 'Mock Exams',
      description: 'Practice tests for preparation',
      icon: FileText,
      color: 'from-purple-500 to-purple-600',
      bgColor: 'bg-purple-50',
      borderColor: 'border-purple-200',
    },
    {
      id: 'model' as const,
      title: 'Model Exams',
      description: 'Sample examination papers',
      icon: ClipboardList,
      color: 'from-green-500 to-green-600',
      bgColor: 'bg-green-50',
      borderColor: 'border-green-200',
    },
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50 dark:from-slate-900 dark:via-slate-800 dark:to-slate-900">
      {/* Header */}
      <div className="bg-gradient-to-r from-purple-600 via-blue-600 to-indigo-600 text-white p-4 pb-6 relative overflow-hidden">
        <div className="absolute inset-0 bg-black/10"></div>
        <div className="relative">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-3">
              <button
                onClick={() => onNavigate('settings')}
                className="w-12 h-12 rounded-full overflow-hidden border-2 border-white/30 hover:border-white/50 transition-all cursor-pointer active:scale-95 flex-shrink-0 shadow-lg backdrop-blur-sm"
                aria-label="View Profile"
              >
                <img 
                  src={user?.profile_picture || `https://ui-avatars.com/api/?name=${encodeURIComponent(user?.full_name || 'User')}&size=128&background=3b82f6&color=fff&bold=true`}
                  alt={user?.full_name || 'User'}
                  className="w-full h-full object-cover"
                  onError={(e) => {
                    e.currentTarget.src = `https://ui-avatars.com/api/?name=${encodeURIComponent(user?.full_name || 'User')}&size=128&background=3b82f6&color=fff&bold=true`;
                  }}
                />
              </button>
              <div>
                <h1 className="text-xl font-bold">Welcome back!</h1>
                <p className="text-blue-100 text-sm">{user?.full_name}</p>
              </div>
            </div>
            <ThemeToggle />
          </div>
          
          {user?.stream && (
            <div className="inline-flex items-center gap-2 bg-white/20 backdrop-blur-sm px-4 py-2 rounded-full border border-white/20">
              <span className="text-sm font-medium">
                {user.stream === 'natural' ? '🧬 Natural Science' : '📚 Social Science'}
              </span>
            </div>
          )}
        </div>
      </div>

      <div className="p-4 space-y-6">
        {/* Stats Summary - Mobile Optimized */}
        <div className="grid grid-cols-2 gap-3">
          <div className="bg-white dark:bg-slate-800 rounded-2xl p-4 shadow-lg border border-slate-200 dark:border-slate-700">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 bg-blue-100 dark:bg-blue-900/30 rounded-xl flex items-center justify-center">
                <BookOpen className="w-5 h-5 text-blue-600" />
              </div>
              <div>
                <p className="text-xs text-slate-600 dark:text-slate-400">Exams Taken</p>
                <p className="text-lg font-bold text-slate-800 dark:text-white">
                  {user?.stats?.total_exams_taken || 0}
                </p>
              </div>
            </div>
          </div>
          
          <div className="bg-white dark:bg-slate-800 rounded-2xl p-4 shadow-lg border border-slate-200 dark:border-slate-700">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 bg-green-100 dark:bg-green-900/30 rounded-xl flex items-center justify-center">
                <TrendingUp className="w-5 h-5 text-green-600" />
              </div>
              <div>
                <p className="text-xs text-slate-600 dark:text-slate-400">Average Score</p>
                <p className="text-lg font-bold text-slate-800 dark:text-white">
                  {user?.stats?.average_score || 0}%
                </p>
              </div>
            </div>
          </div>
          
          <div className="bg-white dark:bg-slate-800 rounded-2xl p-4 shadow-lg border border-slate-200 dark:border-slate-700">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 bg-purple-100 dark:bg-purple-900/30 rounded-xl flex items-center justify-center">
                <FileText className="w-5 h-5 text-purple-600" />
              </div>
              <div>
                <p className="text-xs text-slate-600 dark:text-slate-400">Practice Sessions</p>
                <p className="text-lg font-bold text-slate-800 dark:text-white">
                  {user?.stats?.total_practice_sessions || 0}
                </p>
              </div>
            </div>
          </div>
          
          <div className="bg-white dark:bg-slate-800 rounded-2xl p-4 shadow-lg border border-slate-200 dark:border-slate-700">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 bg-yellow-100 dark:bg-yellow-900/30 rounded-xl flex items-center justify-center">
                <Award className="w-5 h-5 text-yellow-600" />
              </div>
              <div>
                <p className="text-xs text-slate-600 dark:text-slate-400">Best Subject</p>
                <p className="text-sm font-bold text-slate-800 dark:text-white truncate">
                  {user?.stats?.best_subject || 'N/A'}
                </p>
              </div>
            </div>
          </div>
        </div>

        {/* Exam Types - Mobile First */}
        <div>
          <h2 className="text-lg font-bold text-slate-800 dark:text-white mb-4 px-1">Choose Exam Type</h2>
          <div className="space-y-3">
            {examTypes.map((type) => {
              const Icon = type.icon;
              return (
                <button
                  key={type.id}
                  onClick={() => onSelectExamType(type.id)}
                  className="w-full bg-white dark:bg-slate-800 border-2 border-slate-200 dark:border-slate-700 rounded-2xl p-4 text-left hover:shadow-xl transition-all duration-300 hover:-translate-y-1 hover:border-blue-400 dark:hover:border-blue-500 active:scale-98"
                >
                  <div className="flex items-center gap-4">
                    <div className={`w-12 h-12 bg-gradient-to-br ${type.color} rounded-xl flex items-center justify-center shadow-lg flex-shrink-0`}>
                      <Icon className="w-6 h-6 text-white" />
                    </div>
                    <div className="flex-1">
                      <h3 className="text-lg font-bold text-slate-800 dark:text-white mb-1">{type.title}</h3>
                      <p className="text-sm text-slate-600 dark:text-slate-400">{type.description}</p>
                    </div>
                    <div className="w-6 h-6 text-slate-400">
                      <svg className="w-full h-full" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                      </svg>
                    </div>
                  </div>
                </button>
              );
            })}
          </div>
        </div>

        {/* Quick Actions - Mobile Optimized */}
        <div>
          <h2 className="text-lg font-bold text-slate-800 dark:text-white mb-4 px-1">Quick Actions</h2>
          <div className="grid grid-cols-1 gap-3">
            <button
              onClick={() => onNavigate('leaderboard')}
              className="w-full bg-gradient-to-r from-yellow-400 to-orange-500 text-white rounded-2xl p-4 text-left hover:shadow-xl transition-all duration-300 hover:-translate-y-1 active:scale-98"
            >
              <div className="flex items-center gap-4">
                <div className="w-12 h-12 bg-white/20 rounded-xl flex items-center justify-center shadow-lg">
                  <Trophy className="w-6 h-6 text-white" />
                </div>
                <div className="flex-1">
                  <h3 className="font-bold text-white mb-1">Leaderboard</h3>
                  <p className="text-sm text-white/90">See top performers</p>
                </div>
                <div className="w-6 h-6 text-white/70">
                  <svg className="w-full h-full" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                  </svg>
                </div>
              </div>
            </button>

            <button
              onClick={() => onNavigate('progress')}
              className="w-full bg-white dark:bg-slate-800 border-2 border-slate-200 dark:border-slate-700 rounded-2xl p-4 text-left hover:shadow-xl transition-all duration-300 hover:-translate-y-1 hover:border-blue-300 dark:hover:border-blue-500 active:scale-98"
            >
              <div className="flex items-center gap-4">
                <div className="w-12 h-12 bg-blue-100 dark:bg-blue-900/30 rounded-xl flex items-center justify-center">
                  <TrendingUp className="w-6 h-6 text-blue-600" />
                </div>
                <div className="flex-1">
                  <h3 className="font-bold text-slate-800 dark:text-white mb-1">Progress & Stats</h3>
                  <p className="text-sm text-slate-600 dark:text-slate-400">View your performance</p>
                </div>
                <div className="w-6 h-6 text-slate-400">
                  <svg className="w-full h-full" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                  </svg>
                </div>
              </div>
            </button>

            <button
              onClick={() => onNavigate('settings')}
              className="w-full bg-white dark:bg-slate-800 border-2 border-slate-200 dark:border-slate-700 rounded-2xl p-4 text-left hover:shadow-xl transition-all duration-300 hover:-translate-y-1 hover:border-purple-300 dark:hover:border-purple-500 active:scale-98"
            >
              <div className="flex items-center gap-4">
                <div className="w-12 h-12 bg-purple-100 dark:bg-purple-900/30 rounded-xl flex items-center justify-center">
                  <Settings className="w-6 h-6 text-purple-600" />
                </div>
                <div className="flex-1">
                  <h3 className="font-bold text-slate-800 dark:text-white mb-1">Settings</h3>
                  <p className="text-sm text-slate-600 dark:text-slate-400">Manage preferences</p>
                </div>
                <div className="w-6 h-6 text-slate-400">
                  <svg className="w-full h-full" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                  </svg>
                </div>
              </div>
            </button>
          </div>
        </div>

        {/* Bottom Padding */}
        <div className="h-4"></div>
      </div>
    </div>
  );
}
