export class AttemptController {
  constructor(attemptModel, userModel) {
    this.attemptModel = attemptModel;
    this.userModel = userModel;
  }

  async getAllAttempts(req, res) {
    try {
      const telegramId = req.user.telegram_id;
      const attempts = await this.attemptModel.findAll(telegramId);
      res.json(attempts);
    } catch (error) {
      console.error('Get attempts error:', error);
      res.status(500).json({ error: 'Internal server error' });
    }
  }

  async getAttemptById(req, res) {
    try {
      const { id } = req.params;
      const attempt = await this.attemptModel.findById(id);

      if (!attempt) {
        return res.status(404).json({ error: 'Attempt not found' });
      }

      // Verify the attempt belongs to the user
      if (attempt.telegram_id !== req.user.telegram_id) {
        return res.status(403).json({ error: 'Unauthorized' });
      }

      res.json(attempt);
    } catch (error) {
      console.error('Get attempt error:', error);
      res.status(500).json({ error: 'Internal server error' });
    }
  }

  async createAttempt(req, res) {
    try {
      const telegramId = req.user.telegram_id;
      const attemptData = {
        ...req.body,
        telegram_id: telegramId,
      };

      const attempt = await this.attemptModel.create(attemptData);
      res.status(201).json(attempt);
    } catch (error) {
      console.error('Create attempt error:', error);
      res.status(500).json({ error: 'Internal server error' });
    }
  }

  async submitAnswer(req, res) {
    try {
      const { id } = req.params;
      const answerData = req.body;

      const attempt = await this.attemptModel.findById(id);

      if (!attempt) {
        return res.status(404).json({ error: 'Attempt not found' });
      }

      if (attempt.telegram_id !== req.user.telegram_id) {
        return res.status(403).json({ error: 'Unauthorized' });
      }

      const result = await this.attemptModel.submitAnswer(id, answerData);
      res.json(result.value);
    } catch (error) {
      console.error('Submit answer error:', error);
      res.status(500).json({ error: 'Internal server error' });
    }
  }

  async completeAttempt(req, res) {
    try {
      const { id } = req.params;
      const completionData = req.body;

      const attempt = await this.attemptModel.findById(id);

      if (!attempt) {
        return res.status(404).json({ error: 'Attempt not found' });
      }

      if (attempt.telegram_id !== req.user.telegram_id) {
        return res.status(403).json({ error: 'Unauthorized' });
      }

      const result = await this.attemptModel.complete(id, completionData);

      // Update user stats
      await this.updateUserStats(req.user.telegram_id);

      res.json(result.value);
    } catch (error) {
      console.error('Complete attempt error:', error);
      res.status(500).json({ error: 'Internal server error' });
    }
  }

  async getStats(req, res) {
    try {
      const telegramId = req.user.telegram_id;
      const stats = await this.attemptModel.getStatsBySubject(telegramId);
      res.json(stats);
    } catch (error) {
      console.error('Get stats error:', error);
      res.status(500).json({ error: 'Internal server error' });
    }
  }

  async updateUserStats(telegramId) {
    try {
      const attempts = await this.attemptModel.findAll(telegramId);
      const completedAttempts = attempts.filter(a => a.status === 'completed');

      if (completedAttempts.length === 0) return;

      const examAttempts = completedAttempts.filter(a => a.mode === 'exam');
      const practiceAttempts = completedAttempts.filter(a => a.mode === 'practice');

      const averageScore = completedAttempts.reduce((sum, a) => sum + a.percentage, 0) / completedAttempts.length;
      const totalTimeSpent = completedAttempts.reduce((sum, a) => sum + (a.time_spent_seconds || 0), 0);

      const subjectStats = await this.attemptModel.getStatsBySubject(telegramId);
      const bestSubject = subjectStats.reduce((best, curr) => 
        (!best || curr.average_score > best.average_score) ? curr : best, null);
      const weakestSubject = subjectStats.reduce((worst, curr) => 
        (!worst || curr.average_score < worst.average_score) ? curr : worst, null);

      const stats = {
        total_exams_taken: examAttempts.length,
        total_practice_sessions: practiceAttempts.length,
        average_score: Math.round(averageScore * 10) / 10,
        best_subject: bestSubject ? bestSubject._id : null,
        weakest_subject: weakestSubject ? weakestSubject._id : null,
        total_time_spent: totalTimeSpent,
      };

      await this.userModel.updateStats(telegramId, stats);
    } catch (error) {
      console.error('Update user stats error:', error);
    }
  }
}
