import { useState, useEffect } from 'react';
import { Lightbulb, Flag, Grid3x3, ChevronLeft, ChevronRight, Clock } from 'lucide-react';
import { Layout } from '../components/Layout';
import { Card } from '../components/Card';
import { Button } from '../components/Button';
import type { Question, UserAnswer, ExamConfig, PracticeConfig } from '../types/question.types';

interface QuestionInterfaceProps {
  questions: Question[];
  config: ExamConfig | PracticeConfig;
  isPracticeMode: boolean;
  onComplete: (answers: UserAnswer[], timeSpent: number) => void;
  onBack: () => void;
}

export function QuestionInterface({
  questions,
  config,
  isPracticeMode,
  onComplete,
  onBack,
}: QuestionInterfaceProps) {
  const [currentIndex, setCurrentIndex] = useState(0);
  const [answers, setAnswers] = useState<UserAnswer[]>(() =>
    questions.map((q) => ({
      questionId: q.id,
      selectedAnswer: null,
      isCorrect: false,
      usedHint: false,
      isFlagged: false,
      timeSpent: 0,
    }))
  );
  const [showHint, setShowHint] = useState(false);
  const [showExplanation, setShowExplanation] = useState(false);
  const [showGrid, setShowGrid] = useState(false);
  const [startTime] = useState(Date.now());
  const [timeRemaining, setTimeRemaining] = useState<number | null>(
    !isPracticeMode && 'timeLimitSeconds' in config ? config.timeLimitSeconds : null
  );

  const currentQuestion = questions[currentIndex];
  const currentAnswer = answers[currentIndex];

  useEffect(() => {
    if (timeRemaining === null) return;

    const timer = setInterval(() => {
      setTimeRemaining((prev) => {
        if (prev === null || prev <= 0) {
          clearInterval(timer);
          handleSubmit();
          return 0;
        }
        return prev - 1;
      });
    }, 1000);

    return () => clearInterval(timer);
  }, [timeRemaining]);

  function formatTime(seconds: number): string {
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    const secs = seconds % 60;
    return `${hours.toString().padStart(2, '0')}:${minutes
      .toString()
      .padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  }

  function handleAnswerSelect(answerIndex: number) {
    const newAnswers = [...answers];
    const isCorrect = answerIndex === currentQuestion.correctAnswer;

    newAnswers[currentIndex] = {
      ...newAnswers[currentIndex],
      selectedAnswer: answerIndex,
      isCorrect,
    };

    setAnswers(newAnswers);

    if (isPracticeMode) {
      setShowExplanation(true);
    } else {
      setShowHint(false);
    }
  }

  function toggleHint() {
    if (!showHint) {
      const newAnswers = [...answers];
      newAnswers[currentIndex] = {
        ...newAnswers[currentIndex],
        usedHint: true,
      };
      setAnswers(newAnswers);
    }
    setShowHint(!showHint);
  }

  function toggleFlag() {
    const newAnswers = [...answers];
    newAnswers[currentIndex] = {
      ...newAnswers[currentIndex],
      isFlagged: !newAnswers[currentIndex].isFlagged,
    };
    setAnswers(newAnswers);
  }

  function handleNext() {
    if (isPracticeMode && currentAnswer.selectedAnswer !== null) {
      setShowExplanation(false);
    }
    if (currentIndex < questions.length - 1) {
      setCurrentIndex(currentIndex + 1);
      setShowHint(false);
    }
  }

  function handlePrevious() {
    if (currentIndex > 0) {
      setCurrentIndex(currentIndex - 1);
      setShowHint(false);
      if (isPracticeMode) {
        setShowExplanation(answers[currentIndex - 1].selectedAnswer !== null);
      }
    }
  }

  function handleGridSelect(index: number) {
    setCurrentIndex(index);
    setShowGrid(false);
    setShowHint(false);
    if (isPracticeMode) {
      setShowExplanation(answers[index].selectedAnswer !== null);
    }
  }

  function handleSubmit() {
    if (!isPracticeMode) {
      const unansweredCount = answers.filter((a) => a.selectedAnswer === null).length;
      const flaggedUnanswered = answers.filter(
        (a) => a.isFlagged && a.selectedAnswer === null
      ).length;

      if (flaggedUnanswered > 0) {
        alert(`You have ${flaggedUnanswered} red-flagged question(s) unanswered. Please answer all flagged questions before submitting.`);
        return;
      }

      if (unansweredCount > 0) {
        const confirmed = confirm(
          `You have ${unansweredCount} unanswered question(s). Are you sure you want to submit?`
        );
        if (!confirmed) return;
      }
    }

    const totalTime = Math.floor((Date.now() - startTime) / 1000);
    onComplete(answers, totalTime);
  }

  const answeredCount = answers.filter((a) => a.selectedAnswer !== null).length;
  const flaggedCount = answers.filter((a) => a.isFlagged).length;

  return (
    <Layout showThemeToggle={false}>
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <button
            onClick={onBack}
            className="p-2 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-lg transition-colors"
          >
            <ChevronLeft className="w-6 h-6 text-gray-700 dark:text-gray-300" />
          </button>

          <div className="flex items-center space-x-4">
            {timeRemaining !== null && (
              <div className="flex items-center space-x-2 text-gray-700 dark:text-gray-300">
                <Clock className="w-5 h-5" />
                <span className="font-mono font-semibold">
                  {formatTime(timeRemaining)}
                </span>
              </div>
            )}

            <button
              onClick={() => setShowGrid(!showGrid)}
              className="p-2 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-lg transition-colors relative"
            >
              <Grid3x3 className="w-5 h-5 text-gray-700 dark:text-gray-300" />
              {flaggedCount > 0 && (
                <span className="absolute -top-1 -right-1 w-5 h-5 bg-red-500 text-white text-xs rounded-full flex items-center justify-center">
                  {flaggedCount}
                </span>
              )}
            </button>
          </div>
        </div>

        {showGrid && (
          <Card className="p-4">
            <div className="grid grid-cols-5 sm:grid-cols-10 gap-2">
              {answers.map((answer, index) => (
                <button
                  key={index}
                  onClick={() => handleGridSelect(index)}
                  className={`aspect-square rounded-lg font-semibold transition-colors ${
                    index === currentIndex
                      ? 'bg-blue-600 text-white'
                      : answer.isFlagged
                      ? 'bg-red-500 text-white'
                      : answer.selectedAnswer !== null
                      ? 'bg-green-500 text-white'
                      : 'bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-300'
                  }`}
                >
                  {index + 1}
                </button>
              ))}
            </div>
            <div className="mt-4 flex flex-wrap gap-4 text-sm">
              <div className="flex items-center space-x-2">
                <div className="w-4 h-4 bg-green-500 rounded"></div>
                <span className="text-gray-700 dark:text-gray-300">Answered</span>
              </div>
              <div className="flex items-center space-x-2">
                <div className="w-4 h-4 bg-red-500 rounded"></div>
                <span className="text-gray-700 dark:text-gray-300">Flagged</span>
              </div>
              <div className="flex items-center space-x-2">
                <div className="w-4 h-4 bg-gray-200 dark:bg-gray-700 rounded"></div>
                <span className="text-gray-700 dark:text-gray-300">Unanswered</span>
              </div>
            </div>
          </Card>
        )}

        <Card className="p-6">
          <div className="flex items-start justify-between mb-4">
            <div className="flex-1">
              <span className="text-sm text-gray-600 dark:text-gray-400">
                Question {currentIndex + 1} of {questions.length}
              </span>
              <h2 className="text-xl font-semibold text-gray-900 dark:text-white mt-1">
                {currentQuestion.questionText}
              </h2>
              {currentQuestion.questionImage && (
                <img
                  src={currentQuestion.questionImage}
                  alt="Question"
                  className="mt-4 rounded-lg max-w-full"
                />
              )}
            </div>

            <div className="flex space-x-2 ml-4">
              <button
                onClick={toggleHint}
                className={`p-2 rounded-lg transition-colors ${
                  showHint
                    ? 'bg-yellow-100 dark:bg-yellow-900'
                    : 'hover:bg-gray-100 dark:hover:bg-gray-700'
                }`}
              >
                <Lightbulb
                  className={`w-5 h-5 ${
                    showHint ? 'text-yellow-600 dark:text-yellow-400' : 'text-gray-600 dark:text-gray-400'
                  }`}
                />
              </button>

              <button
                onClick={toggleFlag}
                className={`p-2 rounded-lg transition-colors ${
                  currentAnswer.isFlagged
                    ? 'bg-red-100 dark:bg-red-900'
                    : 'hover:bg-gray-100 dark:hover:bg-gray-700'
                }`}
              >
                <Flag
                  className={`w-5 h-5 ${
                    currentAnswer.isFlagged ? 'text-red-600 dark:text-red-400 fill-current' : 'text-gray-600 dark:text-gray-400'
                  }`}
                />
              </button>
            </div>
          </div>

          {showHint && (
            <div className="mb-4 p-4 bg-yellow-50 dark:bg-yellow-900/20 rounded-lg border-l-4 border-yellow-400">
              <p className="text-sm text-yellow-800 dark:text-yellow-200">
                <strong>Hint:</strong> {currentQuestion.hint}
              </p>
            </div>
          )}

          <div className="space-y-3">
            {currentQuestion.options.map((option, index) => {
              const isSelected = currentAnswer.selectedAnswer === index;
              const isCorrect = index === currentQuestion.correctAnswer;
              const showCorrectAnswer = isPracticeMode && showExplanation;

              return (
                <button
                  key={index}
                  onClick={() => handleAnswerSelect(index)}
                  disabled={isPracticeMode && currentAnswer.selectedAnswer !== null}
                  className={`w-full p-4 rounded-lg text-left transition-all ${
                    isSelected && showCorrectAnswer && isCorrect
                      ? 'bg-green-100 dark:bg-green-900 border-2 border-green-500'
                      : isSelected && showCorrectAnswer && !isCorrect
                      ? 'bg-red-100 dark:bg-red-900 border-2 border-red-500'
                      : isSelected
                      ? 'bg-blue-100 dark:bg-blue-900 border-2 border-blue-500'
                      : showCorrectAnswer && isCorrect
                      ? 'bg-green-100 dark:bg-green-900 border-2 border-green-500'
                      : 'bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600'
                  }`}
                >
                  <div className="flex items-center space-x-3">
                    <span className="font-semibold text-gray-700 dark:text-gray-300">
                      {String.fromCharCode(65 + index)}.
                    </span>
                    <span className="text-gray-900 dark:text-white">{option.text}</span>
                  </div>
                  {option.image && (
                    <img
                      src={option.image}
                      alt={`Option ${String.fromCharCode(65 + index)}`}
                      className="mt-2 ml-8 rounded max-w-xs"
                    />
                  )}
                </button>
              );
            })}
          </div>

          {isPracticeMode && showExplanation && (
            <div className="mt-4 p-4 bg-blue-50 dark:bg-blue-900/20 rounded-lg border-l-4 border-blue-400">
              <p className="text-sm text-blue-800 dark:text-blue-200">
                <strong>Explanation:</strong> {currentQuestion.explanation}
              </p>
            </div>
          )}
        </Card>

        <div className="flex items-center justify-between">
          <Button
            onClick={handlePrevious}
            disabled={currentIndex === 0}
            variant="secondary"
          >
            <ChevronLeft className="w-4 h-4 inline mr-1" />
            Previous
          </Button>

          <span className="text-sm text-gray-600 dark:text-gray-400">
            {answeredCount} / {questions.length} answered
          </span>

          {currentIndex < questions.length - 1 ? (
            <Button onClick={handleNext} variant="secondary">
              Next
              <ChevronRight className="w-4 h-4 inline ml-1" />
            </Button>
          ) : (
            <Button onClick={handleSubmit} variant="primary">
              Submit
            </Button>
          )}
        </div>
      </div>
    </Layout>
  );
}
