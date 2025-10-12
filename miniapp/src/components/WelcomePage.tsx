import { Sparkles, BookOpen, Trophy, TrendingUp } from 'lucide-react';

interface WelcomePageProps {
  onGetStarted: () => void;
}

export function WelcomePage({ onGetStarted }: WelcomePageProps) {
  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 via-blue-50 to-indigo-50 dark:from-slate-900 dark:via-slate-800 dark:to-slate-900 flex items-center justify-center p-4">
      <div className="w-full max-w-md">
        {/* Logo/Icon */}
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-24 h-24 bg-gradient-to-br from-purple-500 via-blue-500 to-indigo-600 rounded-3xl shadow-2xl mb-6 relative">
            <Sparkles className="w-12 h-12 text-white" />
            <div className="absolute inset-0 bg-gradient-to-br from-purple-400 via-blue-400 to-indigo-500 rounded-3xl opacity-50 animate-pulse"></div>
          </div>
          <h1 className="text-3xl font-bold text-slate-800 dark:text-white mb-3">
            Exam Platform
          </h1>
          <p className="text-base text-slate-600 dark:text-slate-400 mb-8 leading-relaxed">
            Master your subjects with intelligent practice and comprehensive exams
          </p>
        </div>

        {/* Features */}
        <div className="bg-white dark:bg-slate-800 rounded-3xl p-6 shadow-2xl border border-slate-200 dark:border-slate-700 mb-8 backdrop-blur-sm">
          <div className="space-y-5">
            <div className="flex items-start gap-4">
              <div className="w-12 h-12 bg-gradient-to-br from-blue-100 to-blue-200 dark:from-blue-900/30 dark:to-blue-800/30 rounded-2xl flex items-center justify-center flex-shrink-0 shadow-lg">
                <BookOpen className="w-6 h-6 text-blue-600" />
              </div>
              <div>
                <h3 className="font-bold text-slate-800 dark:text-white mb-2">Smart Learning</h3>
                <p className="text-sm text-slate-600 dark:text-slate-400 leading-relaxed">
                  Practice with instant feedback or take timed exams to challenge yourself
                </p>
              </div>
            </div>

            <div className="flex items-start gap-4">
              <div className="w-12 h-12 bg-gradient-to-br from-yellow-100 to-orange-200 dark:from-yellow-900/30 dark:to-orange-800/30 rounded-2xl flex items-center justify-center flex-shrink-0 shadow-lg">
                <Trophy className="w-6 h-6 text-yellow-600" />
              </div>
              <div>
                <h3 className="font-bold text-slate-800 dark:text-white mb-2">Track Progress</h3>
                <p className="text-sm text-slate-600 dark:text-slate-400 leading-relaxed">
                  Monitor your performance and compete with others on the leaderboard
                </p>
              </div>
            </div>

            <div className="flex items-start gap-4">
              <div className="w-12 h-12 bg-gradient-to-br from-green-100 to-emerald-200 dark:from-green-900/30 dark:to-emerald-800/30 rounded-2xl flex items-center justify-center flex-shrink-0 shadow-lg">
                <TrendingUp className="w-6 h-6 text-green-600" />
              </div>
              <div>
                <h3 className="font-bold text-slate-800 dark:text-white mb-2">Multiple Formats</h3>
                <p className="text-sm text-slate-600 dark:text-slate-400 leading-relaxed">
                  Access past exams, mock tests, and model papers for complete preparation
                </p>
              </div>
            </div>
          </div>
        </div>

        {/* Get Started Button */}
        <button
          onClick={onGetStarted}
          className="w-full py-4 bg-gradient-to-r from-purple-600 via-blue-600 to-indigo-600 text-white rounded-2xl font-bold text-lg shadow-2xl hover:shadow-3xl transform hover:scale-[1.02] transition-all duration-300 relative overflow-hidden"
        >
          <span className="relative z-10">Get Started</span>
          <div className="absolute inset-0 bg-gradient-to-r from-purple-500 via-blue-500 to-indigo-500 opacity-0 hover:opacity-100 transition-opacity duration-300"></div>
        </button>

        <p className="text-center text-sm text-slate-500 dark:text-slate-400 mt-6">
          Choose your stream and start your learning journey! 🚀
        </p>
      </div>
    </div>
  );
}
