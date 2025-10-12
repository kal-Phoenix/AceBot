import { ObjectId } from 'mongodb';

export class ExamModel {
  constructor(db) {
    this.collection = db.collection('exams');
  }

  async findAll(filters = {}) {
    return await this.collection.find(filters).toArray();
  }

  async findById(examId) {
    return await this.collection.findOne({ _id: new ObjectId(examId) });
  }

  async findByTypeAndSubject(examType, subject, stream) {
    return await this.collection.find({
      exam_type: examType,
      subject: subject,
      stream: stream,
    }).toArray();
  }

  async getQuestions(examId) {
    const exam = await this.findById(examId);
    return exam ? exam.questions : [];
  }

  async create(examData) {
    const exam = {
      title: examData.title,
      description: examData.description,
      exam_type: examData.exam_type, // 'past', 'mock', 'model'
      subject: examData.subject,
      stream: examData.stream, // 'natural' or 'social'
      duration_minutes: examData.duration_minutes,
      passing_score: examData.passing_score,
      total_questions: examData.questions.length,
      questions: examData.questions.map((q, index) => ({
        question_id: new ObjectId().toString(),
        question_number: index + 1,
        question_text: q.question_text,
        options: {
          a: q.option_a,
          b: q.option_b,
          c: q.option_c,
          d: q.option_d,
        },
        correct_answer: q.correct_answer,
        explanation: q.explanation,
        points: q.points || 1,
        has_image: q.has_image || false,
        image_url: q.image_url || null,
      })),
      created_at: new Date(),
      updated_at: new Date(),
    };

    const result = await this.collection.insertOne(exam);
    return { ...exam, _id: result.insertedId };
  }

  async getSubjectsByStream(stream) {
    const subjects = stream === 'natural'
      ? ['English', 'Maths', 'SAT', 'Chemistry', 'Biology', 'Physics']
      : ['English', 'Maths', 'SAT', 'History', 'Geography', 'Economics'];
    
    return subjects;
  }
}
