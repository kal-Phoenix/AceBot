import { ObjectId } from 'mongodb';

export class AttemptModel {
  constructor(db) {
    this.collection = db.collection('attempts');
  }

  async findAll(telegramId) {
    return await this.collection.find({ telegram_id: telegramId }).sort({ started_at: -1 }).toArray();
  }

  async findById(attemptId) {
    return await this.collection.findOne({ _id: new ObjectId(attemptId) });
  }

  async create(attemptData) {
    const attempt = {
      telegram_id: attemptData.telegram_id,
      exam_id: attemptData.exam_id,
      exam_title: attemptData.exam_title,
      exam_type: attemptData.exam_type,
      subject: attemptData.subject,
      mode: attemptData.mode, // 'practice' or 'exam'
      started_at: new Date(),
      completed_at: null,
      score: null,
      total_points: null,
      max_points: attemptData.max_points,
      percentage: null,
      status: 'in_progress', // 'in_progress', 'completed', 'abandoned'
      time_spent_seconds: null,
      answers: [],
    };

    const result = await this.collection.insertOne(attempt);
    return { ...attempt, _id: result.insertedId };
  }

  async submitAnswer(attemptId, answerData) {
    const answer = {
      question_id: answerData.question_id,
      question_number: answerData.question_number,
      selected_answer: answerData.selected_answer,
      correct_answer: answerData.correct_answer,
      is_correct: answerData.selected_answer === answerData.correct_answer,
      points_earned: answerData.selected_answer === answerData.correct_answer ? answerData.points : 0,
      answered_at: new Date(),
    };

    return await this.collection.findOneAndUpdate(
      { _id: new ObjectId(attemptId) },
      { $push: { answers: answer } },
      { returnDocument: 'after' }
    );
  }

  async complete(attemptId, completionData) {
    const totalPoints = completionData.answers.reduce((sum, ans) => sum + ans.points_earned, 0);
    const percentage = (totalPoints / completionData.max_points) * 100;

    return await this.collection.findOneAndUpdate(
      { _id: new ObjectId(attemptId) },
      { 
        $set: {
          completed_at: new Date(),
          score: totalPoints,
          total_points: totalPoints,
          percentage: Math.round(percentage * 10) / 10,
          status: 'completed',
          time_spent_seconds: completionData.time_spent_seconds,
          answers: completionData.answers,
        }
      },
      { returnDocument: 'after' }
    );
  }

  async getStatsBySubject(telegramId) {
    return await this.collection.aggregate([
      { $match: { telegram_id: telegramId, status: 'completed' } },
      {
        $group: {
          _id: '$subject',
          total_attempts: { $sum: 1 },
          average_score: { $avg: '$percentage' },
          best_score: { $max: '$percentage' },
        }
      }
    ]).toArray();
  }
}
