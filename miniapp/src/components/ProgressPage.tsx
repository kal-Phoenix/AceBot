import { useEffect, useState } from 'react';
import {
  TrendingUp,
  Calendar,
  Target,
  Award,
  BookOpen,
  Clock,
  CheckCircle2,
  ArrowLeft,
} from 'lucide-react';

interface ProgressPageProps {
  onBack?: () => void;
}

export function ProgressPage({ onBack }: ProgressPageProps = {}) {
  const [loading, setLoading] = useState(true);
  const [progress, setProgress] = useState<any>(null);

  useEffect(() => {
    loadProgress();
  }, []);

  const loadProgress = async () => {
    try {
      // Mock progress data for development
      setProgress({
        totalExams: 2,
        completedExams: 1,
        averageScore: 85,
        totalTimeSpent: '45 minutes',
        recentActivity: [
          {
            examTitle: 'JavaScript Fundamentals',
            score: 85,
            completedAt: new Date(Date.now() - 2 * 24 * 60 * 60 * 1000).toISOString(),
            timeSpent: '18 minutes'
          }
        ],
        achievements: [
          { title: 'First Exam Completed', description: 'Completed your first exam', unlocked: true },
          { title: 'Score Master', description: 'Achieved 85% or higher', unlocked: true },
          { title: 'Speed Demon', description: 'Complete an exam in under 15 minutes', unlocked: false },
          { title: 'Perfectionist', description: 'Score 100% on any exam', unlocked: false }
        ]
      });
    } catch (error) {
      console.error('Error loading progress:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-96">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-50 dark:bg-slate-900">
      {/* Header with Back Button */}
      <div className="bg-white dark:bg-slate-800 border-b border-slate-200 dark:border-slate-700">
        <div className="max-w-7xl mx-auto px-4 py-4">
          <div className="flex items-center gap-4">
            {onBack && (
              <button
                onClick={onBack}
                className="w-10 h-10 flex items-center justify-center rounded-full hover:bg-slate-100 dark:hover:bg-slate-700 transition-colors"
              >
                <ArrowLeft className="w-5 h-5 text-slate-600 dark:text-slate-400" />
              </button>
            )}
            <div>
              <h1 className="text-2xl font-bold text-slate-800 dark:text-white">Progress Overview</h1>
              <p className="text-sm text-slate-600 dark:text-slate-400">Track your learning journey</p>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 py-8">

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6">
          <div className="flex items-center gap-4">
            <div className="min-h-screen bg-slate-50 dark:bg-slate-900 rounded-lg">
              <BookOpen className="text-blue-600" size={24} />
            </div>
            <div>
              <p className="text-slate-600 text-sm">Exams Taken</p>
              <p className="text-2xl font-bold text-slate-800">{progress.completedExams}/{progress.totalExams}</p>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6">
          <div className="flex items-center gap-4">
            <div className="p-3 bg-green-100 rounded-lg">
              <TrendingUp className="text-green-600" size={24} />
            </div>
            <div>
              <p className="text-slate-600 text-sm">Average Score</p>
              <p className="text-2xl font-bold text-slate-800">{progress.averageScore}%</p>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6">
          <div className="flex items-center gap-4">
            <div className="p-3 bg-purple-100 rounded-lg">
              <Clock className="text-purple-600" size={24} />
            </div>
            <div>
              <p className="text-slate-600 text-sm">Time Invested</p>
              <p className="text-2xl font-bold text-slate-800">{progress.totalTimeSpent}</p>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6">
          <div className="flex items-center gap-4">
            <div className="p-3 bg-yellow-100 rounded-lg">
              <Award className="text-yellow-600" size={24} />
            </div>
            <div>
              <p className="text-slate-600 text-sm">Achievements</p>
              <p className="text-2xl font-bold text-slate-800">{progress.achievements.filter((a: any) => a.unlocked).length}</p>
            </div>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Recent Activity */}
        <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-8">
          <h2 className="text-xl font-bold text-slate-800 mb-6">Recent Activity</h2>

          {progress.recentActivity.length === 0 ? (
            <div className="text-center py-8">
              <Calendar className="text-slate-400 mx-auto mb-4" size={48} />
              <p className="text-sm text-slate-600 dark:text-slate-400">No exam attempts yet</p>
              <p className="text-slate-500 text-sm mt-2">Complete your first exam to see activity here</p>
            </div>
          ) : (
            <div className="space-y-4">
              {progress.recentActivity.map((activity: any, index: number) => (
                <div key={index} className="border border-slate-200 rounded-lg p-4">
                  <div className="flex items-center justify-between mb-2">
                    <h3 className="font-semibold text-slate-800">{activity.examTitle}</h3>
                    <span className={`px-2 py-1 rounded text-sm font-medium ${
                      activity.score >= 80 ? 'bg-green-100 text-green-700' :
                      activity.score >= 60 ? 'bg-yellow-100 text-yellow-700' :
                      'bg-red-100 text-red-700'
                    }`}>
                      {activity.score}%
                    </span>
                  </div>
                  <div className="flex items-center gap-4 text-sm text-slate-600">
                    <div className="flex items-center gap-1">
                      <Calendar size={16} />
                      <span>{new Date(activity.completedAt).toLocaleDateString()}</span>
                    </div>
                    <div className="flex items-center gap-1">
                      <Clock size={16} />
                      <span>{activity.timeSpent}</span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Achievements */}
        <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-8">
          <h2 className="text-xl font-bold text-slate-800 mb-6">Achievements</h2>

          <div className="space-y-4">
            {progress.achievements.map((achievement: any, index: number) => (
              <div key={index} className={`border rounded-lg p-4 ${
                achievement.unlocked ? 'border-green-200 bg-green-50' : 'border-slate-200 bg-slate-50'
              }`}>
                <div className="flex items-start gap-3">
                  <div className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center ${
                    achievement.unlocked ? 'bg-green-100 text-green-600' : 'bg-slate-100 text-slate-400'
                  }`}>
                    {achievement.unlocked ? <CheckCircle2 size={16} /> : <Target size={16} />}
                  </div>
                  <div className="flex-1">
                    <h3 className={`font-semibold ${achievement.unlocked ? 'text-slate-800' : 'text-slate-600'}`}>
                      {achievement.title}
                    </h3>
                    <p className={`text-sm mt-1 ${achievement.unlocked ? 'text-slate-600' : 'text-slate-500'}`}>
                      {achievement.description}
                    </p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
      </div>
    </div>
  );
}