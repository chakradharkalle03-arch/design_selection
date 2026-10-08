import React, { useState, useEffect } from 'react';
import { UploadCloud, Sparkles, FileText, CheckCircle2, Trophy, Shirt, Palette, Grid, MessageSquareText, FolderPlus, FilePlus, Trash2 } from 'lucide-react';
import { analyzeGarment, fetchRecommendations, uploadDesign, fetchDesigns, deleteAllDesigns } from '../services/api';
import LoadingAI from '../components/LoadingAI';
import RecommendationCard from '../components/RecommendationCard';
import GarmentAnalysisCard from '../components/GarmentAnalysisCard';

export default function SinglePageStudio() {
  // Upload State 1: Embroidery Designs
  const [designFiles, setDesignFiles] = useState([]);
  const [designCount, setDesignCount] = useState(0);
  const [designUploadSuccess, setDesignUploadSuccess] = useState(null);
  const [isUploadingDesigns, setIsUploadingDesigns] = useState(false);

  // Upload State 2: Blouse or Saree
  const [garmentFile, setGarmentFile] = useState(null);
  const [garmentPreview, setGarmentPreview] = useState(null);
  const [isGarmentPdf, setIsGarmentPdf] = useState(false);
  const [garmentType, setGarmentType] = useState('blouse');

  // State 3: Customer Requirements Text Prompt Input
  const [customerRequirements, setCustomerRequirements] = useState('');

  // AI Processing & Results
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [garmentAnalysis, setGarmentAnalysis] = useState(null);
  const [recommendations, setRecommendations] = useState([]);

  useEffect(() => {
    loadLibraryCount();
  }, []);

  const loadLibraryCount = async () => {
    try {
      const list = await fetchDesigns('all');
      setDesignCount(list.length);
    } catch (e) {
      console.error(e);
    }
  };

  // Delete All Designs Handler
  const handleDeleteAllDesigns = async () => {
    if (!window.confirm(`⚠️ DANGER: Are you sure you want to PERMANENTLY DELETE ALL ${designCount} embroidery designs from your shop library? This action cannot be undone.`)) {
      return;
    }
    try {
      await deleteAllDesigns();
      setDesignCount(0);
      setRecommendations([]);
      setDesignUploadSuccess('✅ All shop library designs deleted.');
    } catch (err) {
      console.error(err);
      alert('Failed to delete all designs.');
    }
  };

  // Handle Multi-Page PDF, Single/Multiple Files, or Folder Uploads
  const handleDesignFilesChange = async (e, isFolder = false) => {
    const files = Array.from(e.target.files || []);
    if (files.length === 0) return;

    setDesignFiles(files);
    setIsUploadingDesigns(true);
    setDesignUploadSuccess(`Processing ${files.length} design file(s)${isFolder ? ' from folder' : ''}...`);

    try {
      let totalExtractedPages = 0;
      for (let i = 0; i < files.length; i++) {
        const file = files[i];
        // Skip non-image / non-pdf system files if folder upload
        const ext = file.name.toLowerCase();
        if (!ext.endsWith('.jpg') && !ext.endsWith('.jpeg') && !ext.endsWith('.png') && !ext.endsWith('.webp') && !ext.endsWith('.pdf')) {
          continue;
        }

        const formData = new FormData();
        formData.append('file', file);
        formData.append('name', file.name.replace(/\.[^/.]+$/, ""));
        formData.append('category', 'Traditional');
        formData.append('style', 'Floral');
        formData.append('placement', 'Full Blouse');
        const res = await uploadDesign(formData);
        if (res.processed_pages) {
          totalExtractedPages += res.processed_pages;
        } else {
          totalExtractedPages += 1;
        }
      }
      await loadLibraryCount();
      setDesignUploadSuccess(`✅ Successfully added ${totalExtractedPages} pattern(s) to AI library!`);
    } catch (err) {
      console.error(err);
      setDesignUploadSuccess(`ℹ️ Ready: Using existing shop catalog (${designCount} designs) for AI matching.`);
    } finally {
      setIsUploadingDesigns(false);
    }
  };

  const handleGarmentFileChange = (file) => {
    if (!file) return;
    setGarmentFile(file);
    const fileIsPdf = file.type === 'application/pdf' || file.name.toLowerCase().endsWith('.pdf');
    setIsGarmentPdf(fileIsPdf);

    if (fileIsPdf) {
      setGarmentPreview(null);
    } else {
      setGarmentPreview(URL.createObjectURL(file));
    }
  };

  const handleRunAIProcess = async (e) => {
    e.preventDefault();
    if (!garmentFile) {
      setError('Please upload a blouse or saree photograph / PDF before running AI process.');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const garmentData = await analyzeGarment(garmentFile, garmentType);
      setGarmentAnalysis(garmentData);

      const recData = await fetchRecommendations(garmentData.upload_id, null, customerRequirements);
      setRecommendations(recData.top_recommendations || []);

      setTimeout(() => {
        const resultsEl = document.getElementById('ai-results-section');
        if (resultsEl) {
          resultsEl.scrollIntoView({ behavior: 'smooth' });
        }
      }, 300);
    } catch (err) {
      console.error(err);
      setError(err.response?.data?.detail || 'Failed to process AI recommendation. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: '1280px', margin: '0 auto', padding: '36px 20px' }}>
      
      {/* Header Banner */}
      <div style={{ textAlign: 'center', marginBottom: '32px' }}>
        <div style={{ display: 'inline-flex', alignItems: 'center', gap: '8px', marginBottom: '12px' }} className="badge-gold">
          <Sparkles size={14} /> AI EMBROIDERY MATCHING ENGINE
        </div>
        <h1 style={{ fontSize: '2.5rem', fontWeight: 800, color: '#FFF', letterSpacing: '-0.5px' }}>
          Akshaya Embroidery <span style={{ color: 'var(--accent-gold)' }}>Design Selection</span>
        </h1>
        <p style={{ color: 'var(--text-secondary)', fontSize: '1rem', marginTop: '6px' }}>
          Upload single files, multi-page PDFs, or an entire folder of catalog designs.
        </p>
      </div>

      {/* Error Banner */}
      {error && (
        <div style={{
          background: 'rgba(239, 68, 68, 0.15)',
          border: '1px solid #EF4444',
          color: '#FCA5A5',
          padding: '12px 20px',
          borderRadius: 'var(--radius-sm)',
          marginBottom: '24px',
          textAlign: 'center',
          fontSize: '0.92rem'
        }}>
          ⚠️ {error}
        </div>
      )}

      {/* TWO UPLOAD PANELS */}
      <form onSubmit={handleRunAIProcess}>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(340px, 1fr))', gap: '24px', marginBottom: '24px' }}>
          
          {/* UPLOAD PANEL 1: EMBROIDERY DESIGNS (Single, Multi-files, Multi-page PDF, or Folder) */}
          <div className="glass-panel" style={{ padding: '24px', display: 'flex', flexDirection: 'column' }}>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '14px' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                <div style={{
                  width: '32px',
                  height: '32px',
                  borderRadius: '50%',
                  background: 'var(--accent-gold)',
                  color: '#000',
                  fontWeight: 800,
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  fontSize: '0.95rem'
                }}>1</div>
                <h3 style={{ fontSize: '1.2rem', color: '#FFF' }}>Upload Design Files or Folder</h3>
              </div>

              {/* Single Button for DELETE ALL DESIGNS */}
              {designCount > 0 && (
                <button
                  type="button"
                  onClick={handleDeleteAllDesigns}
                  style={{
                    background: 'rgba(239, 68, 68, 0.2)',
                    border: '1px solid #EF4444',
                    color: '#EF4444',
                    padding: '4px 10px',
                    borderRadius: '6px',
                    fontSize: '0.78rem',
                    fontWeight: 600,
                    cursor: 'pointer',
                    display: 'flex',
                    alignItems: 'center',
                    gap: '4px'
                  }}
                  title="Delete All Designs in Shop Library"
                >
                  <Trash2 size={14} /> Delete All ({designCount})
                </button>
              )}
            </div>

            <p style={{ color: 'var(--text-secondary)', fontSize: '0.85rem', marginBottom: '16px' }}>
              Upload single, multiple 2+ pattern files, multi-page PDFs, or select an entire folder. ({designCount} designs in AI library)
            </p>

            {/* Dual Pickers: Files vs Folder */}
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '10px', marginTop: 'auto', marginBottom: '12px' }}>
              <button
                type="button"
                onClick={() => document.getElementById('files-input-picker').click()}
                className="btn-secondary"
                style={{ padding: '12px', justifyContent: 'center', flexDirection: 'column', gap: '4px' }}
              >
                <FilePlus size={22} color="var(--accent-gold)" />
                <span style={{ fontSize: '0.84rem', fontWeight: 600 }}>1, 2+ Files or PDFs</span>
              </button>

              <button
                type="button"
                onClick={() => document.getElementById('folder-input-picker').click()}
                className="btn-secondary"
                style={{ padding: '12px', justifyContent: 'center', flexDirection: 'column', gap: '4px' }}
              >
                <FolderPlus size={22} color="var(--accent-gold)" />
                <span style={{ fontSize: '0.84rem', fontWeight: 600 }}>Upload Folder</span>
              </button>
            </div>

            {/* Hidden Inputs */}
            <input
              id="files-input-picker"
              type="file"
              multiple
              accept="image/*,application/pdf,.pdf"
              style={{ display: 'none' }}
              onChange={(e) => handleDesignFilesChange(e, false)}
            />

            <input
              id="folder-input-picker"
              type="file"
              webkitdirectory=""
              directory=""
              mozdirectory=""
              multiple
              style={{ display: 'none' }}
              onChange={(e) => handleDesignFilesChange(e, true)}
            />

            {designUploadSuccess && (
              <div style={{ color: 'var(--accent-gold-light)', fontSize: '0.82rem', fontWeight: 600, textAlign: 'center' }}>
                {designUploadSuccess}
              </div>
            )}
          </div>

          {/* UPLOAD PANEL 2: BLOUSE OR SAREE */}
          <div className="glass-panel" style={{ padding: '24px', display: 'flex', flexDirection: 'column' }}>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '14px' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                <div style={{
                  width: '32px',
                  height: '32px',
                  borderRadius: '50%',
                  background: 'var(--accent-gold)',
                  color: '#000',
                  fontWeight: 800,
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  fontSize: '0.95rem'
                }}>2</div>
                <h3 style={{ fontSize: '1.2rem', color: '#FFF' }}>Upload Blouse or Saree</h3>
              </div>

              <div style={{ display: 'flex', background: 'var(--bg-deep)', padding: '2px', borderRadius: '6px', border: '1px solid var(--border-color)' }}>
                <button
                  type="button"
                  onClick={() => setGarmentType('blouse')}
                  style={{
                    padding: '4px 12px',
                    borderRadius: '4px',
                    border: 'none',
                    background: garmentType === 'blouse' ? 'var(--accent-gold)' : 'transparent',
                    color: garmentType === 'blouse' ? '#000' : 'var(--text-secondary)',
                    fontWeight: 600,
                    fontSize: '0.78rem',
                    cursor: 'pointer'
                  }}
                >
                  Blouse
                </button>
                <button
                  type="button"
                  onClick={() => setGarmentType('saree')}
                  style={{
                    padding: '4px 12px',
                    borderRadius: '4px',
                    border: 'none',
                    background: garmentType === 'saree' ? 'var(--accent-gold)' : 'transparent',
                    color: garmentType === 'saree' ? '#000' : 'var(--text-secondary)',
                    fontWeight: 600,
                    fontSize: '0.78rem',
                    cursor: 'pointer'
                  }}
                >
                  Saree
                </button>
              </div>
            </div>

            <p style={{ color: 'var(--text-secondary)', fontSize: '0.85rem', marginBottom: '16px' }}>
              Upload customer's blouse or saree photo / PDF page.
            </p>

            <div
              style={{
                border: garmentFile ? '2px solid var(--accent-gold)' : '2px dashed var(--border-color)',
                borderRadius: 'var(--radius-sm)',
                padding: '16px',
                background: 'rgba(11, 14, 20, 0.5)',
                textAlign: 'center',
                cursor: 'pointer',
                marginBottom: '12px',
                marginTop: 'auto'
              }}
              onClick={() => document.getElementById('garment-input-file').click()}
            >
              <input
                id="garment-input-file"
                type="file"
                accept="image/*,application/pdf,.pdf"
                style={{ display: 'none' }}
                onChange={(e) => handleGarmentFileChange(e.target.files[0])}
              />

              {isGarmentPdf ? (
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '8px', color: '#FFF' }}>
                  <FileText size={24} color="#EF4444" />
                  <span style={{ fontWeight: 600, fontSize: '0.9rem' }}>{garmentFile.name} (PDF Selected)</span>
                </div>
              ) : garmentPreview ? (
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '12px' }}>
                  <img src={garmentPreview} alt="Garment Preview" style={{ height: '70px', borderRadius: '6px', objectFit: 'cover' }} />
                  <div style={{ textAlign: 'left', fontSize: '0.85rem', color: 'var(--accent-gold-light)' }}>
                    <CheckCircle2 size={16} color="var(--accent-gold)" /> Ready for AI Process
                  </div>
                </div>
              ) : (
                <div>
                  <Shirt size={32} color="var(--accent-gold)" style={{ margin: '0 auto 8px auto' }} />
                  <p style={{ color: '#FFF', fontWeight: 600, fontSize: '0.9rem' }}>
                    Click or Drop Blouse/Saree Photo or PDF
                  </p>
                  <p style={{ color: 'var(--text-muted)', fontSize: '0.78rem', marginTop: '4px' }}>
                    Supports JPG, PNG, WEBP, and PDF
                  </p>
                </div>
              )}
            </div>
          </div>

        </div>

        {/* INPUT BOX 3: CUSTOMER REQUIREMENTS TEXT PROMPT */}
        <div className="glass-panel" style={{ padding: '20px', marginBottom: '28px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '8px' }}>
            <MessageSquareText size={18} color="var(--accent-gold)" />
            <label style={{ fontSize: '0.95rem', fontWeight: 700, color: '#FFF' }}>
              Customer Requirements & Style Preferences (Optional AI Prompt)
            </label>
          </div>
          <input
            type="text"
            placeholder="e.g. Heavy bridal gold zari peacock work for traditional South Indian silk saree..."
            value={customerRequirements}
            onChange={(e) => setCustomerRequirements(e.target.value)}
            style={{
              width: '100%',
              background: 'var(--bg-deep)',
              border: '1px solid var(--border-color)',
              borderRadius: '8px',
              padding: '12px 16px',
              color: '#FFF',
              fontSize: '0.92rem',
              outline: 'none'
            }}
          />
        </div>

        {/* SUBMIT BUTTON */}
        <div style={{ textAlign: 'center', marginBottom: '40px' }}>
          <button
            type="submit"
            disabled={!garmentFile || loading || isUploadingDesigns}
            className="btn-gold"
            style={{
              padding: '16px 48px',
              fontSize: '1.15rem',
              borderRadius: 'var(--radius-md)',
              opacity: !garmentFile || loading || isUploadingDesigns ? 0.6 : 1,
              boxShadow: '0 0 25px rgba(212, 175, 55, 0.4)'
            }}
          >
            <Sparkles size={22} />
            {loading ? 'AI Engine Processing Garment & Matching Designs...' : 'Run AI Embroidery Matching'}
          </button>
        </div>
      </form>

      {/* AI LOADING ANIMATION */}
      {loading && <LoadingAI />}

      {/* RESULTS LIST SECTION BELOW */}
      {garmentAnalysis && !loading && (
        <div id="ai-results-section" style={{ borderTop: '1px solid var(--border-color)', paddingTop: '32px' }}>
          
          {/* Garment Feature Breakdown */}
          <GarmentAnalysisCard garment={garmentAnalysis} onReset={() => {
            setGarmentFile(null);
            setGarmentPreview(null);
            setGarmentAnalysis(null);
            setRecommendations([]);
          }} />

          {/* Top 4 Recommendations Grid */}
          <div style={{ marginTop: '32px' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '24px' }}>
              <Trophy size={26} color="var(--accent-gold)" />
              <h2 style={{ fontSize: '1.7rem', color: '#FFF' }}>Top 4 Matching Embroidery Designs</h2>
            </div>

            <div className="recommendations-grid">
              {recommendations.map((rec, idx) => (
                <RecommendationCard
                  key={rec.design.id}
                  recommendation={rec}
                  rank={idx + 1}
                  sessionId={garmentAnalysis.upload_id}
                  onDelete={(deletedId) => {
                    setRecommendations(prev => prev.filter(item => item.design.id !== deletedId));
                    loadLibraryCount();
                  }}
                />
              ))}
            </div>
          </div>

        </div>
      )}

    </div>
  );
}
