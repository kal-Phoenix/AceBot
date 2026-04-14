import axios from 'axios';
import axiosRetry from 'axios-retry';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:3001/api';

console.log('API URL configured as:', API_URL);

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000, // 30 second timeout
});

// Configure retry logic
axiosRetry(api, {
  retries: 3, // Retry failed requests up to 3 times
  retryDelay: axiosRetry.exponentialDelay, // Exponential backoff
  retryCondition: (error) => {
    // Retry on network errors or 5xx server errors
    return axiosRetry.isNetworkOrIdempotentRequestError(error) ||
           (error.response?.status ? error.response.status >= 500 : false);
  },
  onRetry: (retryCount, error, requestConfig) => {
    console.log(`Retrying request (${retryCount}/3):`, requestConfig.url);
  },
});

// Add token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('auth_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
    console.log('Adding auth token to request:', config.url);
  } else {
    console.log('No auth token found for request:', config.url);
  }
  return config;
});

// Handle token expiration and errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    // Handle authentication errors
    if (error.response?.status === 401 || error.response?.status === 403) {
      localStorage.removeItem('auth_token');
      localStorage.removeItem('user');
      window.location.href = '/';
    }
    
    // Log errors in development
    if (import.meta.env.DEV) {
      console.error('API Error:', {
        url: error.config?.url,
        method: error.config?.method,
        status: error.response?.status,
        message: error.response?.data?.error || error.message,
      });
    }
    
    return Promise.reject(error);
  }
);

export default api;

// Types
export type Student = {
  id: string;
  email: string;
  full_name: string;
  profile_picture?: string | null;
  created_at: string;
};

export type Exam = {
  id: string;
  title: string;
  description: string;
  duration_minutes: number;
  passing_score: number;
  total_questions: number;
  difficulty: string;
  category: string;
  created_at: string;
};

export type Question = {
  id: string;
  exam_id: string;
  question_text: string;
  option_a: string;
  option_b: string;
  option_c: string;
  option_d: string;
  correct_answer: string;
  points: number;
  question_order: number;
  has_image?: boolean;
  image_url?: string | null;
};

export type ExamAttempt = {
  id: string;
  student_id: string;
  exam_id: string;
  started_at: string;
  completed_at: string | null;
  score: number | null;
  total_points: number | null;
  max_points: number | null;
  status: 'in_progress' | 'completed' | 'abandoned';
  time_spent_seconds: number | null;
};

export type ExamAnswer = {
  id: string;
  attempt_id: string;
  question_id: string;
  selected_answer: string;
  is_correct: boolean;
  points_earned: number;
  answered_at: string;
};

// Auth API
export const authAPI = {
  telegramAuth: async (initData: string, user: any) => {
    const response = await api.post('/auth/telegram-auth', { initData, user });
    return response.data;
  },
  getMe: async () => {
    const response = await api.get('/auth/me');
    return response.data;
  },
  signOut: async () => {
    const response = await api.post('/auth/signout');
    return response.data;
  },
};

// User API
export const userAPI = {
  selectStream: async (stream: 'natural' | 'social') => {
    console.log('userAPI.selectStream called with:', stream);
    console.log('API base URL:', api.defaults.baseURL);
    
    try {
      const response = await api.post('/users/stream', { stream });
      console.log('Stream selection response:', response.data);
      return response.data;
    } catch (error) {
      console.error('Stream selection API error:', error);
      console.error('Error config:', error.config);
      throw error;
    }
  },
  getStreamStatus: async () => {
    const response = await api.get('/users/stream/status');
    return response.data;
  },
  forceUpdateStream: async (telegramId: string, stream: 'natural' | 'social') => {
    const response = await api.post('/users/stream/force', { telegramId, stream });
    return response.data;
  },
  updateStats: async (stats: any) => {
    const response = await api.patch('/users/stats', { stats });
    return response.data;
  },
  resetData: async () => {
    const response = await api.post('/users/reset');
    return response.data;
  },
  getLeaderboard: async (stream?: string, limit?: number) => {
    const params = new URLSearchParams();
    if (stream) params.append('stream', stream);
    if (limit) params.append('limit', limit.toString());
    
    const response = await api.get(`/users/leaderboard?${params.toString()}`);
    return response.data;
  },
  getUserRank: async () => {
    const response = await api.get('/users/rank');
    return response.data;
  },
};

// Exams API
export const examsAPI = {
  getAll: async (): Promise<Exam[]> => {
    const response = await api.get('/exams');
    return response.data;
  },
  getById: async (id: string): Promise<Exam> => {
    const response = await api.get(`/exams/${id}`);
    return response.data;
  },
  getByTypeAndSubject: async (examType: string, subject: string, stream: string) => {
    const response = await api.get(`/exams/type/${examType}/subject/${subject}?stream=${stream}`);
    return response.data;
  },
  getQuestions: async (examId: string): Promise<Question[]> => {
    const response = await api.get(`/exams/${examId}/questions`);
    return response.data;
  },
  getSubjects: async (stream: string): Promise<string[]> => {
    const response = await api.get(`/exams/subjects?stream=${stream}`);
    return response.data;
  },
};

// Attempts API
export const attemptsAPI = {
  getAll: async (): Promise<ExamAttempt[]> => {
    const response = await api.get('/attempts');
    return response.data;
  },
  getById: async (id: string): Promise<ExamAttempt> => {
    const response = await api.get(`/attempts/${id}`);
    return response.data;
  },
  create: async (data: any): Promise<any> => {
    const response = await api.post('/attempts', data);
    return response.data;
  },
  submitAnswer: async (attemptId: string, answerData: any) => {
    const response = await api.post(`/attempts/${attemptId}/answer`, answerData);
    return response.data;
  },
  complete: async (attemptId: string, completionData: any) => {
    const response = await api.post(`/attempts/${attemptId}/complete`, completionData);
    return response.data;
  },
  getStats: async () => {
    const response = await api.get('/attempts/stats');
    return response.data;
  },
};

// Questions API
export const questionsAPI = {
  getBatch: async (ids: string[]): Promise<Question[]> => {
    const response = await api.post('/questions/batch', { ids });
    return response.data;
  },
};
