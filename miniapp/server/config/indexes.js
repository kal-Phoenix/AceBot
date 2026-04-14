import logger from '../utils/logger.js';

/**
 * Create database indexes for optimal query performance
 */
export async function createIndexes(db) {
  try {
    logger.info('Creating database indexes...');

    // Students collection indexes
    await db.collection('students').createIndex(
      { telegram_id: 1 },
      { unique: true, sparse: true }
    );
    await db.collection('students').createIndex({ created_at: -1 });
    await db.collection('students').createIndex({ stream: 1 });

    // Exams collection indexes
    await db.collection('exams').createIndex(
      { exam_type: 1, subject: 1, stream: 1 }
    );
    await db.collection('exams').createIndex({ exam_type: 1 });
    await db.collection('exams').createIndex({ subject: 1 });
    await db.collection('exams').createIndex({ stream: 1 });
    await db.collection('exams').createIndex({ year: -1 });
    await db.collection('exams').createIndex({ created_at: -1 });

    // Questions collection indexes
    await db.collection('questions').createIndex({ exam_id: 1 });
    await db.collection('questions').createIndex(
      { exam_id: 1, question_number: 1 },
      { unique: true }
    );

    // Exam attempts collection indexes
    await db.collection('exam_attempts').createIndex({ user_id: 1 });
    await db.collection('exam_attempts').createIndex({ exam_id: 1 });
    await db.collection('exam_attempts').createIndex(
      { user_id: 1, exam_id: 1 }
    );
    await db.collection('exam_attempts').createIndex({ status: 1 });
    await db.collection('exam_attempts').createIndex({ started_at: -1 });
    await db.collection('exam_attempts').createIndex({ completed_at: -1 });
    await db.collection('exam_attempts').createIndex(
      { user_id: 1, subject: 1 }
    );

    // Exam answers collection indexes
    await db.collection('exam_answers').createIndex({ attempt_id: 1 });
    await db.collection('exam_answers').createIndex(
      { attempt_id: 1, question_id: 1 },
      { unique: true }
    );

    logger.info('✅ Database indexes created successfully');
  } catch (error) {
    logger.error('Failed to create indexes:', error);
    // Don't throw - indexes are optimization, not critical
  }
}
