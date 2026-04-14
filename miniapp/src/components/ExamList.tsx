import { useState, useEffect } from 'react';
import { ArrowLeft, Clock, FileText, Play } from 'lucide-react';
import { examsAPI } from '../lib/api';

interface Exam {
  _id: string;
  title: string;
  description: string;
  duration_minutes: number;
  total_questions: number;
  passing_score: number;
  exam_type: string;
  subject: string;
}

interface ExamListProps {
  examType: 'past' | 'mock' | 'model';
  subject: string;
  stream: 'natural' | 'social';
  year?: number;
  onSelectExam: (examId: string, exam: Exam) => void;
  onBack: () => void;
}

export function ExamList({ examType, subject, stream, year, onSelectExam, onBack }: ExamListProps) {
  const [exams, setExams] = useState<Exam[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadExams();
  }, [examType, subject, stream, year]);

  const loadExams = async () => {
    try {
      setLoading(true);
      const data = await examsAPI.getByTypeAndSubject(examType, subject, stream);
      // Filter by year if provided (for past exams organized by year)
      const filteredData = year ? data.filter((exam: any) => exam.year === year) : data;
      setExams(filteredData);
    } catch (error) {
      console.error('Error loading exams:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-slate-50 dark:bg-slate-900 flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

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
              <h2 className="text-xl font-bold text-slate-800 dark:text-white mb-4">{subject}</h2>
              <p className="text-sm text-slate-600 dark:text-slate-400">
                {examType.charAt(0).toUpperCase() + examType.slice(1)} Exams
              </p>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto p-6">
        {exams.length === 0 ? (
          <div className="text-center py-16">
            <div className="w-24 h-24 bg-slate-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <FileText className="w-12 h-12 text-slate-400" />
            </div>
            <p className="text-slate-600 dark:text-slate-400 text-lg mb-2">No exams available</p>
            <p className="text-slate-500 dark:text-slate-500">Check back later for new exams</p>
          </div>
        ) : (
          <div className="space-y-4">
            {exams.map((exam) => (
              <div
                key={exam._id}
                className="bg-white dark:bg-slate-800 border-2 border-slate-200 dark:border-slate-700 rounded-xl p-6 hover:shadow-lg transition-all duration-300 hover:-translate-y-1 hover:border-blue-400 dark:hover:border-blue-500 group"
              >
                <div className="flex items-start justify-between gap-4">
                  <div className="flex-1">
                    <h3 className="text-lg font-bold text-slate-800 dark:text-white mb-2">{exam.title}</h3>
                    <p className="text-sm text-slate-600 dark:text-slate-400 mb-4">{exam.description}</p>
                    
                    <div className="flex flex-wrap gap-3">
                      <div className="flex items-center gap-2 text-sm text-slate-600 dark:text-slate-400">
                        <Clock className="w-4 h-4" />
                        <span>{exam.duration_minutes} min</span>
                      </div>
                      <div className="flex items-center gap-2 text-sm text-slate-600 dark:text-slate-400">
                        <FileText className="w-4 h-4" />
                        <span>{exam.total_questions} questions</span>
                      </div>
                      <div className="text-sm text-slate-600">
                        Pass: {exam.passing_score}%
                      </div>
                    </div>
                  </div>

                  <button
                    onClick={() => onSelectExam(exam._id, exam)}
                    className="flex items-center gap-2 px-6 py-3 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-lg font-medium hover:shadow-lg transition-all duration-300"
                  >
                    <Play className="w-4 h-4" />
                    <span>Start</span>
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
