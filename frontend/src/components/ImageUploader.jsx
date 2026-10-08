import React, { useState } from 'react';
import { UploadCloud, FileText, Sparkles, CheckCircle2 } from 'lucide-react';

export default function ImageUploader({ onUpload, isLoading }) {
  const [selectedFile, setSelectedFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [isPdf, setIsPdf] = useState(false);
  const [garmentType, setGarmentType] = useState('blouse');
  const [isDragging, setIsDragging] = useState(false);

  const handleFileChange = (file) => {
    if (!file) return;
    setSelectedFile(file);
    const fileIsPdf = file.type === 'application/pdf' || file.name.toLowerCase().endsWith('.pdf');
    setIsPdf(fileIsPdf);

    if (fileIsPdf) {
      setPreviewUrl(null);
    } else {
      setPreviewUrl(URL.createObjectURL(file));
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragging(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFileChange(e.dataTransfer.files[0]);
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!selectedFile) return;
    onUpload(selectedFile, garmentType);
  };

  return (
    <div className="glass-panel" style={{ padding: '32px', textAlign: 'center', maxWidth: '640px', margin: '0 auto' }}>
      <div style={{ marginBottom: '24px' }}>
        <h2 style={{ fontSize: '1.6rem', color: '#FFF', marginBottom: '8px' }}>
          Upload Blouse/Saree Photo or PDF Catalog
        </h2>
        <p style={{ color: 'var(--text-secondary)', fontSize: '0.92rem' }}>
          AI extracts dominant colors, fabric texture, and style from images & PDF pages to find your top 4 embroidery matches.
        </p>
      </div>

      {/* Garment Type Selector */}
      <div style={{ display: 'inline-flex', background: 'var(--bg-deep)', padding: '4px', borderRadius: '10px', marginBottom: '24px', border: '1px solid var(--border-color)' }}>
        <button
          type="button"
          onClick={() => setGarmentType('blouse')}
          style={{
            padding: '8px 24px',
            borderRadius: '8px',
            border: 'none',
            background: garmentType === 'blouse' ? 'var(--accent-gold)' : 'transparent',
            color: garmentType === 'blouse' ? '#000' : 'var(--text-secondary)',
            fontWeight: 600,
            cursor: 'pointer',
            transition: 'all 0.2s ease'
          }}
        >
          Blouse
        </button>
        <button
          type="button"
          onClick={() => setGarmentType('saree')}
          style={{
            padding: '8px 24px',
            borderRadius: '8px',
            border: 'none',
            background: garmentType === 'saree' ? 'var(--accent-gold)' : 'transparent',
            color: garmentType === 'saree' ? '#000' : 'var(--text-secondary)',
            fontWeight: 600,
            cursor: 'pointer',
            transition: 'all 0.2s ease'
          }}
        >
          Saree
        </button>
      </div>

      {/* Dropzone */}
      <div
        onDragOver={(e) => { e.preventDefault(); setIsDragging(true); }}
        onDragLeave={() => setIsDragging(false)}
        onDrop={handleDrop}
        style={{
          border: isDragging ? '2px dashed var(--accent-gold)' : '2px dashed var(--border-color)',
          borderRadius: 'var(--radius-md)',
          padding: '36px 20px',
          background: isDragging ? 'rgba(212, 175, 55, 0.08)' : 'rgba(11, 14, 20, 0.4)',
          cursor: 'pointer',
          transition: 'all 0.2s ease',
          marginBottom: '24px',
          position: 'relative'
        }}
        onClick={() => document.getElementById('garment-file-input').click()}
      >
        <input
          id="garment-file-input"
          type="file"
          accept="image/*,application/pdf,.pdf"
          style={{ display: 'none' }}
          onChange={(e) => handleFileChange(e.target.files[0])}
        />

        {isPdf ? (
          <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '12px' }}>
            <div style={{
              width: '64px',
              height: '64px',
              borderRadius: '16px',
              background: 'rgba(239, 68, 68, 0.15)',
              border: '1px solid rgba(239, 68, 68, 0.3)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center'
            }}>
              <FileText size={32} color="#EF4444" />
            </div>
            <div>
              <p style={{ color: '#FFF', fontWeight: 700, fontSize: '1.05rem' }}>
                {selectedFile.name}
              </p>
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '6px', color: 'var(--accent-gold-light)', fontSize: '0.88rem', marginTop: '6px' }}>
                <CheckCircle2 size={16} color="var(--accent-gold)" /> PDF Ready for AI Page Rendering & Analysis
              </div>
            </div>
          </div>
        ) : previewUrl ? (
          <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '12px' }}>
            <img
              src={previewUrl}
              alt="Selected Garment Preview"
              style={{
                maxHeight: '220px',
                maxWidth: '100%',
                borderRadius: '12px',
                objectFit: 'cover',
                boxShadow: '0 8px 20px rgba(0,0,0,0.5)',
                border: '2px solid var(--accent-gold)'
              }}
            />
            <div style={{ display: 'flex', alignItems: 'center', gap: '6px', color: 'var(--accent-gold-light)', fontSize: '0.88rem' }}>
              <CheckCircle2 size={16} color="var(--accent-gold)" /> Ready for AI Analysis
            </div>
          </div>
        ) : (
          <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '12px' }}>
            <div style={{
              width: '56px',
              height: '56px',
              borderRadius: '50%',
              background: 'rgba(212, 175, 55, 0.1)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center'
            }}>
              <UploadCloud size={28} color="var(--accent-gold)" />
            </div>
            <div>
              <p style={{ color: '#FFF', fontWeight: 600, fontSize: '1rem' }}>
                Drag & drop garment image or PDF catalog here
              </p>
              <p style={{ color: 'var(--text-muted)', fontSize: '0.82rem', marginTop: '4px' }}>
                Supports JPG, PNG, WEBP, and PDF documents
              </p>
            </div>
          </div>
        )}
      </div>

      <button
        onClick={handleSubmit}
        disabled={!selectedFile || isLoading}
        className="btn-gold"
        style={{ width: '100%', padding: '14px', fontSize: '1rem', opacity: !selectedFile || isLoading ? 0.6 : 1 }}
      >
        <Sparkles size={20} />
        {isLoading ? 'Processing File & Running AI Engine...' : 'Find Matching Embroidery Designs'}
      </button>
    </div>
  );
}
