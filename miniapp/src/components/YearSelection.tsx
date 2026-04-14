import { ArrowLeft, Calendar } from 'lucide-react';

interface YearSelectionProps {
  subject: string;
  onSelectYear: (year: number) => void;
  onBack: () => void;
}

export function YearSelection({ subject, onSelectYear, onBack }: YearSelectionProps) {
  // Generate years from 2000 to 2017
  const years = Array.from({ length: 18 }, (_, i) => 2000 + i);

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
              <h1 className="text-xl font-bold text-slate-800 dark:text-white">{subject}</h1>
              <p className="text-sm text-slate-600 dark:text-slate-400">Select exam year</p>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto p-6">
        <div className="mb-6 bg-blue-50 border border-blue-200 rounded-xl p-4">
          <p className="text-sm text-blue-800">
            <strong>Past Exams by Year:</strong> Select a year to view all {subject} exams from that academic year.
          </p>
        </div>

        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
          {years.map((year) => (
            <button
              key={year}
              onClick={() => onSelectYear(year)}
              className="bg-white dark:bg-slate-800 border-2 border-slate-200 dark:border-slate-700 rounded-xl p-6 hover:shadow-lg transition-all duration-300 hover:-translate-y-1 hover:border-blue-400 dark:hover:border-blue-500 group"
            >
              <div className="flex flex-col items-center gap-3">
                <div className="w-14 h-14 bg-gradient-to-br from-blue-500 to-blue-600 rounded-xl flex items-center justify-center shadow-lg group-hover:scale-110 transition-transform">
                  <Calendar className="w-7 h-7 text-white" />
                </div>
                <div className="text-center">
                  <h3 className="text-2xl font-bold text-slate-800 dark:text-white">{year}</h3>
                  <p className="text-xs text-slate-600 dark:text-slate-400 mt-1">Academic Year</p>
                </div>
              </div>
            </button>
          ))}
        </div>

        <div className="mt-8 text-center">
          <p className="text-sm text-slate-500 dark:text-slate-500">
            Can't find a specific year? More years may be added in future updates.
          </p>
        </div>
      </div>
    </div>
  );
}
