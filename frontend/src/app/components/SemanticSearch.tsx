import { useState } from 'react';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Search, FileText, ExternalLink } from 'lucide-react';
import { Badge } from './ui/badge';

interface SearchResult {
  id: string;
  videoTitle: string;
  youtubeUrl: string;
  snippet: string;
  relevanceScore: number;
  timestamp: string;
}

interface SemanticSearchProps {
  processedVideosCount: number;
}

export function SemanticSearch({ processedVideosCount }: SemanticSearchProps) {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState<SearchResult[]>([]);
  const [isSearching, setIsSearching] = useState(false);

  // Mock search results for demonstration
  const mockResults: SearchResult[] = [
    {
      id: '1',
      videoTitle: 'Introduction to Machine Learning',
      youtubeUrl: 'https://youtube.com/watch?v=example1',
      snippet: 'Machine learning is a subset of artificial intelligence that focuses on enabling computers to learn from data without being explicitly programmed...',
      relevanceScore: 0.95,
      timestamp: '02:34'
    },
    {
      id: '2',
      videoTitle: 'Deep Learning Fundamentals',
      youtubeUrl: 'https://youtube.com/watch?v=example2',
      snippet: 'Neural networks are the foundation of deep learning, inspired by biological neurons in the human brain. They process information through layers...',
      relevanceScore: 0.87,
      timestamp: '05:12'
    },
    {
      id: '3',
      videoTitle: 'AI Ethics and Society',
      youtubeUrl: 'https://youtube.com/watch?v=example3',
      snippet: 'As AI systems become more prevalent, we must consider the ethical implications and societal impact of these technologies...',
      relevanceScore: 0.76,
      timestamp: '08:45'
    }
  ];

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!query.trim()) return;
    
    setIsSearching(true);
    
    // Simulate API call
    setTimeout(() => {
      setResults(mockResults);
      setIsSearching(false);
    }, 1000);
  };

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Search className="w-5 h-5" />
            Semantic Search
          </CardTitle>
          <CardDescription>
            Search across {processedVideosCount} processed video transcript{processedVideosCount !== 1 ? 's' : ''} using natural language
          </CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSearch} className="space-y-4">
            <div className="flex gap-2">
              <div className="relative flex-1">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400" />
                <Input
                  type="text"
                  placeholder="e.g., 'What is machine learning?' or 'Explain neural networks'"
                  value={query}
                  onChange={(e) => setQuery(e.target.value)}
                  className="pl-10"
                />
              </div>
              <Button type="submit" disabled={!query.trim() || isSearching}>
                {isSearching ? 'Searching...' : 'Search'}
              </Button>
            </div>

            <div className="bg-purple-50 border border-purple-200 rounded-lg p-4">
              <h4 className="font-medium text-purple-900 mb-2">How it works:</h4>
              <p className="text-sm text-purple-800">
                Semantic search uses vector embeddings to understand the meaning behind your query, 
                not just keyword matching. Ask questions naturally and find relevant content across all transcripts.
              </p>
            </div>
          </form>
        </CardContent>
      </Card>

      {results.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle>Search Results</CardTitle>
            <CardDescription>
              Found {results.length} relevant segment{results.length !== 1 ? 's' : ''}
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {results.map((result) => (
                <div
                  key={result.id}
                  className="p-4 border border-gray-200 rounded-lg hover:border-blue-300 hover:shadow-md transition-all"
                >
                  <div className="flex items-start justify-between gap-4 mb-3">
                    <div className="flex-1">
                      <div className="flex items-center gap-2 mb-1">
                        <FileText className="w-4 h-4 text-blue-600" />
                        <h3 className="font-medium text-gray-900">{result.videoTitle}</h3>
                      </div>
                      <div className="flex items-center gap-2 text-sm text-gray-500">
                        <span className="bg-gray-100 px-2 py-0.5 rounded">
                          {result.timestamp}
                        </span>
                        <a 
                          href={result.youtubeUrl}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="flex items-center gap-1 text-blue-600 hover:text-blue-700 hover:underline"
                        >
                          Watch video
                          <ExternalLink className="w-3 h-3" />
                        </a>
                      </div>
                    </div>
                    <Badge variant="secondary" className="shrink-0">
                      {Math.round(result.relevanceScore * 100)}% match
                    </Badge>
                  </div>
                  <p className="text-gray-700 leading-relaxed">{result.snippet}</p>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}

      {results.length === 0 && query && !isSearching && (
        <Card>
          <CardContent className="py-12">
            <div className="text-center text-gray-500">
              <Search className="w-12 h-12 mx-auto mb-3 text-gray-400" />
              <p>No results found</p>
              <p className="text-sm mt-1">Try a different search query</p>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
}
