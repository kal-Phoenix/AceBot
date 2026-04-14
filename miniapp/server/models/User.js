import { ObjectId } from 'mongodb';

export class UserModel {
  constructor(db) {
    this.collection = db.collection('users');
  }

  async findByTelegramId(telegramId) {
    return await this.collection.findOne({ telegram_id: telegramId });
  }

  async create(userData) {
    const user = {
      telegram_id: userData.telegram_id,
      username: userData.username || null,
      first_name: userData.first_name,
      last_name: userData.last_name || null,
      full_name: userData.full_name,
      profile_picture: userData.profile_picture || null,
      stream: null, // 'natural' or 'social'
      stats: {
        total_exams_taken: 0,
        total_practice_sessions: 0,
        average_score: 0,
        best_subject: null,
        weakest_subject: null,
        total_time_spent: 0,
      },
      created_at: new Date(),
      updated_at: new Date(),
    };

    const result = await this.collection.insertOne(user);
    return { ...user, _id: result.insertedId };
  }

  async updateStream(telegramId, stream, force = false) {
    const user = await this.findByTelegramId(telegramId);
    
    // Prevent stream change if user already has a stream (unless forced by admin)
    if (user && user.stream && !force) {
      throw new Error('Stream has already been selected and cannot be changed. Contact admin if needed.');
    }

    // Validate stream value
    if (!stream || !['natural', 'social'].includes(stream)) {
      throw new Error('Invalid stream. Must be "natural" or "social".');
    }

    return await this.collection.findOneAndUpdate(
      { telegram_id: telegramId },
      { 
        $set: { 
          stream: stream,
          stream_selected_at: new Date(),
          updated_at: new Date()
        } 
      },
      { returnDocument: 'after' }
    );
  }

  async getStreamSelectionStatus(telegramId) {
    const user = await this.findByTelegramId(telegramId);
    return {
      hasStream: !!user?.stream,
      stream: user?.stream || null,
      streamSelectedAt: user?.stream_selected_at || null,
      canChange: false // Always false for regular users
    };
  }

  async updateStats(telegramId, stats) {
    return await this.collection.findOneAndUpdate(
      { telegram_id: telegramId },
      { 
        $set: { 
          stats: stats,
          updated_at: new Date()
        } 
      },
      { returnDocument: 'after' }
    );
  }

  async resetUserData(telegramId) {
    return await this.collection.findOneAndUpdate(
      { telegram_id: telegramId },
      { 
        $set: { 
          stream: null,
          stats: {
            total_exams_taken: 0,
            total_practice_sessions: 0,
            average_score: 0,
            best_subject: null,
            weakest_subject: null,
            total_time_spent: 0,
          },
          updated_at: new Date()
        } 
      },
      { returnDocument: 'after' }
    );
  }

  async getLeaderboard(limit = 50, stream = null) {
    const filter = stream ? { stream: stream } : {};
    
    const pipeline = [
      { $match: filter },
      { $match: { 'stats.total_exams_taken': { $gt: 0 } } }, // Only users who have taken exams
      {
        $addFields: {
          leaderboard_score: {
            $add: [
              { $multiply: ['$stats.average_score', 0.7] }, // 70% weight on average score
              { $multiply: ['$stats.total_exams_taken', 2] }, // 20% weight on total exams (scaled)
              { $multiply: [{ $divide: ['$stats.total_practice_sessions', 10] }, 1] } // 10% weight on practice sessions
            ]
          }
        }
      },
      { $sort: { leaderboard_score: -1 } },
      { $limit: limit },
      {
        $project: {
          _id: 1,
          telegram_id: 1,
          username: 1,
          first_name: 1,
          last_name: 1,
          full_name: 1,
          profile_picture: 1,
          stream: 1,
          stats: 1,
          leaderboard_score: 1,
          rank: { $add: [{ $indexOfArray: ['$__results', '$_id'] }, 1] }
        }
      }
    ];

    return await this.collection.aggregate(pipeline).toArray();
  }

  async getUserRank(telegramId) {
    const user = await this.findByTelegramId(telegramId);
    if (!user || user.stats.total_exams_taken === 0) {
      return null;
    }

    const userScore = (user.stats.average_score * 0.7) + (user.stats.total_exams_taken * 2) + (user.stats.total_practice_sessions / 10);
    
    const usersAhead = await this.collection.countDocuments({
      stream: user.stream,
      'stats.total_exams_taken': { $gt: 0 },
      $expr: {
        $gt: [
          { $add: [
            { $multiply: ['$stats.average_score', 0.7] },
            { $multiply: ['$stats.total_exams_taken', 2] },
            { $multiply: [{ $divide: ['$stats.total_practice_sessions', 10] }, 1] }
          ]},
          userScore
        ]
      }
    });

    return {
      rank: usersAhead + 1,
      total_users: await this.collection.countDocuments({
        stream: user.stream,
        'stats.total_exams_taken': { $gt: 0 }
      }),
      score: userScore
    };
  }
}
