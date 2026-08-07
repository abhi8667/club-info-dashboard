'use client'

import { useEffect, useMemo, useState } from 'react'
import { ArrowUpRight, AtSign, ChevronLeft, ChevronRight, Mail, Search, Shuffle, X } from 'lucide-react'
import { clubs, type Club, type ClubCategory } from '@/data/clubs'

const categories: (ClubCategory | 'All')[] = ['All', 'Technical', 'Non-Technical']

function ClubMark({ club, large = false }: { club: Club; large?: boolean }) {
  return (
    <div
      aria-hidden="true"
      className={`club-mark ${large ? 'club-mark-large' : ''}`}
      style={{ '--club-color': club.color, '--club-accent': club.accent } as React.CSSProperties}
    >
      {club.logo ? (
        <img 
          src={club.logo} 
          alt={`${club.shortName} logo`} 
          style={{ width: '100%', height: '100%', objectFit: 'contain' }} 
        />
      ) : (
        <span>{club.symbol}</span>
      )}
    </div>
  )
}

function ClubCard({ club, onOpen }: { club: Club; onOpen: (club: Club) => void }) {
  return (
    <button className="club-card" onClick={() => onOpen(club)} type="button" aria-label={`View ${club.name}`}>
      <div className="club-card-top">
        <ClubMark club={club} />
        <ArrowUpRight className="club-arrow" aria-hidden="true" />
      </div>
      <div className="club-card-copy">
        <span className="club-card-category">{club.division}</span>
        <h3>{club.name}</h3>
        <p>{club.description}</p>
      </div>
      <div className="club-card-footer">
        <span>{club.shortName}</span>
        <span>{club.venue}</span>
      </div>
    </button>
  )
}

function DetailDialog({ club, onClose }: { club: Club | null; onClose: () => void }) {
  const [eventIndex, setEventIndex] = useState(0)

  useEffect(() => {
    setEventIndex(0)
  }, [club])

  useEffect(() => {
    if (!club) return
    const handleKey = (event: KeyboardEvent) => {
      if (event.key === 'Escape') onClose()
    }
    document.addEventListener('keydown', handleKey)
    document.body.style.overflow = 'hidden'
    return () => {
      document.removeEventListener('keydown', handleKey)
      document.body.style.overflow = ''
    }
  }, [club, onClose])

  if (!club) return null
  const event = club.events[eventIndex]

  return (
    <div className="dialog-backdrop" role="presentation" onMouseDown={(event) => event.target === event.currentTarget && onClose()}>
      <section className="club-dialog" role="dialog" aria-modal="true" aria-labelledby="club-dialog-title">
        <button className="dialog-close" onClick={onClose} type="button" aria-label="Close club details">
          <X size={20} />
        </button>
        <div className="dialog-hero">
          <ClubMark club={club} large />
          <span className="dialog-index">{String(clubs.findIndex((item) => item.id === club.id) + 1).padStart(2, '0')} / {clubs.length}</span>
        </div>
        <div className="dialog-body">
          <span className="eyebrow">{club.division}</span>
          <h2 id="club-dialog-title">{club.name}</h2>
          {club.description && <p className="dialog-description">{club.description}</p>}

          {club.images && club.images.length > 0 && (
            <div className="dialog-section gallery-section">
              <div className="dialog-section-heading"><span>Club life</span></div>
              <div className="gallery-grid" style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem', marginTop: '1rem', marginBottom: '2rem' }}>
                {club.images.map((img, i) => (
                  <img key={i} src={img} alt={`${club.name} life`} style={{ width: '100%', borderRadius: '0.5rem', objectFit: 'cover', aspectRatio: '16/9' }} />
                ))}
              </div>
            </div>
          )}

          {club.events.length > 0 && event && <div className="dialog-section">
            <div className="dialog-section-heading"><span>Upcoming events</span><span>{eventIndex + 1} / {club.events.length}</span></div>
            <div className="event-row">
              <div className="event-date">
                {event.date}
                {event.time && <div style={{ fontSize: '0.8em', opacity: 0.8, marginTop: '4px' }}>{event.time}</div>}
              </div>
              <div>
                <strong>{event.name}</strong>
                {event.venue && <div style={{ fontSize: '0.85em', color: 'var(--brand-muted)', marginBottom: '4px' }}>📍 {event.venue}</div>}
                <p>{event.detail}</p>
              </div>
            </div>
            <div className="event-controls">
              <button type="button" onClick={() => setEventIndex((eventIndex - 1 + club.events.length) % club.events.length)} aria-label="Previous event"><ChevronLeft size={18} /></button>
              <button type="button" onClick={() => setEventIndex((eventIndex + 1) % club.events.length)} aria-label="Next event"><ChevronRight size={18} /></button>
            </div>
          </div>}

          {(club.email || club.instagram) && <div className="dialog-section contact-section">
            <div className="dialog-section-heading"><span>Find the club</span><span>Lead · {club.lead}</span></div>
            <div className="contact-links">
              {club.email && <a href={`mailto:${club.email}`}><Mail size={16} />Email club</a>}
              {club.instagram && <a href={`https://instagram.com/${club.instagram.slice(1)}`} target="_blank" rel="noreferrer"><AtSign size={16} />{club.instagram}</a>}
            </div>
          </div>}
        </div>
      </section>
    </div>
  )
}

export function ClubShowcase() {
  const [category, setCategory] = useState<(typeof categories)[number]>('All')
  const [division, setDivision] = useState<string>('All')
  const [query, setQuery] = useState('')
  const [visible, setVisible] = useState(false)
  const [selectedClub, setSelectedClub] = useState<Club | null>(null)
  const [order, setOrder] = useState(() => clubs.map((_, index) => index).sort(() => Math.random() - 0.5))

  const availableDivisions = useMemo(() => {
    if (category === 'All') return []
    const divs = Array.from(new Set(clubs.filter(c => c.category === category).map(c => c.division)))
    return divs.sort()
  }, [category])

  const filteredClubs = useMemo(() => {
    const normalizedQuery = query.trim().toLowerCase()
    return order.map((index) => clubs[index]).filter((club) => {
      const matchesCategory = category === 'All' || club.category === category
      const matchesDivision = division === 'All' || club.division === division
      const matchesQuery = !normalizedQuery || `${club.name} ${club.shortName}`.toLowerCase().includes(normalizedQuery)
      return matchesCategory && matchesDivision && matchesQuery
    })
  }, [category, division, order, query])

  const openClubs = (nextCategory: ClubCategory | 'All') => {
    setCategory(nextCategory)
    setDivision('All')
    setVisible(true)
    window.setTimeout(() => document.getElementById('club-grid')?.scrollIntoView({ behavior: 'smooth', block: 'start' }), 20)
  }

  const shuffle = () => setOrder((current) => [...current].sort(() => Math.random() - 0.5))

  return (
    <main>
      <header className="site-header">
        <a className="wordmark" href="#top" aria-label="The clubs of RVCE home"><span>RVCE</span><i>Clubs</i></a>
        <nav className="main-nav" aria-label="Main navigation">
          <a href="#clubs">Clubs <span>{clubs.length}</span></a>
          <a href="#about">Events <span>Soon</span></a>
          <a href="#about">About</a>
          <a href="#clubs">Wall</a>
        </nav>
        <button className="header-action" onClick={() => openClubs('All')} type="button" aria-label="Open club wall"><Search size={17} /><span>Explore clubs</span><ArrowUpRight size={16} /></button>
      </header>

      <section className="hero" id="top">
        <div className="hero-copy">
          <p className="eyebrow hero-eyebrow">RV College of Engineering · Bengaluru</p>
          <h1>A collection of iconic<br /><em>campus clubs.</em></h1>
          <p className="hero-description">A living directory of the people, practices, and communities that make campus feel like more than a campus.</p>
          <div className="hero-signup">
            <span className="hero-input">Search the club wall</span>
            <button className="primary-action" type="button" onClick={() => openClubs('All')}>Browse clubs <ArrowUpRight size={17} /></button>
          </div>
          <div className="hero-actions">
            <button className="text-action" type="button" onClick={() => openClubs('Technical')}>Technical <span>{clubs.filter((club) => club.category === 'Technical').length}</span></button>
            <button className="text-action" type="button" onClick={() => openClubs('Non-Technical')}>Non-technical <span>{clubs.filter((club) => club.category === 'Non-Technical').length}</span></button>
          </div>
        </div>
        <div className="hero-subscribe" aria-label="Club directory introduction">
          <span>{clubs.length} communities · one campus</span>
          <button className="hero-scroll" type="button" onClick={() => openClubs('All')}>Browse the wall <ArrowUpRight size={15} /></button>
        </div>
      </section>

      <section className={`directory ${visible ? 'directory-visible' : ''}`} id="clubs">
        <div className="directory-heading" id="club-grid">
          <div><p className="eyebrow">The directory</p><h2>Find your people.</h2></div>
          <p className="directory-intro">Browse the student-led communities shaping life at RVCE, one curious idea at a time.</p>
        </div>
        <div className="directory-toolbar">
          <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
            <div className="category-tabs" role="tablist" aria-label="Filter clubs by category">
              {categories.map((item) => <button key={item} className={category === item ? 'active' : ''} onClick={() => { setCategory(item); setDivision('All'); setVisible(true) }} type="button" role="tab" aria-selected={category === item}>{item}</button>)}
            </div>
            {availableDivisions.length > 0 && (
              <div className="division-tabs" role="tablist" aria-label="Filter clubs by division">
                <button className={division === 'All' ? 'active' : ''} onClick={() => setDivision('All')} type="button" role="tab" aria-selected={division === 'All'}>All Divisions</button>
                {availableDivisions.map(div => (
                  <button key={div} className={division === div ? 'active' : ''} onClick={() => setDivision(div)} type="button" role="tab" aria-selected={division === div}>{div}</button>
                ))}
              </div>
            )}
          </div>
          <div className="toolbar-actions">
            <label className="search-field"><Search size={16} /><span className="sr-only">Search clubs</span><input value={query} onChange={(event) => setQuery(event.target.value)} placeholder="Search clubs" /></label>
            <button className="shuffle-action" type="button" onClick={shuffle}><Shuffle size={15} /> Shuffle</button>
          </div>
        </div>
        <div className="club-count">Showing {filteredClubs.length} of {clubs.length} clubs</div>
        {filteredClubs.length ? <div className="club-wall">{Array.from({ length: Math.ceil(filteredClubs.length / 3) }, (_, row) => <div className="club-shelf" key={`shelf-${row}`}>{filteredClubs.slice(row * 3, row * 3 + 3).map((club) => <ClubCard key={club.id} club={club} onOpen={setSelectedClub} />)}</div>)}</div> : <div className="empty-state">No clubs found. Try a different search.</div>}
      </section>

      <footer className="site-footer" id="about"><div><span className="wordmark"><span>RVCE</span><i>Clubs</i></span><p>Built by students, for students.</p></div><span>© {new Date().getFullYear()} · Bengaluru, India</span></footer>
      <DetailDialog club={selectedClub} onClose={() => setSelectedClub(null)} />
    </main>
  )
}
