# FinPulse

FinPulse is a production-ready Financial News Aggregator that collects Indonesian financial news, stores it in PostgreSQL, performs sentiment analysis, and displays it through a modern Next.js frontend.

This platform is designed to aggregate market intelligence cleanly, classify sentiment as positive or negative, and serve as an elite portfolio project showcasing clean architecture, SOLID principles, and high-quality software engineering practices.

## Project Structure

```text
finpulse/
├── backend/          # FastAPI Backend API
├── frontend/         # Next.js Frontend (App Router)
├── scraper/          # Python News Scraper & Sentiment Engine
├── docs/             # Technical Documentation & Sprint Specs
├── nginx/            # Nginx Reverse Proxy Configuration
├── docker-compose.yml
└── README.md
```

## Tech Stack

- **Backend:** Python 3.13 / 3.14, FastAPI, SQLAlchemy 2.x, Alembic, PostgreSQL (Supabase), Pydantic v2, uv
- **Frontend:** Next.js, React, TypeScript, TailwindCSS, shadcn/ui
- **Scraper & Sentiment:** httpx, BeautifulSoup4, feedparser, rule-based keyword matching (with model-based expansion capabilities)
- **Deployment:** Docker, Docker Compose, Nginx, Ubuntu Server

## Core Features

- **Automated News Scraping:** Periodically pulls financial news feeds.
- **Sentiment Engine:** Classifies incoming articles as Positive or Negative.
- **REST API:** Fast, stateless API layer serving paginated, filtered, and searchable news.
- **Responsive UI:** Content-first, minimal design with light/dark theme capabilities.

## Getting Started

Instructions for local development and running via Docker are in the respective guides.
