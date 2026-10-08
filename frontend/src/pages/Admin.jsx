import React, { useState, useEffect } from 'react';
import { fetchFeedbackStats } from '../services/api';
import { BarChart3, ThumbsUp, ThumbsDown, Award, AlertCircle } from 'lucide-react';

export default function Admin() {
  const [stats, setStats] = useState(null);

  useEffect(() => {
    fetchFeedbackStats().then(setStats).catch(console.error);
  }, []);

  if (!stats) {
    return (
      <div style={{ maxWidth: '1280px', margin: '0 auto', padding: '48px 24px', color: 'var(--accent-gold)' }}>
        Loading feedback analytics...
      </div>
    );
  }

  return (
    <div style={{ maxWidth: '1280px', margin: '0 auto', padding: '32px 24px' }}>
      <div style={{ marginBottom: '32px' }}>
        <h1 style={{ fontSize: '1.8rem', color: '#FFF' }}>Recommendation Analytics & Active Feedback</h1>
        <p style={{ color: 'var(--text-secondary)', fontSize: '0.92rem' }}>
          Customer & embroidery designer feedback logs collected to build fine-tuning dataset for custom AI models.
        </p>
      </div>

      {/* KPI Stat Cards */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: '20px', marginBottom: '32px' }}>
        <StatCard
          icon={Award}
          label="Approval Rate"
          value={`${stats.approval_rate}%`}
          color="#D4AF37"
        />
        <StatCard
          icon={BarChart3}
          label="Total Customer Logs"
          value={stats.total_feedback_logs}
          color="#3B82F6"
        />
        <StatCard
          icon={ThumbsUp}
          label="Positive Approvals (👍)"
          value={stats.likes}
          color="#10B981"
        />
        <StatCard
          icon={ThumbsDown}
          label="Dislike Adjustments (👎)"
          value={stats.dislikes}
          color="#EF4444"
        />
      </div>

      {/* Feedback Breakdown */}
      <div className="glass-panel" style={{ padding: '24px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '16px' }}>
          <AlertCircle size={20} color="var(--accent-gold)" />
          <h3 style={{ fontSize: '1.2rem', color: '#FFF' }}>Dislike Rationale Breakdown (For Fine-Tuning)</h3>
        </div>

        {Object.keys(stats.dislike_reasons_breakdown || {}).length === 0 ? (
          <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem' }}>
            No negative feedback logged yet! Recommendations are performing with high customer satisfaction.
          </p>
        ) : (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
            {Object.entries(stats.dislike_reasons_breakdown).map(([reason, count]) => (
              <div key={reason} style={{ background: 'var(--bg-deep)', padding: '12px 16px', borderRadius: '8px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <span style={{ color: '#FFF', fontWeight: 500 }}>{reason}</span>
                <span className="badge-gold">{count} occurrences</span>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

function StatCard({ icon: Icon, label, value, color }) {
  return (
    <div className="glass-panel" style={{ padding: '20px', display: 'flex', alignItems: 'center', gap: '16px' }}>
      <div style={{
        width: '48px',
        height: '48px',
        borderRadius: '12px',
        background: `${color}20`,
        border: `1px solid ${color}40`,
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center'
      }}>
        <Icon size={24} color={color} />
      </div>
      <div>
        <div style={{ fontSize: '0.78rem', color: 'var(--text-secondary)', textTransform: 'uppercase' }}>{label}</div>
        <div style={{ fontSize: '1.5rem', fontWeight: 800, color: '#FFF' }}>{value}</div>
      </div>
    </div>
  );
}
