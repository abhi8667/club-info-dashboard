import clubsData from './clubs.json'

export type ClubCategory = 'Technical' | 'Non-Technical'

export type ClubEvent = {
  name: string
  date: string
  time: string
  venue: string
  detail: string
}

export type Club = {
  id: string
  name: string
  shortName: string
  category: ClubCategory
  description: string
  color: string
  accent: string
  symbol: string
  logo?: string
  lead: string
  email: string
  instagram: string
  venue: string
  images: string[]
  events: ClubEvent[]
}

export const clubs: Club[] = clubsData as Club[]
