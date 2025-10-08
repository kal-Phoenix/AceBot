import { useState } from 'react';
import { ChevronLeft } from 'lucide-react';
import { Layout } from '../components/Layout';
import { Card } from '../components/Card';
import { Button } from '../components/Button';
import type { Stream, Subject, Grade, ExamConfig } from '../types/question.types';
import { NATURAL_SUBJECTS, SOCIAL_SUBJECTS, GRADES, EXAM_YEARS } from '../types/question.types';

interface ExamSelectionProps {
  onBack: () => void;
  onStartExam: (config: ExamConfig) => void;
}

export function ExamSelection({ onBack, onStartExam }: ExamSelectionProps) {
  const [step, setStep] = useState<'stream' | 'grade' | 'subject' | 'year'>('stream');
  const [stream, setStream] = useState<Stream | null>(null);
  const [grade, setGrade] = useState<Grade | null>(null);
  const [subject, setSubject] = useState<Subject | null>(null);

  function handleStreamSelect(selectedStream: Stream) {
    setStream(selectedStream);
    setStep('grade');
  }

  function handleGradeSelect(selectedGrade: Grade) {
    setGrade(selectedGrade);
    setStep('subject');
  }

  function handleSubjectSelect(selectedSubject: Subject) {
    setSubject(selectedSubject);
    setStep('year');
  }

  function handleYearSelect(year: number) {
    if (!stream || !grade || !subject) return;

    const config: ExamConfig = {
      stream,
      grade,
      subject,
      year,
      timeLimitSeconds: 7200,
      totalQuestions: 100,
    };

    onStartExam(config);
  }

  function handleBack() {
    if (step === 'stream') {
      onBack();
    } else if (step === 'grade') {
      setStep('stream');
      setStream(null);
    } else if (step === 'subject') {
      setStep('grade');
      setGrade(null);
    } else if (step === 'year') {
      setStep('subject');
      setSubject(null);
    }
  }

  const subjects = stream === 'Natural' ? NATURAL_SUBJECTS : SOCIAL_SUBJECTS;

  return (
    <Layout>
      <div className="space-y-6">
        <div className="flex items-center space-x-4">
          <button
            onClick={handleBack}
            className="p-2 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-lg transition-colors"
          >
            <ChevronLeft className="w-6 h-6 text-gray-700 dark:text-gray-300" />
          </button>
          <div>
            <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
              Exam Mode
            </h1>
            <p className="text-sm text-gray-600 dark:text-gray-400">
              {step === 'stream' && 'Select your stream'}
              {step === 'grade' && 'Select your grade'}
              {step === 'subject' && 'Select your subject'}
              {step === 'year' && 'Select exam year'}
            </p>
          </div>
        </div>

        {step === 'stream' && (
          <div className="grid grid-cols-1 gap-4">
            <Card hoverable onClick={() => handleStreamSelect('Natural')} className="p-6">
              <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-2">
                Natural Sciences
              </h3>
              <p className="text-sm text-gray-600 dark:text-gray-400">
                English, Maths, SAT, Chemistry, Biology, Physics
              </p>
            </Card>

            <Card hoverable onClick={() => handleStreamSelect('Social')} className="p-6">
              <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-2">
                Social Sciences
              </h3>
              <p className="text-sm text-gray-600 dark:text-gray-400">
                English, Maths, SAT, History, Geography, Economics
              </p>
            </Card>
          </div>
        )}

        {step === 'grade' && (
          <div className="grid grid-cols-2 gap-4">
            {GRADES.map((g) => (
              <Card
                key={g}
                hoverable
                onClick={() => handleGradeSelect(g)}
                className="p-6 text-center"
              >
                <h3 className="text-2xl font-bold text-gray-900 dark:text-white">
                  Grade {g}
                </h3>
              </Card>
            ))}
          </div>
        )}

        {step === 'subject' && (
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            {subjects.map((s) => (
              <Card
                key={s}
                hoverable
                onClick={() => handleSubjectSelect(s)}
                className="p-6 text-center"
              >
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
                  {s}
                </h3>
              </Card>
            ))}
          </div>
        )}

        {step === 'year' && (
          <div className="space-y-4">
            <Card className="p-6 bg-blue-50 dark:bg-blue-900/20">
              <h3 className="font-semibold text-gray-900 dark:text-white mb-2">
                Exam Information
              </h3>
              <ul className="space-y-1 text-sm text-gray-700 dark:text-gray-300">
                <li>• Stream: {stream}</li>
                <li>• Grade: {grade}</li>
                <li>• Subject: {subject}</li>
                <li>• Questions: 100</li>
                <li>• Time Limit: 2 hours</li>
                <li>• First attempt counts for leaderboard</li>
              </ul>
            </Card>

            <div className="grid grid-cols-1 gap-3">
              {EXAM_YEARS.map((year) => (
                <Card
                  key={year}
                  hoverable
                  onClick={() => handleYearSelect(year)}
                  className="p-4"
                >
                  <div className="flex items-center justify-between">
                    <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
                      {year} Exam
                    </h3>
                    <span className="text-sm text-gray-600 dark:text-gray-400">
                      100 questions
                    </span>
                  </div>
                </Card>
              ))}
            </div>
          </div>
        )}
      </div>
    </Layout>
  );
}
