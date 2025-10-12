import { ArrowLeft, Calendar, BookOpen } from 'lucide-react';

interface OrganizationSelectionProps {
  examType: 'past' | 'mock' | 'model';
  onSelectOrganization: (organization: 'year' | 'topic') => void;
  onBack: () => void;
}

export function OrganizationSelection({ examType, onSelectOrganization, onBack }: OrganizationSelectionProps) {
  const examTypeTitle = {
    past: 'Past Exams',
    mock: 'Mock Exams',
    model: 'Model Exams',
  }[examType];

  return (
    <div className="min-h-screen bg-slate-50 dark:bg-slate-900">
      {/* Header */}
      <div className="bg-white dark:bg-slate-800 border-b border-slate-200 dark:border-slate-700 sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-4 py-4">
          <div className="flex items-center gap-4">
            <button
              onClick={onBack}
              className="w-10 h-10 flex items-center justify-center rounded-full hover:bg-slate-100 dark:hover:bg-slate-700 transition-colors"
            >
              <ArrowLeft className="w-5 h-5 text-slate-600 dark:text-slate-400" />
            </button>
            <div>
              <h1 className="text-xl font-bold text-slate-800 dark:text-white">{examTypeTitle}</h1>
              <p className="text-sm text-slate-600 dark:text-slate-400">Choose organization method</p>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-4xl mx-auto p-6">
        <div className="grid md:grid-cols-2 gap-6">
          {/* Organized by Year */}
          <button
            onClick={() => onSelectOrganization('year')}
            className="bg-white dark:bg-slate-800 border-2 border-slate-200 dark:border-slate-700 rounded-2xl p-8 hover:shadow-lg transition-all duration-300 hover:-translate-y-1 hover:border-blue-400 dark:hover:border-blue-500 group"
          >
            <div className="w-16 h-16 bg-gradient-to-br from-blue-500 to-blue-600 rounded-xl flex items-center justify-center mb-4 shadow-lg">
              <Calendar className="w-8 h-8 text-white" />
            </div>
            <h3 className="text-xl font-bold text-slate-800 dark:text-white mb-2">Organized by Year</h3>
            <p className="text-slate-600 dark:text-slate-400 mb-4">
              Browse exams sorted by academic year
            </p>
            <ul className="space-y-2 text-sm text-slate-600 dark:text-slate-400">
              <li className="flex items-start gap-2">
                <span className="text-blue-500 mt-0.5">✓</span>
                <span>2024, 2023, 2022, etc.</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-blue-500 mt-0.5">✓</span>
                <span>Complete exam papers</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-blue-500 mt-0.5">✓</span>
                <span>Chronological order</span>
              </li>
            </ul>
          </button>

          {/* Organized by Topics */}
          <button
            onClick={() => onSelectOrganization('topic')}
            className="bg-white dark:bg-slate-800 border-2 border-slate-200 dark:border-slate-700 rounded-2xl p-8 text-left hover:shadow-lg transition-all duration-300 hover:-translate-y-1 hover:border-purple-300 dark:hover:border-purple-500"
          >
            <div className="w-16 h-16 bg-gradient-to-br from-purple-500 to-purple-600 rounded-xl flex items-center justify-center mb-4 shadow-lg">
              <BookOpen className="w-8 h-8 text-white" />
            </div>
            <h3 className="text-xl font-bold text-slate-800 dark:text-white mb-2">Organized by Topics</h3>
            <p className="text-slate-600 dark:text-slate-400 mb-4">
              Browse exams sorted by subject topics
            </p>
            <ul className="space-y-2 text-sm text-slate-600 dark:text-slate-400">
              <li className="flex items-start gap-2">
                <span className="text-purple-500 mt-0.5">✓</span>
                <span>Topic-specific questions</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-purple-500 mt-0.5">✓</span>
                <span>Focused practice</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-purple-500 mt-0.5">✓</span>
                <span>Targeted learning</span>
              </li>
            </ul>
          </button>
        </div>

        <div className="mt-6 bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-xl p-4">
          <p className="text-sm text-blue-800 dark:text-blue-300">
            <strong>Tip:</strong> Choose "By Year" for full exam practice, or "By Topics" to focus on specific areas you want to improve.
          </p>
        </div>
      </div>
    </div>
  );
}
