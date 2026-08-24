'use client'

import React, { useEffect, useMemo, useState } from 'react'
import { ArrowLeft, ArrowUp, ArrowUpRight, AtSign, ChevronLeft, ChevronRight, Search, Shuffle, X } from 'lucide-react'
import { clubs, type Club, type ClubCategory } from '@/data/clubs'

const categories: (ClubCategory | 'All')[] = ['All', 'Technical', 'Non-Technical']

export interface DivisionMeta {
  name: string
  shortName: string
  category: 'Technical' | 'Non-Technical'
  color: string
  accent: string
  symbol: string
  icon?: string
  description: string
}

export const DIVISION_META: { [key: string]: DivisionMeta } = {
  'Racing & Automotive': {
    name: 'Racing & Automotive',
    shortName: 'FSAE & BAJA Motorsport',
    category: 'Technical',
    color: '#fee2e2',
    accent: '#991b1b',
    symbol: '🏎️',
    icon: '/divisions/Racing and Automotive.png',
    description: 'Formula Student, Hybrid prototypes, and BAJA ATV motorsport teams driving global innovation.',
  },
  'Computer Science, Software & AI': {
    name: 'Computer Science, Software & AI',
    shortName: 'CS, AI & Cloud',
    category: 'Technical',
    color: '#dbeafe',
    accent: '#1e40af',
    symbol: '💻',
    icon: '/divisions/CS and AI.png',
    description: 'Competitive coding, open-source engineering, AI models, cloud computing & developer guilds.',
  },
  'Space, Drone & Aerospace': {
    name: 'Space, Drone & Aerospace',
    shortName: 'Aerospace & Satellites',
    category: 'Technical',
    color: '#e0f2fe',
    accent: '#075985',
    symbol: '🚀',
    icon: '/divisions/Space and Drone.png',
    description: 'Rocketry prototypes, autonomous drone swarms, and CubeSat satellite mission design.',
  },
  'Robotics, Electronics & Core Tech': {
    name: 'Robotics, Electronics & Core Tech',
    shortName: 'Robotics & Hardware',
    category: 'Technical',
    color: '#f3e8ff',
    accent: '#6b21a8',
    symbol: '🤖',
    icon: '/divisions/Robotics and core tech.png',
    description: 'Autonomous robotics, embedded hardware, HAM radio, quantum physics & IEEE chapters.',
  },
  'Astronomy': {
    name: 'Astronomy',
    shortName: 'Astronomy & Stargazing',
    category: 'Technical',
    color: '#fef3c7',
    accent: '#92400e',
    symbol: '🔭',
    icon: '/divisions/Astronomy.png',
    description: 'Stargazing expeditions, space science research & celestial observational projects.',
  },
  'Industry Connect and Interdisciplinary Engineering': {
    name: 'Industry Connect and Interdisciplinary Engineering',
    shortName: 'Industry & R&D',
    category: 'Technical',
    color: '#e0e7ff',
    accent: '#3730a3',
    symbol: '⚙️',
    icon: '/divisions/Industry connect.png',
    description: 'IUCEE education chapters, AgriTech automation, and multidisciplinary student research.',
  },
  'Cultural, Dramatics & Music': {
    name: 'Cultural, Dramatics & Music',
    shortName: 'Music, Dance & Theatre',
    category: 'Non-Technical',
    color: '#fce7f3',
    accent: '#9d174d',
    symbol: '🎭',
    icon: '/divisions/Cultural and Dramatics.png',
    description: 'Classical & western music bands, contemporary street dance, theatrical drama & photography.',
  },
  'Literary, Quizzing & Public Speaking': {
    name: 'Literary, Quizzing & Public Speaking',
    shortName: 'Debate & Quizcorp',
    category: 'Non-Technical',
    color: '#d1fae5',
    accent: '#065f46',
    symbol: '🎙️',
    icon: '/divisions/Quizzing and Public Speaking.png',
    description: 'Parliamentary debate, trivia quizzing, creative writing & official TEDxRVCE events.',
  },
  'Regional, Social Service & Youth Leadership': {
    name: 'Regional, Social Service & Youth Leadership',
    shortName: 'Community & Service',
    category: 'Non-Technical',
    color: '#ffedd5',
    accent: '#9a3412',
    symbol: '🤝',
    icon: '/divisions/Social service and Leadership.png',
    description: 'Rotaract, NSS social welfare, Kannada cultural heritage & youth leadership forums.',
  },
  'Entrepreneurship & Innovation': {
    name: 'Entrepreneurship & Innovation',
    shortName: 'E-Cell & Ventures',
    category: 'Non-Technical',
    color: '#fef9c3',
    accent: '#854d0e',
    symbol: '💡',
    icon: '/divisions/Entrepreneurship and Innovation.png',
    description: 'Startup incubator, angel investment bootcamps & student venture pitch competitions.',
  },
}

function ClubMark({ club, large = false }: { club: Club; large?: boolean }) {
  const [hasError, setHasError] = useState(false)

  useEffect(() => {
    setHasError(false)
  }, [club.logo, club.id])

  const showLogo = club.logo && !hasError

  return (
    <div
      aria-hidden="true"
      className={`club-mark ${large ? 'club-mark-large' : ''} ${showLogo ? 'club-mark-has-logo' : ''}`}
      style={{ 
        '--club-color': club.color, 
        '--club-accent': club.accent,
        ...(showLogo ? { background: '#ffffff', borderColor: 'rgba(0,0,0,0.08)' } : {})
      } as React.CSSProperties}
    >
      {showLogo ? (
        <img 
          key={club.logo}
          src={club.logo} 
          alt={`${club.shortName} logo`} 
          onError={() => setHasError(true)}
          style={{ 
            width: '100%', 
            height: '100%', 
            objectFit: 'contain',
            padding: '6px',
            borderRadius: 'inherit'
          }} 
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

function DetailDialog({ club, onClose, onBack }: { club: Club | null; onClose: () => void; onBack: () => void }) {
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
        <div className="dialog-actions">
          <button className="dialog-back" onClick={onBack} type="button" aria-label="Back to clubs in this division">
            <ArrowLeft size={17} />
            <span>Clubs</span>
          </button>
        </div>
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

          {club.instagram && <div className="dialog-section contact-section">
            <div className="dialog-section-heading"><span>Find the club</span><span>Lead · {club.lead}</span></div>
            <div className="contact-links">
              {club.instagram && (
                <a 
                  href={club.instagram.startsWith('http://') || club.instagram.startsWith('https://') ? club.instagram : `https://instagram.com/${club.instagram.replace(/^@/, '')}`} 
                  target="_blank" 
                  rel="noreferrer"
                >
                  <AtSign size={16} />
                  {club.instagram.startsWith('http://') || club.instagram.startsWith('https://')
                    ? (club.instagram.match(/instagram\.com\/([a-zA-Z0-9._]+)/)?.[1] ? `@${club.instagram.match(/instagram\.com\/([a-zA-Z0-9._]+)/)![1]}` : club.instagram)
                    : (club.instagram.startsWith('@') ? club.instagram : `@${club.instagram}`)}
                </a>
              )}
            </div>
          </div>}
        </div>
      </section>
    </div>
  )
}

function EventBanner() {
  const [dismissed, setDismissed] = useState(false)
  if (dismissed) return null

  return (
    <div className="event-banner">
      <p>
        <strong>Club Showcase</strong>
        <span className="event-banner-sep">·</span>
        Aug 28 &amp; 29
        <span className="event-banner-sep">·</span>
        <span className="event-banner-detail">Venues across campus — open a club to see its schedule</span>
      </p>
      <button type="button" onClick={() => setDismissed(true)} aria-label="Dismiss showcase banner">
        <X size={15} />
      </button>
    </div>
  )
}

function BackToTop() {
  const [shown, setShown] = useState(false)

  useEffect(() => {
    const onScroll = () => setShown(window.scrollY > 600)
    onScroll()
    window.addEventListener('scroll', onScroll, { passive: true })
    return () => window.removeEventListener('scroll', onScroll)
  }, [])

  return (
    <button
      type="button"
      className={`back-to-top${shown ? ' is-visible' : ''}`}
      onClick={() => window.scrollTo({ top: 0, behavior: 'smooth' })}
      aria-label="Back to top"
      tabIndex={shown ? 0 : -1}
    >
      <ArrowUp size={18} />
    </button>
  )
}

function DivisionDrawer({
  divisionName,
  divisionClubs,
  onClose,
  onOpenClub,
}: {
  divisionName: string | null
  divisionClubs: Club[]
  onClose: () => void
  onOpenClub: (club: Club) => void
}) {
  const [drawerQuery, setDrawerQuery] = useState('')

  useEffect(() => {
    setDrawerQuery('')
  }, [divisionName])

  useEffect(() => {
    if (!divisionName) return
    const handleKey = (e: KeyboardEvent) => {
      if (e.key === 'Escape') onClose()
    }
    document.addEventListener('keydown', handleKey)
    document.body.style.overflow = 'hidden'
    return () => {
      document.removeEventListener('keydown', handleKey)
      document.body.style.overflow = ''
    }
  }, [divisionName, onClose])

  if (!divisionName) return null

  const meta = DIVISION_META[divisionName] || {
    name: divisionName,
    shortName: 'Division',
    category: 'Technical',
    color: '#e2e8f0',
    accent: '#334155',
    symbol: '🏛️',
    description: 'Student communities in this division.',
  }

  const filteredInDrawer = drawerQuery.trim() === ''
    ? divisionClubs
    : divisionClubs.filter(c =>
        c.name.toLowerCase().includes(drawerQuery.toLowerCase()) ||
        c.shortName.toLowerCase().includes(drawerQuery.toLowerCase())
      )

  return (
    <div
      className="drawer-backdrop"
      role="presentation"
      onClick={(e) => e.target === e.currentTarget && onClose()}
    >
      <aside className="division-drawer" role="dialog" aria-modal="true">
        {/* Drawer Header */}
        <div className="drawer-header">
          <div className="dialog-actions">
            <button className="dialog-back" onClick={onClose} type="button" aria-label="Back to divisions">
              <ArrowLeft size={17} />
              <span>Divisions</span>
            </button>
          </div>

          <div style={{ display: 'flex', alignItems: 'center', gap: '20px' }}>
            <div
              className="division-large-mark"
              style={{
                '--div-color': meta.color,
                '--div-accent': meta.accent,
                width: '80px',
                height: '80px',
                borderRadius: '24px',
                fontSize: '34px',
                margin: 0,
              } as React.CSSProperties}
            >
              {meta.icon ? (
                <img
                  src={meta.icon}
                  alt={meta.name}
                  style={{ width: '100%', height: '100%', objectFit: 'cover' }}
                />
              ) : (
                <span>{meta.symbol}</span>
              )}
            </div>

            <div>
              <span className="eyebrow">{meta.category} · {meta.shortName}</span>
              <h2 style={{ fontSize: '26px', margin: '4px 0 2px' }}>{meta.name}</h2>
              <p style={{ margin: 0, fontSize: '13px', color: 'var(--muted-foreground)' }}>
                {divisionClubs.length} {divisionClubs.length === 1 ? 'community' : 'communities'} in this division
              </p>
            </div>
          </div>

          <div style={{ marginTop: '20px' }}>
            <label className="search-field" style={{ width: '100%', maxWidth: '320px' }}>
              <Search size={16} />
              <input
                value={drawerQuery}
                onChange={(e) => setDrawerQuery(e.target.value)}
                placeholder={`Search ${divisionName} clubs...`}
                style={{ width: '100%' }}
              />
            </label>
          </div>
        </div>

        {/* Drawer Body - 3x3 Club Logo Grid */}
        <div className="drawer-body">
          {filteredInDrawer.length > 0 ? (
            <div className="drawer-club-grid">
              {filteredInDrawer.map((club) => (
                <button
                  key={club.id}
                  className="drawer-club-card"
                  onClick={() => onOpenClub(club)}
                  type="button"
                  aria-label={`View ${club.name}`}
                >
                  <ClubMark club={club} large />
                  <div className="drawer-club-info">
                    <h4>{club.name}</h4>
                    <span className="drawer-club-code">{club.shortName}</span>
                  </div>
                </button>
              ))}
            </div>
          ) : (
            <div className="empty-state">No matching clubs found in this division.</div>
          )}
        </div>
      </aside>
    </div>
  )
}

export function ClubShowcase() {
  const [category, setCategory] = useState<(typeof categories)[number]>('All')
  const [division, setDivision] = useState<string>('All')
  const [query, setQuery] = useState('')
  const [visible, setVisible] = useState(false)
  
  const [selectedClub, setSelectedClub] = useState<Club | null>(null)
  const [activeDivisionDrawer, setActiveDivisionDrawer] = useState<string | null>(null)

  const [order, setOrder] = useState(() => clubs.map((_, index) => index))

  useEffect(() => {
    setOrder((current) => [...current].sort(() => Math.random() - 0.5))
  }, [])

  const filteredClubs = useMemo(() => {
    const normalizedQuery = query.trim().toLowerCase()
    return order.map((index) => clubs[index]).filter((club) => {
      const matchesCategory = category === 'All' || club.category === category
      const matchesDivision = division === 'All' || club.division === division
      const matchesQuery = !normalizedQuery || `${club.name} ${club.shortName} ${club.division}`.toLowerCase().includes(normalizedQuery)
      return matchesCategory && matchesDivision && matchesQuery
    })
  }, [category, division, order, query])

  // Group filtered clubs by division for Large Division Cards display
  const divisionsData = useMemo(() => {
    const map: { [divName: string]: Club[] } = {}
    filteredClubs.forEach(c => {
      const div = c.division || 'General'
      if (!map[div]) map[div] = []
      map[div].push(c)
    })

    return Object.entries(map).map(([name, divClubs]) => ({
      name,
      meta: DIVISION_META[name] || {
        name,
        shortName: 'Division',
        category: divClubs[0]?.category || 'Technical',
        color: '#e2e8f0',
        accent: '#334155',
        symbol: '🏛️',
        description: 'Explore the student-led communities in this division.',
      },
      clubs: divClubs,
    }))
  }, [filteredClubs])

  const openClubs = (nextCategory: ClubCategory | 'All') => {
    setCategory(nextCategory)
    setDivision('All')
    setVisible(true)
    window.setTimeout(() => document.getElementById('club-grid')?.scrollIntoView({ behavior: 'smooth', block: 'start' }), 20)
  }

  const shuffle = () => setOrder((current) => [...current].sort(() => Math.random() - 0.5))

  const drawerClubs = useMemo(() => {
    if (!activeDivisionDrawer) return []
    return clubs.filter(c => c.division === activeDivisionDrawer)
  }, [activeDivisionDrawer])

  return (
    <main>
      <EventBanner />

      <div className="site-header-bar">
      <header className="site-header">
        <div className="header-brand-group">
          <a href="#top" className="rvce-logo-link" title="RV College of Engineering">
            <img src="/rvce-logo.png" alt="RV College of Engineering" className="rvce-top-logo" />
          </a>
          <div className="header-brand-divider" />
          <a className="wordmark" href="#top" aria-label="The clubs of RVCE home">
            <span>RVCE</span><i>Clubs</i>
          </a>
        </div>
        <nav className="main-nav" aria-label="Main navigation">
          <a href="#clubs">Clubs <span>{clubs.length}</span></a>
          <a href="#clubs">Wall</a>
        </nav>
        <button className="header-action" onClick={() => openClubs('All')} type="button" aria-label="Open club wall"><Search size={17} /><span>Explore clubs</span><ArrowUpRight size={16} /></button>
      </header>
      </div>

      <section className="hero" id="top">
        <div className="hero-copy">
          <div className="hero-logo-wrapper">
            <img src="/rvce-logo.png" alt="RV College of Engineering Logo" className="hero-rvce-logo" />
          </div>
          <p className="eyebrow hero-eyebrow">RV College of Engineering · Bengaluru</p>
          <h1>A collection of iconic<br /><em>campus clubs.</em></h1>
          <p className="hero-description">A living directory of the people, practices, and communities that make campus feel like more than a campus.</p>
          
          <div className="hero-signup">
            <div className="hero-input-wrapper">
              <Search size={16} className="hero-input-icon" />
              <input
                className="hero-input-field"
                value={query}
                onChange={(event) => setQuery(event.target.value)}
                placeholder="Search the club wall..."
              />
            </div>
            <button className="primary-action" type="button" onClick={() => openClubs('All')}>Browse clubs <ArrowUpRight size={17} /></button>
          </div>

          <div className="hero-actions">
            <button className="text-action" type="button" onClick={() => openClubs('Technical')}>Technical <span>{clubs.filter((club) => club.category === 'Technical').length}</span></button>
            <button className="text-action" type="button" onClick={() => openClubs('Non-Technical')}>Non-technical <span>{clubs.filter((club) => club.category === 'Non-Technical').length}</span></button>
            <span className="hero-divider">•</span>
            <span className="hero-stat-badge">{clubs.length} COMMUNITIES · ONE CAMPUS</span>
          </div>
        </div>
      </section>

      <section className={`directory ${visible ? 'directory-visible' : ''}`} id="clubs">
        <div className="directory-heading" id="club-grid">
          <div><p className="eyebrow">The directory</p><h2>Find your people.</h2></div>
          <p className="directory-intro">Browse the student-led communities shaping life at RVCE, grouped by specialized division.</p>
        </div>

        <div className="directory-toolbar">
          <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
            <div className="category-tabs" role="tablist" aria-label="Filter clubs by category">
              {categories.map((item) => <button key={item} className={category === item ? 'active' : ''} onClick={() => { setCategory(item); setDivision('All'); setVisible(true) }} type="button" role="tab" aria-selected={category === item}>{item}</button>)}
            </div>
          </div>
          <div className="toolbar-actions">
            <label className="search-field"><Search size={16} /><span className="sr-only">Search clubs</span><input value={query} onChange={(event) => setQuery(event.target.value)} placeholder="Search clubs or divisions" /></label>
            <button className="shuffle-action" type="button" onClick={shuffle}><Shuffle size={15} /> Shuffle</button>
          </div>
        </div>

        <div className="club-count">Showing {divisionsData.length} divisions ({filteredClubs.length} total clubs)</div>

        {/* Large Division Cards Display */}
        {divisionsData.length > 0 ? (
          <div className="division-cards-grid">
            {divisionsData.map(({ name, meta, clubs: divClubs }) => (
              <button
                key={name}
                type="button"
                className="division-large-card"
                onClick={() => setActiveDivisionDrawer(name)}
                aria-label={`Open ${name} drawer`}
              >
                <div className="division-icon-container">
                  {meta.icon ? (
                    <img
                      src={meta.icon}
                      alt={name}
                      className="division-icon-img"
                    />
                  ) : (
                    <span className="division-icon-symbol">{meta.symbol}</span>
                  )}
                </div>

                <h3 className="division-card-title">{name}</h3>

                <span className="division-card-count">
                  {divClubs.length} {divClubs.length === 1 ? 'Club' : 'Clubs'}
                </span>
              </button>
            ))}
          </div>
        ) : (
          <div className="empty-state">No divisions or clubs found. Try a different search query.</div>
        )}
      </section>

      <footer className="site-footer" id="about"><div><span className="wordmark"><span>RVCE</span><i>Clubs</i></span><p>Built by students, for students.</p></div><span>© {new Date().getFullYear()} · Bengaluru, India</span></footer>

      {/* Slide-over Division Drawer */}
      <DivisionDrawer
        divisionName={activeDivisionDrawer}
        divisionClubs={drawerClubs}
        onClose={() => setActiveDivisionDrawer(null)}
        onOpenClub={(club) => setSelectedClub(club)}
      />

      {/* Club Exhibit Detail Modal */}
      <DetailDialog
        club={selectedClub}
        /* Back steps up one level to the division's club list; ✕ exits all the way to the divisions grid. */
        onBack={() => setSelectedClub(null)}
        onClose={() => { setSelectedClub(null); setActiveDivisionDrawer(null) }}
      />

      <BackToTop />
    </main>
  )
}
