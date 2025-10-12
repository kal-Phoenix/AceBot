import { ArrowLeft, BookOpen } from 'lucide-react';

interface SubjectSelectionProps {
  examType: 'past' | 'mock' | 'model';
  stream: 'natural' | 'social';
  onSelectSubject: (subject: string) => void;
  onBack: () => void;
}

export function SubjectSelection({ examType, stream, onSelectSubject, onBack }: SubjectSelectionProps) {
  const subjects = stream === 'natural'
    ? ['English', 'Maths', 'SAT', 'Chemistry', 'Biology', 'Physics']
    : ['English', 'Maths', 'SAT', 'History', 'Geography', 'Economics'];

  const examTypeTitle = {
    past: 'Past Exams',
    mock: 'Mock Exams',
    model: 'Model Exams',
  }[examType];

  const subjectColors = [
    'from-blue-500 to-blue-600',
    'from-purple-500 to-purple-600',
    'from-green-500 to-green-600',
    'from-orange-500 to-orange-600',
    'from-pink-500 to-pink-600',
    'from-indigo-500 to-indigo-600',
  ];

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
              <p className="text-sm text-slate-600 dark:text-slate-400">Select a subject</p>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto p-6">
        <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
          {subjects.map((subject, index) => (
            <button
              key={subject}
              onClick={() => onSelectSubject(subject)}
              className="bg-white dark:bg-slate-800 border-2 border-slate-200 dark:border-slate-700 rounded-xl p-6 hover:shadow-lg transition-all duration-300 hover:-translate-y-1 hover:border-blue-400 dark:hover:border-blue-500"
            >
              <div className={`w-14 h-14 bg-gradient-to-br ${subjectColors[index % subjectColors.length]} rounded-xl flex items-center justify-center mb-4 mx-auto shadow-lg`}>
                <BookOpen className="w-7 h-7 text-white" />
              </div>
              <h3 className="text-lg font-bold text-slate-800 dark:text-white text-center">{subject}</h3>
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}
