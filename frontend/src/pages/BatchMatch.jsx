import React, { useState, useEffect } from 'react';
import ImageUploader from '../components/ImageUploader';
import RecommendationCard from '../components/RecommendationCard';
import LoadingAI from '../components/LoadingAI';
import { analyzeGarment, fetchDesigns, fetchRecommendations } from '../services/api';
import { Layers, Sparkles, CheckSquare, Square, Play } from 'lucide-react';

export default function BatchMatch() {
  const [garment, setGarment] = useState(null);
  const [libraryDesigns, setLibraryDesigns] = useState([]);
  const [selectedDesignIds, setSelectedDesignIds] = useState([]);
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchDesigns('all').then(setLibraryDesigns).catch(console.error);
  }, []);

  const handleUpload = async (file, garmentType) => {
    setLoading(true);
    try {
      const data = await analyzeGarment(file, garmentType);
      setGarment(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const toggleSelectDesign = (id) => {
    if (selectedDesignIds.includes(id)) {
      setSelectedDesignIds(selectedDesignIds.filter(item => item !== id));
    } else {
      setSelectedDesignIds([...selectedDesignIds, id]);
    }
  };

  const selectAll = () => {
    setSelectedDesignIds(libraryDesigns.map(d => d.id));
  };

  const deselectAll = () => {
    setSelectedDesignIds([]);
  };

  const runBatchMatch = async () => {
    if (!garment || selectedDesignIds.length === 0) return;
    setLoading(true);
    try {
      const recData = await fetchRecommendations(garment.upload_id, selectedDesignIds);
      setRecommendations(recData.top_recommendations || []);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: '1280px', margin: '0 auto', padding: '32px 24px' }}>
      <div style={{ textAlign: 'center', marginBottom: '32px' }}>
        <div style={{ display: 'inline-flex', alignItems: 'center', gap: '8px', marginBottom: '12px' }} className="badge-gold">
          <Layers size={14} /> MODE B: CANDIDATE BATCH CONSULTATION
        </div>
        <h1 style={{ fontSize: '2rem', color: '#FFF' }}>
          Compare Blouse against <span style={{ color: 'var(--accent-gold)' }}>Selected Design Subset</span>
        </h1>
        <p style={{ color: 'var(--text-secondary)', maxWidth: '600px', margin: '0 auto', fontSize: '0.95rem' }}>
          Customer uploaded a blouse and wants to choose between 5 or 10 specific embroidery patterns? Pick the candidate subset below.
        </p>
      </div>

      {!garment && !loading && (
        <ImageUploader onUpload={handleUpload} isLoading={loading} />
      )}

      {loading && <LoadingAI />}

      {garment && !loading && recommendations.length === 0 && (
        <div>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '16px' }}>
            <h3 style={{ fontSize: '1.2rem', color: '#FFF' }}>
              Select Candidate Embroidery Patterns ({selectedDesignIds.length} Selected)
            </h3>
            <div style={{ display: 'flex', gap: '8px' }}>
              <button onClick={selectAll} className="btn-secondary" style={{ padding: '6px 12px', fontSize: '0.8rem' }}>Select All</button>
              <button onClick={deselectAll} className="btn-secondary" style={{ padding: '6px 12px', fontSize: '0.8rem' }}>Deselect All</button>
              <button
                onClick={runBatchMatch}
                disabled={selectedDesignIds.length === 0}
                className="btn-gold"
                style={{ opacity: selectedDesignIds.length === 0 ? 0.5 : 1 }}
              >
                <Play size={16} /> Run Candidate Batch Match ({selectedDesignIds.length})
              </button>
            </div>
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(220px, 1fr))', gap: '16px' }}>
            {libraryDesigns.map((d) => {
              const isSelected = selectedDesignIds.includes(d.id);
              return (
                <div
                  key={d.id}
                  onClick={() => toggleSelectDesign(d.id)}
                  className="glass-panel"
                  style={{
                    padding: '12px',
                    cursor: 'pointer',
                    border: isSelected ? '2px solid var(--accent-gold)' : '1px solid var(--border-color)',
                    background: isSelected ? 'rgba(212, 175, 55, 0.12)' : 'var(--bg-card)',
                    borderRadius: 'var(--radius-sm)'
                  }}
                >
                  <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '8px' }}>
                    <span style={{ fontSize: '0.78rem', color: 'var(--accent-gold)', fontWeight: 700 }}>{d.design_code}</span>
                    {isSelected ? <CheckSquare size={18} color="var(--accent-gold)" /> : <Square size={18} color="var(--text-muted)" />}
                  </div>
                  <img src={d.image_url} alt={d.name} style={{ width: '100%', height: '140px', objectFit: 'cover', borderRadius: '6px', marginBottom: '8px' }} />
                  <div style={{ fontSize: '0.9rem', color: '#FFF', fontWeight: 600 }}>{d.name}</div>
                </div>
              );
            })}
          </div>
        </div>
      )}

      {recommendations.length > 0 && (
        <div>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '24px' }}>
            <h2 style={{ fontSize: '1.6rem', color: '#FFF' }}>Top Matches from Selected Batch</h2>
            <button onClick={() => setRecommendations([])} className="btn-secondary">
              ← Change Selected Candidates
            </button>
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
      )}
    </div>
  );
}
