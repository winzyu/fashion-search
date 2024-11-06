import { useState } from 'react';
import { Search, Loader2 } from 'lucide-react';

export default function FashionSearch() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [loadingMore, setLoadingMore] = useState(false);
  const [error, setError] = useState('');
  const [currentPage, setCurrentPage] = useState(1);
  const [hasMore, setHasMore] = useState(true);
  const PAGE_SIZE = 5;

  const handleSearch = async (e, isLoadMore = false) => {
    e?.preventDefault();
    if (!query.trim()) return;

    if (isLoadMore) {
      setLoadingMore(true);
    } else {
      setLoading(true);
      setResults([]);
      setCurrentPage(1);
    }
    
    setError('');
    
    try {
      const page = isLoadMore ? currentPage + 1 : 1;
      
      const response = await fetch('http://localhost:8000/search', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          query: query,
          page_size: PAGE_SIZE,
          page: page
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      
      if (isLoadMore) {
        setResults(prev => [...prev, ...data.results]);
      } else {
        setResults(data.results);
      }
      
      setHasMore(data.has_more);
      setCurrentPage(data.current_page);
    } catch (err) {
      console.error('Error:', err);
      setError('Failed to fetch results. Please try again.');
    } finally {
      setLoading(false);
      setLoadingMore(false);
    }
  };

  const ProductCard = ({ product }) => (
    <div className="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow duration-300">
      <div className="aspect-square w-full relative bg-gray-100">
        <img
          src={product.image_url}
          alt={product.name}
          onError={(e) => {
            e.target.src = "/api/placeholder/400/400";
          }}
          className="w-full h-full object-cover"
        />
      </div>
      <div className="p-4">
        <h3 className="font-semibold text-lg mb-2 line-clamp-2 min-h-[3.5rem]">
          {product.name}
        </h3>
        <div className="flex items-center justify-between mb-2">
          <span className="text-lg font-bold text-blue-600">
            ₹{product.price.toLocaleString()}
          </span>
          <span className="text-sm bg-blue-100 text-blue-800 px-2 py-1 rounded-full">
            {(product.similarity_score * 100).toFixed(1)}% match
          </span>
        </div>
        <div className="text-sm text-gray-600 mb-2">{product.brand}</div>
        <p className="text-sm text-gray-500 line-clamp-3">
          {product.description}
        </p>
      </div>
    </div>
  );

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-6xl mx-auto p-6">
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-center mb-6 text-gray-800">
            Fashion Search
          </h1>
          
          {/* Search Form */}
          <form onSubmit={handleSearch} className="max-w-2xl mx-auto">
            <div className="flex gap-2">
              <input
                type="text"
                id="search-input"
                name="search-query"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="Describe what you're looking for... (e.g., blue jeans, black dress)"
                className="flex-1 p-4 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 shadow-sm"
              />
              <button
                type="submit"
                disabled={loading}
                className="bg-blue-500 text-white px-8 py-4 rounded-lg hover:bg-blue-600 
                         flex items-center gap-2 disabled:bg-blue-300 shadow-sm"
              >
                {loading ? (
                  <Loader2 className="h-5 w-5 animate-spin" />
                ) : (
                  <Search className="h-5 w-5" />
                )}
                Search
              </button>
            </div>
          </form>

          {/* Error Message */}
          {error && (
            <div className="mt-4 text-red-500 text-center" role="alert">
              {error}
            </div>
          )}
        </div>

        {/* Results Section */}
        <div className="space-y-6">
          {/* Results Grid */}
          {results.length > 0 && (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {results.map((product, index) => (
                <ProductCard key={index} product={product} />
              ))}
            </div>
          )}

          {/* Load More Button */}
          {results.length > 0 && hasMore && (
            <div className="flex justify-center mt-8">
              <button
                onClick={(e) => handleSearch(e, true)}
                disabled={loadingMore}
                className="bg-white text-blue-500 border border-blue-500 px-8 py-3 rounded-lg
                         hover:bg-blue-50 flex items-center gap-2 disabled:opacity-50"
              >
                {loadingMore ? (
                  <>
                    <Loader2 className="h-5 w-5 animate-spin" />
                    Loading more...
                  </>
                ) : (
                  'Load More Results'
                )}
              </button>
            </div>
          )}

          {/* Loading State */}
          {loading && (
            <div className="flex justify-center items-center min-h-[200px]">
              <Loader2 className="h-8 w-8 animate-spin text-blue-500" />
            </div>
          )}

          {/* No Results State */}
          {query && !loading && results.length === 0 && (
            <div className="text-center text-gray-500 mt-8">
              No results found. Try a different search term.
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
