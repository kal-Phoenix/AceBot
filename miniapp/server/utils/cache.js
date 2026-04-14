import NodeCache from 'node-cache';
import logger from './logger.js';

// Create cache instance with 10 minute default TTL
const cache = new NodeCache({
  stdTTL: 600, // 10 minutes
  checkperiod: 120, // Check for expired keys every 2 minutes
  useClones: false, // Don't clone objects (better performance)
});

// Cache events
cache.on('set', (key, value) => {
  logger.debug(`Cache SET: ${key}`);
});

cache.on('del', (key, value) => {
  logger.debug(`Cache DEL: ${key}`);
});

cache.on('expired', (key, value) => {
  logger.debug(`Cache EXPIRED: ${key}`);
});

/**
 * Get value from cache
 */
export const get = (key) => {
  try {
    const value = cache.get(key);
    if (value !== undefined) {
      logger.debug(`Cache HIT: ${key}`);
      return value;
    }
    logger.debug(`Cache MISS: ${key}`);
    return null;
  } catch (error) {
    logger.error('Cache get error:', error);
    return null;
  }
};

/**
 * Set value in cache
 */
export const set = (key, value, ttl = 600) => {
  try {
    cache.set(key, value, ttl);
    return true;
  } catch (error) {
    logger.error('Cache set error:', error);
    return false;
  }
};

/**
 * Delete value from cache
 */
export const del = (key) => {
  try {
    cache.del(key);
    return true;
  } catch (error) {
    logger.error('Cache del error:', error);
    return false;
  }
};

/**
 * Clear all cache
 */
export const flush = () => {
  try {
    cache.flushAll();
    logger.info('Cache flushed');
    return true;
  } catch (error) {
    logger.error('Cache flush error:', error);
    return false;
  }
};

/**
 * Get cache statistics
 */
export const getStats = () => {
  return cache.getStats();
};

/**
 * Middleware to cache GET requests
 */
export const cacheMiddleware = (duration = 600) => {
  return (req, res, next) => {
    // Only cache GET requests
    if (req.method !== 'GET') {
      return next();
    }

    const key = `cache:${req.originalUrl || req.url}`;
    const cachedResponse = get(key);

    if (cachedResponse) {
      return res.json(cachedResponse);
    }

    // Store original json function
    const originalJson = res.json.bind(res);

    // Override json function to cache response
    res.json = (body) => {
      set(key, body, duration);
      return originalJson(body);
    };

    next();
  };
};

export default {
  get,
  set,
  del,
  flush,
  getStats,
  cacheMiddleware,
};
