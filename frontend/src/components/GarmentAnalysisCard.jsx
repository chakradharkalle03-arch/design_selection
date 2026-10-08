import React from 'react';
import { Palette, Shirt, Sparkles, RefreshCw } from 'lucide-react';

export default function GarmentAnalysisCard({ garment, onReset }) {
  if (!garment) return null;

  return (
    <div className="glass-panel" style={{ padding: '24px', marginBottom: '32px' }}>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '20px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
          <Sparkles size={20} color="var(--accent-gold)" />
          <h3 style={{ fontSize: '1.2rem', color: '#FFF' }}>AI Garment Analysis</h3>
        </div>
        <button onClick={onReset} className="btn-secondary" style={{ padding: '6px 14px', fontSize: '0.82rem' }}>
          <RefreshCw size={14} /> Upload New Garment
        </button>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '180px 1fr', gap: '24px', alignItems: 'center' }}>
        {/* Garment Image */}
        <div style={{ borderRadius: '12px', overflow: 'hidden', border: '1px solid var(--border-color)', position: 'relative' }}>
          <img
            src={garment.image_url}
            alt="Uploaded Garment"
            style={{ width: '100%', height: '180px', objectFit: 'cover', display: 'block' }}
          />
          <div style={{
            position: 'absolute',
            bottom: '8px',
            left: '8px',
            background: 'rgba(0,0,0,0.75)',
            padding: '2px 8px',
            borderRadius: '6px',
            fontSize: '0.75rem',
            color: 'var(--accent-gold-light)',
            fontWeight: 600,
            textTransform: 'capitalize'
          }}>
            {garment.garment_type || 'Blouse'}
          </div>
        </div>

        {/* AI Extracted Characteristics */}
        <div>
          {/* Dominant Colors */}
          <div style={{ marginBottom: '16px' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '6px', color: 'var(--text-secondary)', fontSize: '0.85rem', marginBottom: '8px' }}>
              <Palette size={15} color="var(--accent-gold)" /> Dominant Garment Colors
            </div>
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '10px' }}>
              {garment.colors && garment.colors.map((c, idx) => (
                <div key={idx} style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: '8px',
                  background: 'var(--bg-deep)',
                  padding: '6px 12px',
                  borderRadius: 'var(--radius-full)',
                  border: '1px solid var(--border-color)',
                  fontSize: '0.82rem',
                  color: '#FFF'
                }}>
                  <span style={{
                    width: '14px',
                    height: '14px',
                    borderRadius: '50%',
                    backgroundColor: c.hex || '#800000',
                    border: '1px solid rgba(255,255,255,0.3)',
                    boxShadow: '0 0 5px rgba(0,0,0,0.5)'
                  }} />
                  <span style={{ fontWeight: 600 }}>{c.name}</span>
                  <span style={{ color: 'var(--accent-gold-light)', fontSize: '0.75rem' }}>{c.percentage}%</span>
                </div>
              ))}
            </div>
          </div>

          {/* Fabric & Style Tags */}
          <div style={{ display: 'flex', gap: '16px', flexWrap: 'wrap' }}>
            <div style={{ background: 'rgba(16, 185, 129, 0.1)', border: '1px solid rgba(16, 185, 129, 0.25)', padding: '8px 16px', borderRadius: '10px' }}>
              <div style={{ fontSize: '0.72rem', color: '#34D399', textTransform: 'uppercase', letterSpacing: '0.5px' }}>Detected Fabric</div>
              <div style={{ color: '#FFF', fontWeight: 700, fontSize: '0.95rem', textTransform: 'capitalize' }}>
                🧵 {garment.fabric || 'silk-like'}
              </div>
            </div>

            <div style={{ background: 'rgba(59, 130, 246, 0.1)', border: '1px solid rgba(59, 130, 246, 0.25)', padding: '8px 16px', borderRadius: '10px' }}>
              <div style={{ fontSize: '0.72rem', color: '#60A5FA', textTransform: 'uppercase', letterSpacing: '0.5px' }}>Visual Style</div>
              <div style={{ color: '#FFF', fontWeight: 700, fontSize: '0.95rem', textTransform: 'capitalize' }}>
                ✨ {garment.style || 'Traditional'}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
