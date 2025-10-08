import { useState } from 'react';
import { ChevronLeft } from 'lucide-react';
import { Layout } from '../components/Layout';
import { Card } from '../components/Card';
import { Button } from '../components/Button';
import type { Stream, Subject, Grade, PracticeConfig, Difficulty } from '../types/question.types';
import { NATURAL_SUBJECTS, SOCIAL_SUBJECTS, GRADES, EXAM_YEARS } from '../types/question.types';
import { getTopicsBySubject } from '../data/sampleQuestions';

interface PracticeSelectionProps {
  onBack: () => void;
  onStartPractice: (config: PracticeConfig) => void;
}

export function PracticeSelection({ onBack, onStartPractice }: PracticeSelectionProps) {
  const [step, setStep] = useState<'mode' | 'stream' | 'grade' | 'subject' | 'year' | 'topics'>('mode');
  const [isPastExam, setIsPastExam] = useState<boolean | null>(null);
  const [stream, setStream] = useState<Stream | null>(null);
  const [grade, setGrade] = useState<Grade | null>(null);
  const [subject, setSubject] = useState<Subject | null>(null);
  const [selectedTopics, setSelectedTopics] = useState<string[]>([]);
  const [difficulty, setDifficulty] = useState<Difficulty | 'mixed'>('mixed');

  function handleModeSelect(mode: 'pastExam' | 'topic') {
    setIsPastExam(mode === 'pastExam');
    setStep('stream');
  }

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
    if (isPastExam) {
      setStep('year');
    } else {
      setStep('topics');
    }
  }

  function handleYearSelect(year: number) {
    if (!stream || !grade || !subject) return;

    const config: PracticeConfig = {
      stream,
      grade,
      subject,
      year,
      isPastExam: true,
    };

    onStartPractice(config);
  }

  function handleStartTopicPractice() {
    if (!stream || !grade || !subject) return;

    const config: PracticeConfig = {
      stream,
      grade,
      subject,
      topics: selectedTopics.length > 0 ? selectedTopics : undefined,
      difficulty: difficulty,
      isPastExam: false,
    };

    onStartPractice(config);
  }

  function toggleTopic(topic: string) {
    setSelectedTopics((prev) =>
      prev.includes(topic) ? prev.filter((t) => t !== topic) : [...prev, topic]
    );
  }

  function handleBack() {
    if (step === 'mode') {
      onBack();
    } else if (step === 'stream') {
      setStep('mode');
      setStream(null);
    } else if (step === 'grade') {
      setStep('stream');
      setGrade(null);
    } else if (step === 'subject') {
      setStep('grade');
      setSubject(null);
    } else if (step === 'year' || step === 'topics') {
      setStep('subject');
      setSubject(null);
    }
  }

  const subjects = stream === 'Natural' ? NATURAL_SUBJECTS : SOCIAL_SUBJECTS;
  const availableTopics = stream && subject && grade
    ? getTopicsBySubject(stream, subject, grade)
    : [];

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
              Practice Mode
            </h1>
            <p className="text-sm text-gray-600 dark:text-gray-400">
              {step === 'mode' && 'Choose practice type'}
              {step === 'stream' && 'Select your stream'}
              {step === 'grade' && 'Select your grade'}
              {step === 'subject' && 'Select your subject'}
              {step === 'year' && 'Select exam year'}
              {step === 'topics' && 'Select topics and difficulty'}
            </p>
          </div>
        </div>

        {step === 'mode' && (
          <div className="grid grid-cols-1 gap-4">
            <Card hoverable onClick={() => handleModeSelect('pastExam')} className="p-6">
              <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-2">
                Past Exams
              </h3>
              <p className="text-sm text-gray-600 dark:text-gray-400">
                Practice with complete past exam papers
              </p>
            </Card>

            <Card hoverable onClick={() => handleModeSelect('topic')} className="p-6">
              <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-2">
                By Topic
              </h3>
              <p className="text-sm text-gray-600 dark:text-gray-400">
                Practice specific topics with custom difficulty
              </p>
            </Card>
          </div>
        )}

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
          <div className="grid grid-cols-1 gap-3">
            {EXAM_YEARS.map((year) => (
              <Card
                key={year}
                hoverable
                onClick={() => handleYearSelect(year)}
                className="p-4"
              >
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
                  {year} Exam Practice
                </h3>
              </Card>
            ))}
          </div>
        )}

        {step === 'topics' && (
          <div className="space-y-6">
            <Card className="p-6">
              <h3 className="font-semibold text-gray-900 dark:text-white mb-4">
                Select Difficulty
              </h3>
              <div className="grid grid-cols-2 sm:grid-cols-4 gap-2">
                {(['easy', 'medium', 'hard', 'mixed'] as const).map((d) => (
                  <button
                    key={d}
                    onClick={() => setDifficulty(d)}
                    className={`px-4 py-2 rounded-lg font-medium transition-colors ${
                      difficulty === d
                        ? 'bg-blue-600 text-white'
                        : 'bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-300'
                    }`}
                  >
                    {d.charAt(0).toUpperCase() + d.slice(1)}
                  </button>
                ))}
              </div>
            </Card>

            <Card className="p-6">
              <h3 className="font-semibold text-gray-900 dark:text-white mb-4">
                Select Topics (Optional)
              </h3>
              {availableTopics.length > 0 ? (
                <div className="space-y-2">
                  {availableTopics.map((topic) => (
                    <button
                      key={topic}
                      onClick={() => toggleTopic(topic)}
                      className={`w-full px-4 py-2 rounded-lg text-left transition-colors ${
                        selectedTopics.includes(topic)
                          ? 'bg-green-100 dark:bg-green-900 text-green-800 dark:text-green-200'
                          : 'bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300'
                      }`}
                    >
                      {topic}
                    </button>
                  ))}
                </div>
              ) : (
                <p className="text-gray-600 dark:text-gray-400">
                  No topics available. Random questions will be selected.
                </p>
              )}
              {selectedTopics.length === 0 && availableTopics.length > 0 && (
                <p className="text-sm text-gray-500 dark:text-gray-400 mt-2">
                  Leave empty for random topics
                </p>
              )}
            </Card>

            <Button onClick={handleStartTopicPractice} fullWidth size="lg">
              Start Practice
            </Button>
          </div>
        )}
      </div>
    </Layout>
  );
}
