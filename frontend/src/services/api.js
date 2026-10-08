import axios from 'axios';

const API_BASE = '/api';

export const analyzeGarment = async (file, garmentType = 'blouse') => {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('garment_type', garmentType);

  const response = await axios.post(`${API_BASE}/analyze-garment`, formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
  return response.data;
};

export const fetchDesigns = async (category = 'all', placement = 'all') => {
  const params = {};
  if (category && category !== 'all') params.category = category;
  if (placement && placement !== 'all') params.placement = placement;

  const response = await axios.get(`${API_BASE}/designs`, { params });
  return response.data;
};

export const uploadDesign = async (formData) => {
  const response = await axios.post(`${API_BASE}/designs/upload`, formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
  return response.data;
};

export const deleteDesign = async (designId) => {
  const response = await axios.delete(`${API_BASE}/designs/${designId}`);
  return response.data;
};

export const deleteAllDesigns = async () => {
  const response = await axios.delete(`${API_BASE}/designs/all`);
  return response.data;
};

export const fetchRecommendations = async (uploadId, designIds = null, customerRequirements = null) => {
  const payload = {
    upload_id: uploadId,
    customer_requirements: customerRequirements,
    design_ids: designIds,
    top_k: 4
  };
  const response = await axios.post(`${API_BASE}/recommend`, payload);
  return response.data;
};

export const submitFeedback = async (payload) => {
  const response = await axios.post(`${API_BASE}/feedback`, payload);
  return response.data;
};

export const fetchFeedbackStats = async () => {
  const response = await axios.get(`${API_BASE}/feedback`);
  return response.data;
};
