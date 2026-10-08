import React, { useEffect, useState } from 'react';
import { Sparkles, Cpu, Palette, Feather } from 'lucide-react';

export default function LoadingAI() {
  const messages = [
    "Analyzing garment ROI & cropping background...",
    "Extracting dominant colors & converting RGB → LAB space...",
    "Generating 512-dim CLIP vision embedding...",
    "Evaluating color harmony & zari contrast matrix...",
    "Calculating fabric texture & style suitability...",
    "Ranking Top 4 best embroidery designs..."
  ];

  const [index, setIndex] = useState(0);

  useEffect(() => {
    const timer = setInterval(() => {
      setIndex((prev) => (prev + 1) % messages.length);
    }, 1200);
    return () => clearInterval(timer);
  }, []);

  return (
    <div className="glass-panel pulse-loader" style={{ padding: '48px', textAlign: 'center', maxWidth: '540px', margin: '40px auto' }}>
      <div style={{
        width: '72px',
        height: '72px',
        borderRadius: '50%',
        background: 'linear-gradient(135deg, #D4AF37 0%, #800020 100%)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        margin: '0 auto 24px auto',
        boxShadow: '0 0 30px rgba(212, 175, 55, 0.5)'
      }}>
        <Cpu size={36} color="#FFF" />
      </div>

      <h3 style={{ fontSize: '1.4rem', color: '#FFF', marginBottom: '8px' }}>
        AI Recommendation Engine Active
      </h3>
      
      <p style={{ color: 'var(--accent-gold-light)', fontSize: '0.95rem', minHeight: '28px', fontWeight: 500 }}>
        ✨ {messages[index]}
      </p>

      {/* Progress Line */}
      <div style={{
        width: '80%',
        height: '4px',
        background: 'rgba(255,255,255,0.1)',
        borderRadius: '2px',
        margin: '24px auto 0 auto',
        overflow: 'hidden'
      }}>
        <div style={{
          width: '100%',
          height: '100%',
          background: 'linear-gradient(90deg, transparent, var(--accent-gold), transparent)',
          animation: 'shimmer 1.5s infinite'
        }} />
      </div>
    </div>
  );
}
