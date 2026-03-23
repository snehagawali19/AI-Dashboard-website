export interface Source {
  id: number;
  name: string;
  url: string;
  category?: string;
}

export interface NewsItem {
  id: string;
  title: string;
  url: string;
  summary?: string;
  tags?: string[];
  image_url?: string;
  author?: string;
  published_at?: string;
  created_at?: string;
  category?: string; 
  source: Source;
  is_favorited: boolean;
}

export interface PaginatedNews {
  items: NewsItem[];
  total: number;
  page: number;
  per_page: number;
  has_more: boolean;
}

export interface Favorite {
  id: string;
  news_item: NewsItem;
  created_at: string;
}

export interface BroadcastResult {
  message: string;
  channel: string;
  preview?: string;
}
