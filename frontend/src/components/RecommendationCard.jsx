import React, { useState } from 'react';
import { ThumbsUp, ThumbsDown, Trash2 } from 'lucide-react';
import { submitFeedback, deleteDesign } from '../services/api';

export default function RecommendationCard({ recommendation, rank, sessionId, onDelete }) {
  const { design, match_score, scores_breakdown, reason } = recommendation;
  const [feedback, setFeedback] = useState(null);
  const [showReasonModal, setShowReasonModal] = useState(false);
  const [isDeleting, setIsDeleting] = useState(false);

  const rankBadges = ['⭐ 1st Best Match', '⭐ 2nd Best Match', '⭐ 3rd Best Match', '⭐ 4th Best Match'];
  const badgeText = rankBadges[rank - 1] || `⭐ Rank ${rank}`;

  const handleRating = async (rating) => {
    if (rating === 'like') {
      setFeedback('like');
      try {
        await submitFeedback({
          session_id: sessionId,
          design_code: design.design_code,
          rating: 'like',
          reason: 'Good match'
        });
      } catch (err) {
        console.error(err);
      }
    } else {
      setFeedback('dislike');
      setShowReasonModal(true);
    }
  };

  const handleDislikeReasonSubmit = async (reasonText) => {
    setShowReasonModal(false);
    try {
      await submitFeedback({
        session_id: sessionId,
        design_code: design.design_code,
        rating: 'dislike',
        reason: reasonText
      });
    } catch (err) {
      console.error(err);
    }
  };

  const handleDeleteClick = async () => {
    if (!window.confirm(`Are you sure you want to PERMANENTLY delete design ${design.design_code} from your shop library?`)) {
      return;
    }
    setIsDeleting(true);
    try {
      await deleteDesign(design.id);
      if (onDelete) {
        onDelete(design.id);
      }
    } catch (err) {
      console.error(err);
      alert('Failed to delete design. Please try again.');
      setIsDeleting(false);
    }
  };

  return (
    <div className="glass-panel gold-glow-hover" style={{ padding: '20px', display: 'flex', flexDirection: 'column', height: '100%', position: 'relative' }}>
      {/* Header Rank & Match Score & Delete Button */}
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '14px' }}>
        <span className="badge-gold">{badgeText}</span>
        
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
          <div className="match-score-badge">
            {match_score}%
          </div>
          
          {/* Permanent Delete Button */}
          <button
            onClick={handleDeleteClick}
            disabled={isDeleting}
            style={{
              background: 'rgba(239, 68, 68, 0.15)',
              border: '1px solid rgba(239, 68, 68, 0.4)',
              color: '#EF4444',
              borderRadius: '6px',
              padding: '6px 8px',
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              transition: 'all 0.2s ease',
              opacity: isDeleting ? 0.5 : 1
            }}
            title="Permanently Delete Design from Shop Library"
          >
            <Trash2 size={16} />
          </button>
        </div>
      </div>

      {/* Image Preview */}
      <div style={{
        position: 'relative',
        borderRadius: 'var(--radius-sm)',
        overflow: 'hidden',
        border: '1px solid var(--border-color)',
        marginBottom: '14px',
        height: '210px',
        backgroundColor: '#000'
      }}>
        <img
          src={design.image_url}
          alt={design.name}
          style={{ width: '100%', height: '100%', objectFit: 'cover' }}
        />
        <div style={{
          position: 'absolute',
          bottom: '8px',
          right: '8px',
          background: 'rgba(0,0,0,0.8)',
          padding: '4px 10px',
          borderRadius: '6px',
          fontSize: '0.78rem',
          color: 'var(--accent-gold-light)',
          fontWeight: 700
        }}>
          {design.placement || 'Full Blouse'}
        </div>
      </div>

      {/* Design Details */}
      <div style={{ marginBottom: '14px' }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
          <span style={{ fontSize: '0.78rem', color: 'var(--accent-gold)', fontWeight: 700, textTransform: 'uppercase' }}>
            {design.design_code}
          </span>
          <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>
            {design.category}
          </span>
        </div>
        <h4 style={{ fontSize: '1.05rem', color: '#FFF', margin: '4px 0 8px 0', lineHeight: '1.3' }}>
          {design.name}
        </h4>
        
        {/* Match Rationale */}
        <div style={{
          background: 'rgba(212, 175, 55, 0.08)',
          borderLeft: '3px solid var(--accent-gold)',
          padding: '10px 12px',
          borderRadius: '4px',
          fontSize: '0.84rem',
          color: 'var(--accent-gold-light)',
          lineHeight: '1.4'
        }}>
          💡 {reason}
        </div>
      </div>

      {/* 4-Factor Score Breakdown */}
      <div style={{ marginTop: 'auto', background: 'var(--bg-deep)', padding: '12px', borderRadius: '10px', marginBottom: '14px' }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '8px' }}>
          <span style={{ fontSize: '0.72rem', color: 'var(--accent-gold-light)', fontWeight: 700, textTransform: 'uppercase' }}>
            🤖 Supervisor Multi-Agent Breakdown
          </span>
          <span style={{ fontSize: '0.68rem', background: 'rgba(16, 185, 129, 0.2)', color: '#10B981', padding: '2px 6px', borderRadius: '4px', border: '1px solid rgba(16, 185, 129, 0.4)' }}>
            Consensus Approved
          </span>
        </div>
        
        <ScoreBar label="Motif & Print Pattern (40%)" value={scores_breakdown.motif_pattern_compatibility || scores_breakdown.visual_similarity} color="#EC4899" />
        <ScoreBar label="Color Harmony (35%)" value={scores_breakdown.color_harmony} color="#D4AF37" />
        <ScoreBar label="CLIP Visual Fit (15%)" value={scores_breakdown.visual_similarity} color="#3B82F6" />
        <ScoreBar label="Fabric & Style (10%)" value={scores_breakdown.fabric_suitability} color="#10B981" />
      </div>

      {/* Feedback Controls */}
      <div style={{ borderTop: '1px solid var(--border-color)', paddingTop: '10px', display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        <span style={{ fontSize: '0.78rem', color: 'var(--text-secondary)' }}>
          Helpful recommendation?
        </span>
        <div style={{ display: 'flex', gap: '8px' }}>
          <button
            onClick={() => handleRating('like')}
            style={{
              background: feedback === 'like' ? 'rgba(16, 185, 129, 0.2)' : 'var(--bg-card)',
              border: feedback === 'like' ? '1px solid #10B981' : '1px solid var(--border-color)',
              color: feedback === 'like' ? '#10B981' : 'var(--text-secondary)',
              padding: '5px 10px',
              borderRadius: '6px',
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              gap: '4px',
              fontSize: '0.78rem'
            }}
          >
            <ThumbsUp size={14} /> Yes
          </button>
          <button
            onClick={() => handleRating('dislike')}
            style={{
              background: feedback === 'dislike' ? 'rgba(239, 68, 68, 0.2)' : 'var(--bg-card)',
              border: feedback === 'dislike' ? '1px solid #EF4444' : '1px solid var(--border-color)',
              color: feedback === 'dislike' ? '#EF4444' : 'var(--text-secondary)',
              padding: '5px 10px',
              borderRadius: '6px',
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              gap: '4px',
              fontSize: '0.78rem'
            }}
          >
            <ThumbsDown size={14} /> No
          </button>
        </div>
      </div>

      {/* Dislike Reason Modal */}
      {showReasonModal && (
        <div style={{
          position: 'absolute',
          inset: 0,
          background: 'rgba(11, 14, 20, 0.95)',
          borderRadius: 'var(--radius-md)',
          padding: '20px',
          zIndex: 10,
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'center'
        }}>
          <h5 style={{ fontSize: '0.92rem', color: '#FFF', marginBottom: '12px' }}>Why was this recommendation not suitable?</h5>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
            {['Color mismatch', 'Design style mismatch', 'Fabric mismatch', 'Too heavy', 'Too simple'].map((item) => (
              <button
                key={item}
                onClick={() => handleDislikeReasonSubmit(item)}
                style={{
                  background: 'var(--bg-card)',
                  border: '1px solid var(--border-color)',
                  color: 'var(--text-primary)',
                  padding: '8px 12px',
                  borderRadius: '6px',
                  textAlign: 'left',
                  fontSize: '0.82rem',
                  cursor: 'pointer'
                }}
              >
                ○ {item}
              </button>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

function ScoreBar({ label, value, color }) {
  return (
    <div style={{ marginBottom: '6px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.72rem', color: 'var(--text-muted)', marginBottom: '2px' }}>
        <span>{label}</span>
        <span style={{ fontWeight: 600, color: '#FFF' }}>{value}%</span>
      </div>
      <div style={{ height: '4px', background: 'rgba(255,255,255,0.1)', borderRadius: '2px', overflow: 'hidden' }}>
        <div style={{ width: `${value}%`, height: '100%', background: color, transition: 'width 0.5s ease' }} />
      </div>
    </div>
  );
}
