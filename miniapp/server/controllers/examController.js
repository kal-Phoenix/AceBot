export class ExamController {
  constructor(examModel) {
    this.examModel = examModel;
  }

  async getAllExams(req, res) {
    try {
      const { exam_type, subject, stream } = req.query;
      
      const filters = {};
      if (exam_type) filters.exam_type = exam_type;
      if (subject) filters.subject = subject;
      if (stream) filters.stream = stream;

      const exams = await this.examModel.findAll(filters);
      res.json(exams);
    } catch (error) {
      console.error('Get exams error:', error);
      res.status(500).json({ error: 'Internal server error' });
    }
  }

  async getExamById(req, res) {
    try {
      const { id } = req.params;
      const exam = await this.examModel.findById(id);

      if (!exam) {
        return res.status(404).json({ error: 'Exam not found' });
      }

      res.json(exam);
    } catch (error) {
      console.error('Get exam error:', error);
      res.status(500).json({ error: 'Internal server error' });
    }
  }

  async getExamsByTypeAndSubject(req, res) {
    try {
      const { examType, subject } = req.params;
      const { stream } = req.query;

      if (!stream) {
        return res.status(400).json({ error: 'Stream is required' });
      }

      const exams = await this.examModel.findByTypeAndSubject(examType, subject, stream);
      res.json(exams);
    } catch (error) {
      console.error('Get exams by type and subject error:', error);
      res.status(500).json({ error: 'Internal server error' });
    }
  }

  async getQuestions(req, res) {
    try {
      const { id } = req.params;
      const questions = await this.examModel.getQuestions(id);

      if (!questions) {
        return res.status(404).json({ error: 'Exam not found' });
      }

      // Remove correct answers and explanations for exam mode
      // Frontend will handle this based on mode
      res.json(questions);
    } catch (error) {
      console.error('Get questions error:', error);
      res.status(500).json({ error: 'Internal server error' });
    }
  }

  async getSubjects(req, res) {
    try {
      const { stream } = req.query;

      if (!stream || !['natural', 'social'].includes(stream)) {
        return res.status(400).json({ error: 'Invalid stream' });
      }

      const subjects = await this.examModel.getSubjectsByStream(stream);
      res.json(subjects);
    } catch (error) {
      console.error('Get subjects error:', error);
      res.status(500).json({ error: 'Internal server error' });
    }
  }

  async createExam(req, res) {
    try {
      const examData = req.body;
      const exam = await this.examModel.create(examData);
      res.status(201).json(exam);
    } catch (error) {
      console.error('Create exam error:', error);
      res.status(500).json({ error: 'Internal server error' });
    }
  }
}
