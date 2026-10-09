import React from 'react';
import { Sparkles, Grid, Layers, BarChart3, Feather } from 'lucide-react';

export default function Navbar({ activeTab, setActiveTab }) {
  const tabs = [
    { id: 'match', label: 'AI Matcher Studio', icon: Sparkles },
    { id: 'library', label: 'Design Library', icon: Grid },
    { id: 'batch', label: 'Batch Matcher', icon: Layers },
    { id: 'admin', label: 'Analytics & Feedback', icon: BarChart3 },
  ];

  return (
    <header style={{
      borderBottom: '1px solid var(--border-color)',
      background: 'rgba(11, 14, 20, 0.88)',
      backdropFilter: 'blur(16px)',
      position: 'sticky',
      top: 0,
      zIndex: 100,
      padding: '0 24px'
    }}>
      <div style={{
        maxWidth: '1280px',
        margin: '0 auto',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        height: '72px'
      }}>
        {/* Brand Logo */}
        <div 
          onClick={() => setActiveTab('match')}
          style={{ display: 'flex', alignItems: 'center', gap: '12px', cursor: 'pointer' }}
        >
          <div style={{
            width: '40px',
            height: '40px',
            borderRadius: '10px',
            background: 'linear-gradient(135deg, #D4AF37 0%, #800020 100%)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            boxShadow: '0 0 15px rgba(212, 175, 55, 0.4)'
          }}>
            <Feather size={22} color="#FFF" />
          </div>
          <div>
            <h1 style={{ fontSize: '1.2rem', fontWeight: 800, letterSpacing: '-0.5px', color: '#FFF' }}>
              Akshaya <span style={{ color: 'var(--accent-gold)' }}>Embroidery</span>
            </h1>
            <p style={{ fontSize: '0.68rem', color: 'var(--text-secondary)', textTransform: 'uppercase', letterSpacing: '0.8px' }}>
              Design Selection AI
            </p>
          </div>
        </div>

        {/* Navigation Tabs */}
        <nav className="mobile-nav" style={{ display: 'flex', gap: '6px', flexWrap: 'wrap' }}>
          {tabs.map((tab) => {
            const Icon = tab.icon;
            const isActive = activeTab === tab.id;
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className="nav-btn"
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: '6px',
                  padding: '8px 12px',
                  borderRadius: 'var(--radius-sm)',
                  border: isActive ? '1px solid var(--accent-gold)' : '1px solid transparent',
                  background: isActive ? 'rgba(212, 175, 55, 0.15)' : 'transparent',
                  color: isActive ? 'var(--accent-gold-light)' : 'var(--text-secondary)',
                  fontWeight: isActive ? 600 : 400,
                  fontSize: '0.85rem',
                  cursor: 'pointer',
                  transition: 'all 0.2s ease'
                }}
              >
                <Icon size={18} color={isActive ? 'var(--accent-gold)' : 'currentColor'} />
                <span className="nav-label">{tab.label}</span>
              </button>
            );
          })}
        </nav>
      </div>
    </header>
  );
}
