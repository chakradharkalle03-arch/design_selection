import React from 'react';
import { Trash2, CheckCircle2 } from 'lucide-react';

export default function DesignCard({ design, onDelete }) {
  return (
    <div className="glass-panel gold-glow-hover" style={{ padding: '16px', display: 'flex', flexDirection: 'column', height: '100%' }}>
      {/* Design Image Thumbnail */}
      <div style={{
        position: 'relative',
        borderRadius: '8px',
        overflow: 'hidden',
        height: '180px',
        marginBottom: '12px',
        background: '#000'
      }}>
        <img
          src={design.image_url}
          alt={design.name}
          style={{ width: '100%', height: '100%', objectFit: 'cover' }}
        />
        <div style={{
          position: 'absolute',
          top: '8px',
          left: '8px',
          background: 'rgba(0,0,0,0.75)',
          padding: '2px 8px',
          borderRadius: '4px',
          fontSize: '0.72rem',
          color: 'var(--accent-gold)',
          fontWeight: 700
        }}>
          {design.design_code}
        </div>
        <div style={{
          position: 'absolute',
          bottom: '8px',
          right: '8px',
          background: 'rgba(0,0,0,0.75)',
          padding: '2px 8px',
          borderRadius: '4px',
          fontSize: '0.72rem',
          color: '#FFF',
          fontWeight: 600
        }}>
          {design.placement}
        </div>
      </div>

      {/* Info */}
      <div style={{ marginBottom: '12px' }}>
        <h4 style={{ fontSize: '1rem', color: '#FFF', marginBottom: '4px' }}>{design.name}</h4>
        <div style={{ display: 'flex', gap: '8px', fontSize: '0.78rem', color: 'var(--text-secondary)' }}>
          <span>{design.category}</span>
          <span>•</span>
          <span>{design.style}</span>
        </div>
      </div>

      {/* Precomputed Embedding Indicator */}
      <div style={{ marginTop: 'auto', pt: '8px', display: 'flex', alignItems: 'center', justifyContent: 'space-between', borderTop: '1px solid var(--border-color)' }}>
        <span style={{ display: 'flex', alignItems: 'center', gap: '4px', fontSize: '0.72rem', color: '#10B981' }}>
          <CheckCircle2 size={12} /> AI Embedding Saved
        </span>
        {onDelete && (
          <button
            onClick={() => onDelete(design.id)}
            style={{
              background: 'transparent',
              border: 'none',
              color: '#EF4444',
              cursor: 'pointer',
              padding: '4px',
              display: 'flex',
              alignItems: 'center'
            }}
            title="Delete Design"
          >
            <Trash2 size={16} />
          </button>
        )}
      </div>
    </div>
  );
}
