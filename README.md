# Fashion Search Engine

A full-stack application that enables users to search for fashion items using both text descriptions and image similarity. The project uses machine learning techniques to provide accurate search results based on user queries.

## Project Structure

```
fashion-search/
├── cosine_similarity/         # Backend Python code
│   ├── app.py                # FastAPI server
│   ├── data_explorer.py      # Data analysis utilities
│   ├── fashion_recommender.py # Core recommendation engine
│   ├── get_fashion_data.py   # Data loading utilities
│   └── requirements.txt      # Python dependencies
│
├── dataset/                  # Data directory (not tracked in git)
│   ├── Fashion Dataset.csv   # Main dataset file
│   └── analysis_output/      # Generated analysis files
│
└── fashion-frontend/         # React frontend
    ├── src/
    │   ├── components/
    │   │   └── FashionSearch.jsx
    │   ├── App.jsx
    │   └── main.jsx
    ├── package.json
    └── vite.config.js
```

## Setup

### Backend Setup

1. Create and activate a virtual environment:
```bash
cd cosine_similarity
python -m venv myenv
source myenv/bin/activate  # On Windows: myenv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Start the FastAPI server:
```bash
python app.py
```

### Frontend Setup

1. Install dependencies:
```bash
cd fashion-frontend
npm install
```

2. Start the development server:
```bash
npm run dev
```

## Features

- Text-based search using cosine similarity
- Product recommendations based on description matching
- Interactive web interface
- Pagination support
- Responsive design

## Technologies Used

- **Backend:**
  - Python
  - FastAPI
  - scikit-learn
  - pandas

- **Frontend:**
  - React
  - Vite
  - Tailwind CSS
  - Lucide Icons

## License

MIT License

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request
