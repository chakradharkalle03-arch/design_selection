import React, { useState, useEffect } from 'react';
import DesignCard from '../components/DesignCard';
import { fetchDesigns, uploadDesign, deleteDesign, deleteAllDesigns } from '../services/api';
import { Plus, Grid, Trash2, FolderPlus, FilePlus, X } from 'lucide-react';

export default function DesignLibrary() {
  const [designs, setDesigns] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [showModal, setShowModal] = useState(false);

  // Form states
  const [uploadFiles, setUploadFiles] = useState([]);
  const [isFolder, setIsFolder] = useState(false);
  const [name, setName] = useState('');
  const [designCode, setDesignCode] = useState('');
  const [category, setCategory] = useState('Traditional');
  const [style, setStyle] = useState('Floral');
  const [placement, setPlacement] = useState('Full Blouse');
  const [description, setDescription] = useState('');
  const [isUploading, setIsUploading] = useState(false);
  const [uploadStatus, setUploadStatus] = useState('');

  const categories = ['all', 'Bridal', 'Traditional', 'Temple', 'Floral', 'Peacock', 'Minimal'];

  const loadCatalog = async () => {
    setLoading(true);
    try {
      const data = await fetchDesigns(selectedCategory);
      setDesigns(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadCatalog();
  }, [selectedCategory]);

  const handleDelete = async (id) => {
    if (!window.confirm('Are you sure you want to delete this design pattern?')) return;
    try {
      await deleteDesign(id);
      setDesigns(designs.filter(d => d.id !== id));
    } catch (err) {
      console.error(err);
    }
  };

  const handleDeleteAll = async () => {
    if (!window.confirm(`⚠️ DANGER: Are you sure you want to PERMANENTLY DELETE ALL ${designs.length} embroidery designs from your shop library? This action cannot be undone.`)) {
      return;
    }
    setLoading(true);
    try {
      await deleteAllDesigns();
      setDesigns([]);
      alert('All embroidery designs have been permanently deleted.');
    } catch (err) {
      console.error(err);
      alert('Failed to delete all designs. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleFilesSelection = (e, folderMode = false) => {
    const files = Array.from(e.target.files || []);
    if (files.length === 0) return;
    setUploadFiles(files);
    setIsFolder(folderMode);
    if (files.length === 1 && !name) {
      setName(files[0].name.replace(/\.[^/.]+$/, ""));
    } else if (files.length > 1) {
      setName(`Batch Catalog Upload (${files.length} items)`);
    }
  };

  const handleFormSubmit = async (e) => {
    e.preventDefault();
    if (uploadFiles.length === 0) return;

    setIsUploading(true);
    setUploadStatus(`Processing ${uploadFiles.length} design file(s)...`);

    try {
      let totalExtracted = 0;
      for (let i = 0; i < uploadFiles.length; i++) {
        const file = uploadFiles[i];
        const formData = new FormData();
        formData.append('file', file);
        formData.append('name', uploadFiles.length === 1 ? (name || file.name) : file.name.replace(/\.[^/.]+$/, ""));
        if (designCode && uploadFiles.length === 1) formData.append('design_code', designCode);
        formData.append('category', category);
        formData.append('style', style);
        formData.append('placement', placement);
        formData.append('description', description);

        const res = await uploadDesign(formData);
        if (res.processed_pages) {
          totalExtracted += res.processed_pages;
        } else {
          totalExtracted += 1;
        }
      }

      setUploadStatus(`✅ Successfully added ${totalExtracted} design pattern(s) to AI library!`);
      setTimeout(() => {
        setShowModal(false);
        setUploadFiles([]);
        setName('');
        setDesignCode('');
        setUploadStatus('');
        loadCatalog();
      }, 1000);

    } catch (err) {
      console.error(err);
      alert('Failed to upload designs. Please try again.');
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div style={{ maxWidth: '1280px', margin: '0 auto', padding: '32px 24px' }}>
      
      {/* Header & Actions */}
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '24px', flexWrap: 'wrap', gap: '16px' }}>
        <div>
          <h1 style={{ fontSize: '1.8rem', color: '#FFF' }}>Shop Embroidery Design Library ({designs.length} Items)</h1>
          <p style={{ color: 'var(--text-secondary)', fontSize: '0.92rem' }}>
            Store and manage pre-computed AI embeddings for instant customer matching.
          </p>
        </div>
        
        <div style={{ display: 'flex', gap: '12px' }}>
          {/* Delete All Button */}
          {designs.length > 0 && (
            <button
              onClick={handleDeleteAll}
              style={{
                background: 'rgba(239, 68, 68, 0.2)',
                border: '1px solid #EF4444',
                color: '#EF4444',
                fontWeight: 600,
                padding: '10px 18px',
                borderRadius: 'var(--radius-sm)',
                cursor: 'pointer',
                display: 'inline-flex',
                alignItems: 'center',
                gap: '8px'
              }}
            >
              <Trash2 size={18} /> Delete All Designs ({designs.length})
            </button>
          )}

          <button onClick={() => setShowModal(true)} className="btn-gold">
            <Plus size={18} /> Add / Batch Upload Designs
          </button>
        </div>
      </div>

      {/* Category Filter Tabs */}
      <div style={{ display: 'flex', gap: '10px', overflowX: 'auto', paddingBottom: '12px', marginBottom: '24px' }}>
        {categories.map((cat) => (
          <button
            key={cat}
            onClick={() => setSelectedCategory(cat)}
            style={{
              padding: '8px 18px',
              borderRadius: 'var(--radius-full)',
              border: selectedCategory === cat ? '1px solid var(--accent-gold)' : '1px solid var(--border-color)',
              background: selectedCategory === cat ? 'rgba(212, 175, 55, 0.15)' : 'var(--bg-card)',
              color: selectedCategory === cat ? 'var(--accent-gold-light)' : 'var(--text-secondary)',
              fontWeight: 600,
              fontSize: '0.88rem',
              cursor: 'pointer',
              textTransform: 'capitalize',
              whiteSpace: 'nowrap'
            }}
          >
            {cat}
          </button>
        ))}
      </div>

      {/* Grid */}
      {loading ? (
        <div style={{ textAlign: 'center', padding: '60px', color: 'var(--accent-gold)' }}>
          Loading design catalog...
        </div>
      ) : designs.length === 0 ? (
        <div className="glass-panel" style={{ padding: '48px', textAlign: 'center', color: 'var(--text-secondary)' }}>
          No embroidery designs in library. Click "Add / Batch Upload Designs" to upload design files or an entire catalog folder.
        </div>
      ) : (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(240px, 1fr))', gap: '20px' }}>
          {designs.map((design) => (
            <DesignCard key={design.id} design={design} onDelete={handleDelete} />
          ))}
        </div>
      )}

      {/* Admin Upload Modal (Supports Single/Multiple Files & Folder Upload) */}
      {showModal && (
        <div style={{
          position: 'fixed',
          inset: 0,
          background: 'rgba(0,0,0,0.85)',
          backdropFilter: 'blur(8px)',
          zIndex: 200,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          padding: '20px'
        }}>
          <div className="glass-panel" style={{ width: '100%', maxWidth: '580px', padding: '32px', position: 'relative' }}>
            <button
              onClick={() => setShowModal(false)}
              style={{ position: 'absolute', top: '16px', right: '16px', background: 'none', border: 'none', color: '#FFF', cursor: 'pointer' }}
            >
              <X size={20} />
            </button>

            <h3 style={{ fontSize: '1.4rem', color: '#FFF', marginBottom: '8px' }}>Upload Embroidery Patterns / Folder</h3>
            <p style={{ color: 'var(--text-secondary)', fontSize: '0.85rem', marginBottom: '20px' }}>
              Select single files, multiple pattern files, multi-page PDFs, or an entire directory folder.
            </p>

            <form onSubmit={handleFormSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
              
              {/* Dual Upload Options: Files vs Folder */}
              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '12px' }}>
                <button
                  type="button"
                  onClick={() => document.getElementById('files-picker-input').click()}
                  className="btn-secondary"
                  style={{ padding: '14px', justifyContent: 'center', flexDirection: 'column', gap: '6px' }}
                >
                  <FilePlus size={24} color="var(--accent-gold)" />
                  <span style={{ fontWeight: 600, fontSize: '0.9rem' }}>Select File(s) / PDFs</span>
                  <span style={{ fontSize: '0.72rem', color: 'var(--text-muted)' }}>Single or multiple files</span>
                </button>

                <button
                  type="button"
                  onClick={() => document.getElementById('folder-picker-input').click()}
                  className="btn-secondary"
                  style={{ padding: '14px', justifyContent: 'center', flexDirection: 'column', gap: '6px' }}
                >
                  <FolderPlus size={24} color="var(--accent-gold)" />
                  <span style={{ fontWeight: 600, fontSize: '0.9rem' }}>Select Entire Folder</span>
                  <span style={{ fontSize: '0.72rem', color: 'var(--text-muted)' }}>Upload folder directory</span>
                </button>
              </div>

              {/* Hidden Inputs */}
              <input
                id="files-picker-input"
                type="file"
                multiple
                accept="image/*,application/pdf,.pdf"
                style={{ display: 'none' }}
                onChange={(e) => handleFilesSelection(e, false)}
              />

              <input
                id="folder-picker-input"
                type="file"
                webkitdirectory=""
                directory=""
                mozdirectory=""
                multiple
                style={{ display: 'none' }}
                onChange={(e) => handleFilesSelection(e, true)}
              />

              {uploadFiles.length > 0 && (
                <div style={{ background: 'rgba(212, 175, 55, 0.12)', border: '1px solid var(--accent-gold)', padding: '10px 14px', borderRadius: '6px', fontSize: '0.88rem', color: 'var(--accent-gold-light)' }}>
                  📁 Selected: <b>{uploadFiles.length} file(s)</b> {isFolder ? '(Folder mode)' : ''}
                </div>
              )}

              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '12px' }}>
                <div>
                  <label style={{ display: 'block', fontSize: '0.85rem', color: 'var(--text-secondary)', marginBottom: '4px' }}>Design Name</label>
                  <input
                    type="text"
                    placeholder="e.g. Royal Peacock Neckline"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    style={{ width: '100%', background: 'var(--bg-deep)', color: '#FFF', padding: '8px 12px', borderRadius: '6px', border: '1px solid var(--border-color)' }}
                  />
                </div>
                <div>
                  <label style={{ display: 'block', fontSize: '0.85rem', color: 'var(--text-secondary)', marginBottom: '4px' }}>Design Code (Optional)</label>
                  <input
                    type="text"
                    placeholder="e.g. EMB-0099"
                    value={designCode}
                    onChange={(e) => setDesignCode(e.target.value)}
                    style={{ width: '100%', background: 'var(--bg-deep)', color: '#FFF', padding: '8px 12px', borderRadius: '6px', border: '1px solid var(--border-color)' }}
                  />
                </div>
              </div>

              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: '12px' }}>
                <div>
                  <label style={{ display: 'block', fontSize: '0.85rem', color: 'var(--text-secondary)', marginBottom: '4px' }}>Category</label>
                  <select
                    value={category}
                    onChange={(e) => setCategory(e.target.value)}
                    style={{ width: '100%', background: 'var(--bg-deep)', color: '#FFF', padding: '8px', borderRadius: '6px', border: '1px solid var(--border-color)' }}
                  >
                    <option value="Bridal">Bridal</option>
                    <option value="Traditional">Traditional</option>
                    <option value="Temple">Temple</option>
                    <option value="Floral">Floral</option>
                    <option value="Peacock">Peacock</option>
                    <option value="Minimal">Minimal</option>
                  </select>
                </div>
                <div>
                  <label style={{ display: 'block', fontSize: '0.85rem', color: 'var(--text-secondary)', marginBottom: '4px' }}>Style</label>
                  <select
                    value={style}
                    onChange={(e) => setStyle(e.target.value)}
                    style={{ width: '100%', background: 'var(--bg-deep)', color: '#FFF', padding: '8px', borderRadius: '6px', border: '1px solid var(--border-color)' }}
                  >
                    <option value="Heavy Zari">Heavy Zari</option>
                    <option value="Floral">Floral</option>
                    <option value="Peacock">Peacock</option>
                    <option value="Minimalistic">Minimalistic</option>
                    <option value="Kundan">Kundan</option>
                  </select>
                </div>
                <div>
                  <label style={{ display: 'block', fontSize: '0.85rem', color: 'var(--text-secondary)', marginBottom: '4px' }}>Placement</label>
                  <select
                    value={placement}
                    onChange={(e) => setPlacement(e.target.value)}
                    style={{ width: '100%', background: 'var(--bg-deep)', color: '#FFF', padding: '8px', borderRadius: '6px', border: '1px solid var(--border-color)' }}
                  >
                    <option value="Full Blouse">Full Blouse</option>
                    <option value="Neck">Neck</option>
                    <option value="Back">Back</option>
                    <option value="Sleeve">Sleeve</option>
                    <option value="Border">Border</option>
                  </select>
                </div>
              </div>

              {uploadStatus && (
                <div style={{ color: 'var(--accent-gold-light)', fontSize: '0.85rem', fontWeight: 600, textAlign: 'center' }}>
                  {uploadStatus}
                </div>
              )}

              <button type="submit" disabled={isUploading || uploadFiles.length === 0} className="btn-gold" style={{ width: '100%', marginTop: '8px', opacity: isUploading || uploadFiles.length === 0 ? 0.6 : 1 }}>
                {isUploading ? 'Precomputing AI Embeddings...' : `Process & Save ${uploadFiles.length || ''} File(s)`}
              </button>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
