export class UserController {
  constructor(userModel) {
    this.userModel = userModel;
  }

  async getUser(req, res) {
    try {
      const telegramId = req.user.telegram_id;
      const user = await this.userModel.findByTelegramId(telegramId);

      if (!user) {
        return res.status(404).json({ error: 'User not found' });
      }

      res.json(user);
    } catch (error) {
      console.error('Get user error:', error);
      res.status(500).json({ error: 'Internal server error' });
    }
  }

  async selectStream(req, res) {
    try {
      const telegramId = req.user.telegram_id;
      const { stream } = req.body;

      if (!stream || !['natural', 'social'].includes(stream)) {
        return res.status(400).json({ error: 'Invalid stream. Must be "natural" or "social"' });
      }

      const result = await this.userModel.updateStream(telegramId, stream);

      if (!result.value) {
        return res.status(404).json({ error: 'User not found' });
      }

      res.json({ 
        message: 'Stream selected successfully. This selection is permanent.',
        user: result.value,
        permanent: true
      });
    } catch (error) {
      console.error('Select stream error:', error);
      
      if (error.message.includes('already been selected')) {
        return res.status(400).json({ 
          error: error.message,
          code: 'STREAM_ALREADY_SELECTED'
        });
      }
      
      res.status(500).json({ error: 'Internal server error' });
    }
  }

  async getStreamStatus(req, res) {
    try {
      const telegramId = req.user.telegram_id;
      const status = await this.userModel.getStreamSelectionStatus(telegramId);
      res.json(status);
    } catch (error) {
      console.error('Get stream status error:', error);
      res.status(500).json({ error: 'Internal server error' });
    }
  }

  // Admin only endpoint for forcing stream changes
  async forceUpdateStream(req, res) {
    try {
      const { telegramId, stream } = req.body;

      if (!telegramId || !stream || !['natural', 'social'].includes(stream)) {
        return res.status(400).json({ error: 'Invalid parameters' });
      }

      // In a real app, you'd check for admin permissions here
      const result = await this.userModel.updateStream(telegramId, stream, true);

      if (!result.value) {
        return res.status(404).json({ error: 'User not found' });
      }

      res.json({ 
        message: 'Stream forcefully updated by admin',
        user: result.value 
      });
    } catch (error) {
      console.error('Force update stream error:', error);
      res.status(500).json({ error: 'Internal server error' });
    }
  }

  async updateStats(req, res) {
    try {
      const telegramId = req.user.telegram_id;
      const { stats } = req.body;

      const result = await this.userModel.updateStats(telegramId, stats);

      if (!result.value) {
        return res.status(404).json({ error: 'User not found' });
      }

      res.json({ 
        message: 'Stats updated successfully',
        user: result.value 
      });
    } catch (error) {
      console.error('Update stats error:', error);
      res.status(500).json({ error: 'Internal server error' });
    }
  }

  async resetData(req, res) {
    try {
      const telegramId = req.user.telegram_id;

      const result = await this.userModel.resetUserData(telegramId);

      if (!result.value) {
        return res.status(404).json({ error: 'User not found' });
      }

      res.json({ 
        message: 'User data reset successfully',
        user: result.value 
      });
    } catch (error) {
      console.error('Reset data error:', error);
      res.status(500).json({ error: 'Internal server error' });
    }
  }

  async getLeaderboard(req, res) {
    try {
      const { stream, limit = 50 } = req.query;
      
      const leaderboard = await this.userModel.getLeaderboard(
        parseInt(limit), 
        stream || null
      );

      // Add rank to each user
      const leaderboardWithRank = leaderboard.map((user, index) => ({
        ...user,
        rank: index + 1
      }));

      res.json(leaderboardWithRank);
    } catch (error) {
      console.error('Get leaderboard error:', error);
      res.status(500).json({ error: 'Internal server error' });
    }
  }

  async getUserRank(req, res) {
    try {
      const telegramId = req.user.telegram_id;
      
      const rankData = await this.userModel.getUserRank(telegramId);
      
      if (!rankData) {
        return res.json({ 
          message: 'User has not taken any exams yet',
          rank: null,
          total_users: 0,
          score: 0
        });
      }

      res.json(rankData);
    } catch (error) {
      console.error('Get user rank error:', error);
      res.status(500).json({ error: 'Internal server error' });
    }
  }
}
