import type { Question } from '../types/question.types';

export const sampleQuestions: Question[] = [
  {
    id: 'nat_eng_9_2024_001',
    stream: 'Natural',
    subject: 'English',
    grade: 9,
    topic: 'Grammar',
    year: 2024,
    difficulty: 'easy',
    questionText: 'Choose the correct form of the verb: "She ___ to school every day."',
    options: [
      { text: 'go' },
      { text: 'goes' },
      { text: 'going' },
      { text: 'gone' },
    ],
    correctAnswer: 1,
    hint: 'Think about subject-verb agreement with third person singular.',
    explanation: 'The correct answer is "goes" because with third person singular subjects (she, he, it), we add -s or -es to the base form of the verb in simple present tense.',
  },
  {
    id: 'nat_math_9_2024_001',
    stream: 'Natural',
    subject: 'Maths',
    grade: 9,
    topic: 'Algebra',
    year: 2024,
    difficulty: 'medium',
    questionText: 'Solve for x: 2x + 5 = 15',
    options: [
      { text: 'x = 5' },
      { text: 'x = 10' },
      { text: 'x = 7.5' },
      { text: 'x = 20' },
    ],
    correctAnswer: 0,
    hint: 'Subtract 5 from both sides first, then divide by 2.',
    explanation: '2x + 5 = 15. Subtract 5: 2x = 10. Divide by 2: x = 5.',
  },
  {
    id: 'nat_chem_10_2024_001',
    stream: 'Natural',
    subject: 'Chemistry',
    grade: 10,
    topic: 'Atomic Structure',
    year: 2024,
    difficulty: 'medium',
    questionText: 'What is the atomic number of Carbon?',
    options: [
      { text: '4' },
      { text: '6' },
      { text: '12' },
      { text: '14' },
    ],
    correctAnswer: 1,
    hint: 'The atomic number equals the number of protons in the nucleus.',
    explanation: 'Carbon has an atomic number of 6, meaning it has 6 protons in its nucleus. The mass number (12) is different from the atomic number.',
  },
  {
    id: 'nat_bio_11_2024_001',
    stream: 'Natural',
    subject: 'Biology',
    grade: 11,
    topic: 'Cell Biology',
    year: 2024,
    difficulty: 'hard',
    questionText: 'Which organelle is responsible for protein synthesis?',
    options: [
      { text: 'Mitochondria' },
      { text: 'Ribosome' },
      { text: 'Golgi apparatus' },
      { text: 'Lysosome' },
    ],
    correctAnswer: 1,
    hint: 'This organelle reads mRNA and assembles amino acids.',
    explanation: 'Ribosomes are the organelles responsible for protein synthesis. They translate mRNA sequences into amino acid chains (polypeptides).',
  },
  {
    id: 'nat_phy_12_2024_001',
    stream: 'Natural',
    subject: 'Physics',
    grade: 12,
    topic: 'Mechanics',
    year: 2024,
    difficulty: 'hard',
    questionText: 'What is Newton\'s Second Law of Motion?',
    options: [
      { text: 'An object at rest stays at rest' },
      { text: 'F = ma' },
      { text: 'For every action there is an equal and opposite reaction' },
      { text: 'Energy cannot be created or destroyed' },
    ],
    correctAnswer: 1,
    hint: 'This law relates force, mass, and acceleration.',
    explanation: 'Newton\'s Second Law states that Force equals mass times acceleration (F = ma). This fundamental equation describes how the velocity of an object changes when it is subjected to an external force.',
  },
  {
    id: 'soc_hist_9_2024_001',
    stream: 'Social',
    subject: 'History',
    grade: 9,
    topic: 'Ancient Civilizations',
    year: 2024,
    difficulty: 'easy',
    questionText: 'Which ancient civilization built the pyramids?',
    options: [
      { text: 'Romans' },
      { text: 'Greeks' },
      { text: 'Egyptians' },
      { text: 'Persians' },
    ],
    correctAnswer: 2,
    hint: 'This civilization was located along the Nile River.',
    explanation: 'The ancient Egyptians built the pyramids as tombs for their pharaohs. The most famous pyramids are located at Giza.',
  },
  {
    id: 'soc_geo_10_2024_001',
    stream: 'Social',
    subject: 'Geography',
    grade: 10,
    topic: 'Physical Geography',
    year: 2024,
    difficulty: 'medium',
    questionText: 'What is the largest ocean on Earth?',
    options: [
      { text: 'Atlantic Ocean' },
      { text: 'Indian Ocean' },
      { text: 'Pacific Ocean' },
      { text: 'Arctic Ocean' },
    ],
    correctAnswer: 2,
    hint: 'This ocean is located between Asia and the Americas.',
    explanation: 'The Pacific Ocean is the largest ocean on Earth, covering approximately 165 million square kilometers.',
  },
  {
    id: 'soc_econ_11_2024_001',
    stream: 'Social',
    subject: 'Economics',
    grade: 11,
    topic: 'Microeconomics',
    year: 2024,
    difficulty: 'hard',
    questionText: 'What happens to demand when the price of a good increases, all else being equal?',
    options: [
      { text: 'Demand increases' },
      { text: 'Demand decreases' },
      { text: 'Demand stays the same' },
      { text: 'Demand becomes zero' },
    ],
    correctAnswer: 1,
    hint: 'Think about the law of demand.',
    explanation: 'According to the law of demand, when the price of a good increases (ceteris paribus), the quantity demanded decreases. This is an inverse relationship.',
  },
];

export function getQuestionsByConfig(config: {
  stream?: string;
  subject?: string;
  grade?: number;
  year?: number;
  topic?: string;
  difficulty?: string;
}): Question[] {
  return sampleQuestions.filter((q) => {
    if (config.stream && q.stream !== config.stream) return false;
    if (config.subject && q.subject !== config.subject) return false;
    if (config.grade && q.grade !== config.grade) return false;
    if (config.year && q.year !== config.year) return false;
    if (config.topic && q.topic !== config.topic) return false;
    if (config.difficulty && q.difficulty !== config.difficulty) return false;
    return true;
  });
}

export function getRandomQuestions(
  questions: Question[],
  count: number
): Question[] {
  const shuffled = [...questions].sort(() => Math.random() - 0.5);
  return shuffled.slice(0, count);
}

export function getTopicsBySubject(
  stream: string,
  subject: string,
  grade: number
): string[] {
  const questions = sampleQuestions.filter(
    (q) => q.stream === stream && q.subject === subject && q.grade === grade
  );
  const topics = [...new Set(questions.map((q) => q.topic))];
  return topics;
}
