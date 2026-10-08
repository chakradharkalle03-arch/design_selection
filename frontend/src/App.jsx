import React, { useState } from 'react';
import Navbar from './components/Navbar';
import SinglePageStudio from './pages/SinglePageStudio';
import DesignLibrary from './pages/DesignLibrary';
import BatchMatch from './pages/BatchMatch';
import Admin from './pages/Admin';

export default function App() {
  const [activeTab, setActiveTab] = useState('match');

  return (
    <div style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column' }}>
      <Navbar activeTab={activeTab} setActiveTab={setActiveTab} />

      <main style={{ flex: 1 }}>
        {activeTab === 'match' && <SinglePageStudio />}
        {activeTab === 'library' && <DesignLibrary />}
        {activeTab === 'batch' && <BatchMatch />}
        {activeTab === 'admin' && <Admin />}
      </main>

      <footer style={{
        borderTop: '1px solid var(--border-color)',
        padding: '24px',
        textAlign: 'center',
        color: 'var(--text-muted)',
        fontSize: '0.82rem',
        marginTop: '60px'
      }}>
        Akshaya Embroidery Design Selection © 2026 — AI Recommendation Engine • Powered by HuggingFace CLIP & LAB Color Harmony
      </footer>
    </div>
  );
}
