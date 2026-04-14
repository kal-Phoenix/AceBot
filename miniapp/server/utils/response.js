/**
 * Standardized API response utilities
 */

export const success = (res, data, message = 'Success', statusCode = 200) => {
  return res.status(statusCode).json({
    success: true,
    message,
    data,
  });
};

export const error = (res, message, statusCode = 500, errors = null) => {
  const response = {
    success: false,
    error: message,
  };

  if (errors) {
    response.errors = errors;
  }

  return res.status(statusCode).json(response);
};

export const validationError = (res, errors) => {
  return res.status(400).json({
    success: false,
    error: 'Validation failed',
    errors: errors.array(),
  });
};

export const notFound = (res, resource = 'Resource') => {
  return res.status(404).json({
    success: false,
    error: `${resource} not found`,
  });
};

export const unauthorized = (res, message = 'Unauthorized access') => {
  return res.status(401).json({
    success: false,
    error: message,
  });
};

export const forbidden = (res, message = 'Access forbidden') => {
  return res.status(403).json({
    success: false,
    error: message,
  });
};
