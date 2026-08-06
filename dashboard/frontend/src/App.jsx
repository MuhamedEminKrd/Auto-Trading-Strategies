import { useState, useEffect, useRef, useMemo } from 'react';
import { useVirtualizer } from '@tanstack/react-virtual';
import {
  Download, LayoutDashboard, FileDown, Code,
  X, Loader2, ChevronDown, ChevronUp, Search
} from 'lucide-react';
import * as XLSX from 'xlsx';

const API_URL = 'http://localhost:8000/api';

const NUM_OPS = [
  { label: '>', value: 'gt' },
  { label: '>=', value: 'gte' },
  { label: '<', value: 'lt' },
  { label: '<=', value: 'lte' },
  { label: '=', value: 'eq' },
];

// Her sütun için sabit genişlik (px) — header ve satır aynı değeri kullanır
function getColWidth(key, isNumeric) {
  const k = key.toLowerCase();
  if (k.includes('strateji')) return 160;
  if (k.includes('hisse') || k.includes('unnamed: 0')) return 100;
  if (k.includes('akademik') || k.includes('geçerlilik')) return 200;
  if (isNumeric) return 130;
  return 140;
}

// ── Sayısal filtre satırı ──────────────────────────────────────────────
function NumericFilterRow({ filter, onChange, onRemove }) {
  return (
    <div className="filter-row">
      <select className="filter-op-select" value={filter.op}
        onChange={e => onChange({ ...filter, op: e.target.value })}>
        {NUM_OPS.map(op => <option key={op.value} value={op.value}>{op.label}</option>)}
      </select>
      <input className="filter-num-input" type="number" placeholder="değer"
        value={filter.val}
        onChange={e => onChange({ ...filter, val: e.target.value })} />
      <button className="filter-remove-btn" onClick={onRemove}>×</button>
    </div>
  );
}

// ── String checkbox filtresi ───────────────────────────────────────────
function StringFilterPanel({ uniqueValues, selectedValues, onChange }) {
  const [search, setSearch] = useState('');
  const filtered = uniqueValues.filter(v =>
    String(v).toLowerCase().includes(search.toLowerCase())
  );
  const toggle = val => {
    const s = new Set(selectedValues);
    s.has(val) ? s.delete(val) : s.add(val);
    onChange(s);
  };
  return (
    <div className="string-filter-panel">
      {uniqueValues.length > 6 && (
        <input className="filter-search-input" placeholder="Ara..."
          value={search} onChange={e => setSearch(e.target.value)} />
      )}
      <div className="string-filter-actions">
        <button className="filter-link-btn" onClick={() => onChange(new Set(uniqueValues))}>Tümü</button>
        <button className="filter-link-btn" onClick={() => onChange(new Set())}>Temizle</button>
      </div>
      <div className="string-filter-list">
        {filtered.map(val => (
          <label key={val} className="string-filter-item">
            <input type="checkbox" checked={selectedValues.has(val)} onChange={() => toggle(val)} />
            <span>{String(val)}</span>
          </label>
        ))}
        {filtered.length === 0 && <span className="no-results">Sonuç yok</span>}
      </div>
    </div>
  );
}

// ── Accordion filtre grubu ─────────────────────────────────────────────
function FilterAccordion({ colKey, colLabel, isNumeric, uniqueValues,
  numericFilters, stringSelected, onNumericChange, onStringChange }) {
  const [open, setOpen] = useState(false);

  const hasActive = isNumeric
    ? numericFilters.some(f => f.val !== '')
    : stringSelected.size < uniqueValues.length;

  return (
    <div className={`accordion ${hasActive ? 'accordion-active' : ''}`}>
      <button className="accordion-header" onClick={() => setOpen(o => !o)}>
        <span className="accordion-label">
          {hasActive && <span className="filter-dot" />}
          {colLabel}
        </span>
        {open ? <ChevronUp size={13} /> : <ChevronDown size={13} />}
      </button>
      {open && (
        <div className="accordion-body">
          {isNumeric ? (
            <>
              {numericFilters.map((f, i) => (
                <NumericFilterRow key={i} filter={f}
                  onChange={upd => { const n = [...numericFilters]; n[i] = upd; onNumericChange(n); }}
                  onRemove={() => onNumericChange(numericFilters.filter((_, idx) => idx !== i))} />
              ))}
              <button className="filter-add-btn"
                onClick={() => onNumericChange([...numericFilters, { op: 'gt', val: '' }])}>
                + Koşul Ekle
              </button>
            </>
          ) : (
            <StringFilterPanel
              uniqueValues={uniqueValues}
              selectedValues={stringSelected}
              onChange={onStringChange} />
          )}
        </div>
      )}
    </div>
  );
}

// ══════════════════════════════════════════════════════════════════════
// ANA BİLEŞEN
// ══════════════════════════════════════════════════════════════════════
export default function App() {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedRow, setSelectedRow] = useState(null);
  const [chartLoading, setChartLoading] = useState(false);
  const [chartHtml, setChartHtml] = useState(null);
  const [sorting, setSorting] = useState(null);
  const [numFilters, setNumFilters] = useState({});
  const [strFilters, setStrFilters] = useState({});
  const scrollRef = useRef(null);

  // Veri çek
  useEffect(() => {
    fetch(`${API_URL}/metrics`)
      .then(r => r.json())
      .then(d => { setData(d); setLoading(false); })
      .catch(() => setLoading(false));
  }, []);

  // Sütun meta
  const columnMeta = useMemo(() => {
    if (!data.length) return [];
    return Object.keys(data[0]).map(key => {
      let isNumeric = false;
      for (let i = 0; i < Math.min(data.length, 50); i++) {
        const v = data[i][key];
        if (v !== null && v !== undefined) { isNumeric = typeof v === 'number'; break; }
      }
      const uniqueValues = isNumeric
        ? []
        : [...new Set(data.map(r => r[key]).filter(v => v != null))].sort();
      const label = key.includes('Unnamed')
        ? (key.includes('0') ? 'Hisse' : 'Strateji')
        : key;
      return { key, isNumeric, uniqueValues, label, width: getColWidth(key, isNumeric) };
    });
  }, [data]);

  // String filtre başlangıç (tümü seçili)
  useEffect(() => {
    if (!columnMeta.length) return;
    const init = {};
    columnMeta.forEach(col => {
      if (!col.isNumeric && col.uniqueValues.length)
        init[col.key] = new Set(col.uniqueValues);
    });
    setStrFilters(init);
  }, [columnMeta]);

  // Grid template — her sütun için sabit px genişliği
  const gridTemplate = useMemo(
    () => columnMeta.map(c => `${c.width}px`).join(' '),
    [columnMeta]
  );

  // Filtreleme + sıralama
  const filteredData = useMemo(() => {
    let rows = data;

    // Sayısal filtreler
    for (const [key, filters] of Object.entries(numFilters)) {
      for (const { op, val } of filters) {
        if (val === '') continue;
        const num = parseFloat(val);
        if (isNaN(num)) continue;
        rows = rows.filter(row => {
          const v = row[key];
          if (v == null) return false;
          if (op === 'gt') return v > num;
          if (op === 'gte') return v >= num;
          if (op === 'lt') return v < num;
          if (op === 'lte') return v <= num;
          if (op === 'eq') return v === num;
          return true;
        });
      }
    }

    // String filtreler
    for (const [key, selected] of Object.entries(strFilters)) {
      if (!selected?.size) continue;
      const col = columnMeta.find(c => c.key === key);
      if (!col || selected.size === col.uniqueValues.length) continue;
      rows = rows.filter(row => selected.has(row[key]));
    }

    // Sıralama
    if (sorting) {
      rows = [...rows].sort((a, b) => {
        const av = a[sorting.key], bv = b[sorting.key];
        if (av == null) return 1;
        if (bv == null) return -1;
        const cmp = typeof av === 'number' ? av - bv : String(av).localeCompare(String(bv));
        return sorting.dir === 'asc' ? cmp : -cmp;
      });
    }

    return rows;
  }, [data, numFilters, strFilters, sorting, columnMeta]);

  // Virtual scroll — sadece tek bir dış scroll container
  const rowVirtualizer = useVirtualizer({
    count: filteredData.length,
    getScrollElement: () => scrollRef.current,
    estimateSize: () => 46,
    overscan: 15,
  });

  const handleRowClick = row => {
    setSelectedRow(row);
    setChartLoading(true);
    setChartHtml(null);
    const vals = Object.values(row);
    fetch(`${API_URL}/chart/html/${vals[0]}/${vals[1]}`)
      .then(r => r.text())
      .then(html => { setChartHtml(html); setChartLoading(false); })
      .catch(() => setChartLoading(false));
  };

  const exportExcel = () => {
    const ws = XLSX.utils.json_to_sheet(filteredData);
    const wb = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(wb, ws, 'Filtrelenmis');
    XLSX.writeFile(wb, `BIST_${new Date().toISOString().split('T')[0]}.xlsx`);
  };

  const downloadHtml = () => {
    if (!chartHtml || !selectedRow) return;
    const vals = Object.values(selectedRow);
    const blob = new Blob([chartHtml], { type: 'text/html' });
    const a = Object.assign(document.createElement('a'), {
      href: URL.createObjectURL(blob),
      download: `${vals[0]}_${vals[1]}.html`
    });
    a.click();
  };

  const downloadPng = () => {
    if (!selectedRow) return;
    const vals = Object.values(selectedRow);
    window.location.href = `${API_URL}/chart/png/${vals[0]}/${vals[1]}`;
  };

  const resetFilters = () => {
    setNumFilters({});
    const init = {};
    columnMeta.forEach(col => {
      if (!col.isNumeric && col.uniqueValues.length)
        init[col.key] = new Set(col.uniqueValues);
    });
    setStrFilters(init);
  };

  // ── Render ──────────────────────────────────────────────────────────
  return (
    <div className="app-container">

      {/* ── SIDEBAR ── */}
      <div className="glass-panel sidebar">
        <div className="sidebar-top">
          <h2><LayoutDashboard size={17} className="profit" /> BIST Dashboard</h2>
          <div className="mini-stat">
            <span className="mini-stat-label">Toplam</span>
            <span className="mini-stat-val">{data.length}</span>
          </div>
          <div className="mini-stat">
            <span className="mini-stat-label">Filtrelenen</span>
            <span className="mini-stat-val accent">{filteredData.length}</span>
          </div>
        </div>

        <div className="sidebar-filter-title">
          <Search size={12} />
          <span>Filtreler</span>
          <button className="filter-link-btn" onClick={resetFilters} style={{ marginLeft: 'auto' }}>
            Sıfırla
          </button>
        </div>

        <div className="filter-list">
          {columnMeta.map(col => (
            <FilterAccordion
              key={col.key}
              colKey={col.key}
              colLabel={col.label}
              isNumeric={col.isNumeric}
              uniqueValues={col.uniqueValues}
              numericFilters={numFilters[col.key] || []}
              stringSelected={strFilters[col.key] || new Set()}
              onNumericChange={v => setNumFilters(p => ({ ...p, [col.key]: v }))}
              onStringChange={v => setStrFilters(p => ({ ...p, [col.key]: v }))}
            />
          ))}
        </div>

        <div className="sidebar-bottom">
          <button className="btn primary" onClick={exportExcel}
            style={{ width: '100%', justifyContent: 'center' }}>
            <FileDown size={15} /> Excel İndir ({filteredData.length})
          </button>
        </div>
      </div>

      {/* ── TABLO ── */}
      <div className="main-content">
        <div className="glass-panel table-wrapper">
          {loading ? (
            <div className="loader-container">
              <div className="spinner" />
              <p>Veriler Yükleniyor...</p>
            </div>
          ) : (
            /* Tek scroll container — hem header hem body kaydırılır */
            <div className="scroll-container" ref={scrollRef}>
              {/* HEADER — sabit grid ile */}
              {columnMeta.length > 0 && (
                <div className="grid-header" style={{ gridTemplateColumns: gridTemplate }}>
                  {columnMeta.map(col => (
                    <div
                      key={col.key}
                      className={`grid-th ${col.isNumeric ? 'num' : ''}`}
                      style={{ width: col.width }}
                      onClick={() => setSorting(prev =>
                        prev?.key === col.key
                          ? prev.dir === 'asc' ? { key: col.key, dir: 'desc' } : null
                          : { key: col.key, dir: 'asc' }
                      )}
                    >
                      {col.label}
                      {sorting?.key === col.key ? (sorting.dir === 'asc' ? ' ▲' : ' ▼') : ''}
                    </div>
                  ))}
                </div>
              )}

              {/* BODY — virtual scroll */}
              <div
                className="virtual-body"
                style={{ height: `${rowVirtualizer.getTotalSize()}px` }}
              >
                {rowVirtualizer.getVirtualItems().map(vRow => {
                  const row = filteredData[vRow.index];
                  const isSelected = selectedRow === row;
                  return (
                    <div
                      key={vRow.index}
                      className={`grid-row ${isSelected ? 'selected' : ''}`}
                      style={{
                        gridTemplateColumns: gridTemplate,
                        position: 'absolute',
                        top: 0,
                        transform: `translateY(${vRow.start}px)`,
                        height: `${vRow.size}px`,
                        width: '100%',
                      }}
                      onClick={() => handleRowClick(row)}
                    >
                      {columnMeta.map(col => {
                        const val = row[col.key];
                        let display = val == null ? '—' : val;
                        let cls = '';
                        if (col.isNumeric && typeof val === 'number') {
                          display = val.toFixed(2);
                          const isReturn = col.key.toLowerCase().includes('kâr') ||
                            col.key.toLowerCase().includes('return') ||
                            col.key.toLowerCase().includes('getiri') ||
                            col.key.toLowerCase().includes('alfa');
                          if (isReturn) cls = val > 0 ? 'profit' : val < 0 ? 'loss' : '';
                        }
                        return (
                          <div
                            key={col.key}
                            className={`grid-td ${col.isNumeric ? 'num' : ''}`}
                            style={{ width: col.width }}
                          >
                            <span className={cls}>{display}</span>
                          </div>
                        );
                      })}
                    </div>
                  );
                })}
              </div>
            </div>
          )}
        </div>
      </div>

      {/* ── GRAFİK PANELİ ── */}
      {(selectedRow || chartLoading) && (
        <div className="glass-panel chart-panel">
          <div className="chart-header">
            <h3>
              {selectedRow
                ? `${Object.values(selectedRow)[0]} × ${Object.values(selectedRow)[1]}`
                : 'Yükleniyor...'}
            </h3>
            <div className="chart-actions">
              <button className="btn" onClick={downloadHtml} disabled={!chartHtml}>
                <Code size={14} /> HTML
              </button>
              <button className="btn" onClick={downloadPng} disabled={!chartHtml}>
                <Download size={14} /> PNG
              </button>
              <button className="btn icon-btn"
                onClick={() => { setSelectedRow(null); setChartHtml(null); }}>
                <X size={15} />
              </button>
            </div>
          </div>

          <div className="chart-content">
            {chartLoading && (
              <div className="loader-container">
                <Loader2 size={30} className="profit" style={{ animation: 'spin 1.5s linear infinite' }} />
                <p style={{ color: 'var(--text-secondary)', fontSize: '0.88rem' }}>
                  VectorBT grafiği oluşturuluyor...
                </p>
              </div>
            )}
            {chartHtml && !chartLoading && (
              <iframe srcDoc={chartHtml} className="chart-frame" title="Plotly Chart" />
            )}
          </div>
        </div>
      )}
    </div>
  );
}
