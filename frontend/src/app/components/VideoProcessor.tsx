import { useState } from 'react';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Upload, Link2 } from 'lucide-react';

interface VideoProcessorProps {
  onSubmit: (url: string) => void;
}

export function VideoProcessor({ onSubmit }: VideoProcessorProps) {
  const [url, setUrl] = useState('');
  const [isValid, setIsValid] = useState(true);

  const validateYouTubeUrl = (url: string): boolean => {
    const youtubeRegex = /^(https?:\/\/)?(www\.)?(youtube\.com|youtu\.be)\/.+/;
    return youtubeRegex.test(url);
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!validateYouTubeUrl(url)) {
      setIsValid(false);
      return;
    }
    
    setIsValid(true);
    onSubmit(url);
    setUrl('');
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Upload className="w-5 h-5" />
          Add YouTube Video
        </CardTitle>
        <CardDescription>
          Enter a YouTube URL to extract and process the video transcript
        </CardDescription>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="space-y-2">
            <div className="flex gap-2">
              <div className="relative flex-1">
                <Link2 className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400" />
                <Input
                  type="text"
                  placeholder="https://www.youtube.com/watch?v=..."
                  value={url}
                  onChange={(e) => {
                    setUrl(e.target.value);
                    setIsValid(true);
                  }}
                  className={`pl-10 ${!isValid ? 'border-red-500' : ''}`}
                />
              </div>
              <Button type="submit" disabled={!url.trim()}>
                Process Video
              </Button>
            </div>
            {!isValid && (
              <p className="text-sm text-red-600">Please enter a valid YouTube URL</p>
            )}
          </div>
          
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
            <h4 className="font-medium text-blue-900 mb-2">Processing Pipeline:</h4>
            <ol className="text-sm text-blue-800 space-y-1 list-decimal list-inside">
              <li>Extract video from YouTube</li>
              <li>Convert video to audio</li>
              <li>Generate transcript from audio</li>
              <li>Vectorize transcript for semantic search</li>
            </ol>
          </div>
        </form>
      </CardContent>
    </Card>
  );
}
