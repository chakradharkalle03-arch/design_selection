import React, { useState } from 'react';
import ImageUploader from '../components/ImageUploader';
import GarmentAnalysisCard from '../components/GarmentAnalysisCard';
import RecommendationCard from '../components/RecommendationCard';
import LoadingAI from '../components/LoadingAI';
import { analyzeGarment, fetchRecommendations } from '../services/api';
import { Sparkles, Trophy } from 'lucide-react';

export default function CustomerMatch() {
  const [garment, setGarment] = useState(null);
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleUploadAndAnalyze = async (file, garmentType) => {
    setLoading(true);
    setError(null);

    try {
      // Step 1: Upload & analyze garment
      const garmentData = await analyzeGarment(file, garmentType);
      setGarment(garmentData);

      // Step 2: Fetch Top 4 Recommendations
      const recData = await fetchRecommendations(garmentData.upload_id);
      setRecommendations(recData.top_recommendations || []);
    } catch (err) {
      console.error('Matching failed:', err);
      setError(err.response?.data?.detail || 'Failed to analyze garment. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setGarment(null);
    setRecommendations([]);
    setError(null);
  };

  return (
    <div style={{ maxWidth: '1280px', margin: '0 auto', padding: '32px 24px' }}>
      {/* Hero Header */}
      {!garment && !loading && (
        <div style={{ textAlign: 'center', margin: '20px 0 40px 0' }}>
          <div style={{ display: 'inline-flex', alignItems: 'center', gap: '8px', marginBottom: '16px' }} className="badge-gold">
            <Sparkles size={14} /> AI-POWERED EMBROIDERY FINDER
          </div>
          <h1 style={{ fontSize: '2.5rem', fontWeight: 800, color: '#FFF', letterSpacing: '-0.5px', marginBottom: '12px' }}>
            Find the Best Embroidery for Your <span style={{ color: 'var(--accent-gold)' }}>Blouse or Saree</span>
          </h1>
          <p style={{ color: 'var(--text-secondary)', maxWidth: '640px', margin: '0 auto', fontSize: '1.05rem' }}>
            Upload a saree or blouse photograph. Our AI analyzes fabric texture, dominant colors in LAB space, and visual features to instantly rank your shop's top 4 embroidery patterns.
          </p>
        </div>
      )}

      {/* Error Banner */}
      {error && (
        <div style={{
          background: 'rgba(239, 68, 68, 0.15)',
          border: '1px solid #EF4444',
          color: '#FCA5A5',
          padding: '14px 20px',
          borderRadius: 'var(--radius-sm)',
          marginBottom: '24px',
          textAlign: 'center'
        }}>
          ⚠️ {error}
        </div>
      )}

      {/* Step 1: Upload Form */}
      {!garment && !loading && (
        <ImageUploader onUpload={handleUploadAndAnalyze} isLoading={loading} />
      )}

      {/* Loading Animation */}
      {loading && <LoadingAI />}

      {/* Step 2 & 3: Results View */}
      {garment && !loading && (
        <div>
          {/* Garment Breakdown */}
          <GarmentAnalysisCard garment={garment} onReset={handleReset} />

          {/* Top 4 Recommendations Grid */}
          <div style={{ marginBottom: '24px' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '20px' }}>
              <Trophy size={24} color="var(--accent-gold)" />
              <h2 style={{ fontSize: '1.6rem', color: '#FFF' }}>Top 4 Embroidery Matches</h2>
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '24px' }}>
              {recommendations.map((rec, idx) => (
                <RecommendationCard
                  key={rec.design.id}
                  recommendation={rec}
                  rank={idx + 1}
                  sessionId={garment.upload_id}
                />
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
