/**
 * API Service for NEXIS Platform
 * Handles all backend communication
 */

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';

class APIError extends Error {
  constructor(message, status, data) {
    super(message);
    this.name = 'APIError';
    this.status = status;
    this.data = data;
  }
}

/**
 * Token management
 */
const TOKEN_KEY = 'nexis_auth_token';

export const tokenManager = {
  getToken: () => localStorage.getItem(TOKEN_KEY),
  setToken: (token) => localStorage.setItem(TOKEN_KEY, token),
  removeToken: () => localStorage.removeItem(TOKEN_KEY),
  hasToken: () => !!localStorage.getItem(TOKEN_KEY),
};

/**
 * Make API request with error handling
 */
async function apiRequest(endpoint, options = {}) {
  const url = `${API_BASE_URL}${endpoint}`;
  
  const headers = {
    'Content-Type': 'application/json',
    ...options.headers,
  };
  
  // Add auth token if available
  const token = tokenManager.getToken();
  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }
  
  const config = {
    headers,
    ...options,
  };

  try {
    const response = await fetch(url, config);
    const data = await response.json();

    if (!response.ok) {
      // Handle unauthorized
      if (response.status === 401) {
        tokenManager.removeToken();
        window.location.href = '/';
      }
      
      throw new APIError(
        data.detail || 'An error occurred',
        response.status,
        data
      );
    }

    return data;
  } catch (error) {
    if (error instanceof APIError) {
      throw error;
    }
    throw new APIError('Network error. Please check your connection.', 0, null);
  }
}

/**
 * API Methods
 */
export const api = {
  // ============= AUTHENTICATION =============
  
  /**
   * Register new user
   */
  register: async (userData) => {
    const response = await apiRequest('/auth/register', {
      method: 'POST',
      body: JSON.stringify(userData),
    });
    
    // Store token
    if (response.access_token) {
      tokenManager.setToken(response.access_token);
    }
    
    return response;
  },

  /**
   * Login user
   */
  login: async (credentials) => {
    const response = await apiRequest('/auth/login', {
      method: 'POST',
      body: JSON.stringify(credentials),
    });
    
    // Store token
    if (response.access_token) {
      tokenManager.setToken(response.access_token);
    }
    
    return response;
  },

  /**
   * Get current user profile
   */
  getCurrentUser: async () => {
    return apiRequest('/auth/me');
  },

  /**
   * Logout user
   */
  logout: async () => {
    try {
      await apiRequest('/auth/logout', { method: 'POST' });
    } finally {
      tokenManager.removeToken();
    }
  },

  // ============= CONSENT & SCORING =============
  
  /**
   * Submit user consent
   */
  submitConsent: async (consentData) => {
    return apiRequest('/consent', {
      method: 'POST',
      body: JSON.stringify(consentData),
    });
  },

  /**
   * Calculate credit trust score
   */
  calculateScore: async (userId, behavioralData) => {
    return apiRequest('/score', {
      method: 'POST',
      body: JSON.stringify({
        user_id: userId,
        behavioral_data: behavioralData,
      }),
    });
  },

  /**
   * Get score explainability
   */
  getExplainability: async (userId) => {
    return apiRequest(`/explainability/${userId}`);
  },

  /**
   * Get improvement plan
   */
  getImprovementPlan: async (userId) => {
    return apiRequest(`/improvement/${userId}`);
  },

  /**
   * Get roadmap
   */
  getRoadmap: async (userId) => {
    return apiRequest(`/roadmap/${userId}`);
  },

  /**
   * Get lender view
   */
  getLenderView: async (userId) => {
    return apiRequest(`/lender-view/${userId}`);
  },

  /**
   * Submit lender decision
   */
  submitLenderDecision: async (decisionData) => {
    return apiRequest('/lender-decision', {
      method: 'POST',
      body: JSON.stringify(decisionData),
    });
  },

  /**
   * Health check
   */
  healthCheck: async () => {
    const url = API_BASE_URL.replace('/api/v1', '/health');
    const response = await fetch(url);
    return response.json();
  },
};

/**
 * Generate random sample behavioral data for demo (India context)
 * Creates realistic variations to demonstrate different user profiles
 */
export const generateSampleBehavioralData = () => {
  // Generate random values within realistic ranges
  const profiles = [
    // Excellent profile
    {
      utility_payment_months: Math.floor(Math.random() * 6) + 18,  // 18-24 months
      utility_payment_consistency: 0.92 + Math.random() * 0.08,    // 92-100%
      monthly_transaction_count: Math.floor(Math.random() * 20) + 50,  // 50-70 transactions
      transaction_regularity_score: 0.85 + Math.random() * 0.15,   // 85-100%
      spending_volatility: Math.random() * 0.15,                   // 0-15%
      avg_month_end_balance: 20000 + Math.random() * 30000,        // ₹20K-50K
      savings_growth_rate: 0.12 + Math.random() * 0.18,            // 12-30%
      withdrawal_discipline_score: 0.80 + Math.random() * 0.20,    // 80-100%
      income_regularity_score: 0.85 + Math.random() * 0.15,        // 85-100%
      income_stability_months: Math.floor(Math.random() * 7) + 18, // 18-24 months
      account_tenure_months: Math.floor(Math.random() * 24) + 36,  // 36-60 months
      address_stability_years: 2.5 + Math.random() * 3.5,          // 2.5-6 years
      discretionary_income_ratio: 0.18 + Math.random() * 0.12,     // 18-30%
    },
    // Good profile
    {
      utility_payment_months: Math.floor(Math.random() * 6) + 12,  // 12-18 months
      utility_payment_consistency: 0.80 + Math.random() * 0.12,    // 80-92%
      monthly_transaction_count: Math.floor(Math.random() * 15) + 35,  // 35-50 transactions
      transaction_regularity_score: 0.70 + Math.random() * 0.15,   // 70-85%
      spending_volatility: 0.15 + Math.random() * 0.15,            // 15-30%
      avg_month_end_balance: 10000 + Math.random() * 15000,        // ₹10K-25K
      savings_growth_rate: 0.05 + Math.random() * 0.12,            // 5-17%
      withdrawal_discipline_score: 0.65 + Math.random() * 0.20,    // 65-85%
      income_regularity_score: 0.70 + Math.random() * 0.15,        // 70-85%
      income_stability_months: Math.floor(Math.random() * 7) + 12, // 12-18 months
      account_tenure_months: Math.floor(Math.random() * 18) + 24,  // 24-42 months
      address_stability_years: 1.5 + Math.random() * 2.5,          // 1.5-4 years
      discretionary_income_ratio: 0.12 + Math.random() * 0.10,     // 12-22%
    },
    // Average profile
    {
      utility_payment_months: Math.floor(Math.random() * 6) + 8,   // 8-14 months
      utility_payment_consistency: 0.65 + Math.random() * 0.15,    // 65-80%
      monthly_transaction_count: Math.floor(Math.random() * 15) + 25,  // 25-40 transactions
      transaction_regularity_score: 0.55 + Math.random() * 0.15,   // 55-70%
      spending_volatility: 0.25 + Math.random() * 0.20,            // 25-45%
      avg_month_end_balance: 5000 + Math.random() * 10000,         // ₹5K-15K
      savings_growth_rate: 0.00 + Math.random() * 0.08,            // 0-8%
      withdrawal_discipline_score: 0.50 + Math.random() * 0.20,    // 50-70%
      income_regularity_score: 0.55 + Math.random() * 0.15,        // 55-70%
      income_stability_months: Math.floor(Math.random() * 7) + 6,  // 6-12 months
      account_tenure_months: Math.floor(Math.random() * 18) + 12,  // 12-30 months
      address_stability_years: 0.8 + Math.random() * 2.0,          // 0.8-2.8 years
      discretionary_income_ratio: 0.08 + Math.random() * 0.08,     // 8-16%
    },
    // Developing profile
    {
      utility_payment_months: Math.floor(Math.random() * 4) + 4,   // 4-8 months
      utility_payment_consistency: 0.50 + Math.random() * 0.15,    // 50-65%
      monthly_transaction_count: Math.floor(Math.random() * 15) + 15,  // 15-30 transactions
      transaction_regularity_score: 0.40 + Math.random() * 0.15,   // 40-55%
      spending_volatility: 0.40 + Math.random() * 0.25,            // 40-65%
      avg_month_end_balance: 2000 + Math.random() * 5000,          // ₹2K-7K
      savings_growth_rate: -0.05 + Math.random() * 0.08,           // -5% to 3%
      withdrawal_discipline_score: 0.35 + Math.random() * 0.20,    // 35-55%
      income_regularity_score: 0.40 + Math.random() * 0.15,        // 40-55%
      income_stability_months: Math.floor(Math.random() * 4) + 3,  // 3-6 months
      account_tenure_months: Math.floor(Math.random() * 12) + 6,   // 6-18 months
      address_stability_years: 0.3 + Math.random() * 1.2,          // 0.3-1.5 years
      discretionary_income_ratio: 0.03 + Math.random() * 0.07,     // 3-10%
    }
  ];

  // Randomly select a profile (weighted towards good/average profiles)
  const rand = Math.random();
  let selectedProfile;
  if (rand < 0.25) {
    selectedProfile = profiles[0]; // 25% excellent
  } else if (rand < 0.60) {
    selectedProfile = profiles[1]; // 35% good
  } else if (rand < 0.90) {
    selectedProfile = profiles[2]; // 30% average
  } else {
    selectedProfile = profiles[3]; // 10% developing
  }

  return selectedProfile;
};

/**
 * Default sample behavioral data for demo (India context)
 * This is a good profile example
 */
export const SAMPLE_BEHAVIORAL_DATA = {
  utility_payment_months: 18,  // Electricity, water bills
  utility_payment_consistency: 0.95,
  monthly_transaction_count: 52,  // UPI, digital payments
  transaction_regularity_score: 0.88,
  spending_volatility: 0.12,
  avg_month_end_balance: 25000.0,  // ₹25,000
  savings_growth_rate: 0.15,
  withdrawal_discipline_score: 0.82,
  income_regularity_score: 0.90,
  income_stability_months: 18,
  account_tenure_months: 42,  // Bank account age
  address_stability_years: 3.5,
  discretionary_income_ratio: 0.22,
};

export default api;
