import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Badge } from './ui/badge';
import { CheckCircle2, Clock, XCircle, Video } from 'lucide-react';
import type { ProcessedVideo } from '../App';

interface VideoListProps {
  videos: ProcessedVideo[];
}

export function VideoList({ videos }: VideoListProps) {
  if (videos.length === 0) {
    return (
      <Card>
        <CardContent className="py-12">
          <div className="text-center text-gray-500">
            <Video className="w-12 h-12 mx-auto mb-3 text-gray-400" />
            <p>No videos processed yet</p>
            <p className="text-sm mt-1">Add a YouTube URL above to get started</p>
          </div>
        </CardContent>
      </Card>
    );
  }

  const getStatusIcon = (status: ProcessedVideo['status']) => {
    switch (status) {
      case 'completed':
        return <CheckCircle2 className="w-4 h-4" />;
      case 'processing':
        return <Clock className="w-4 h-4" />;
      case 'failed':
        return <XCircle className="w-4 h-4" />;
    }
  };

  const getStatusVariant = (status: ProcessedVideo['status']) => {
    switch (status) {
      case 'completed':
        return 'default';
      case 'processing':
        return 'secondary';
      case 'failed':
        return 'destructive';
    }
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle>Processed Videos</CardTitle>
        <CardDescription>
          {videos.length} video{videos.length !== 1 ? 's' : ''} in the system
        </CardDescription>
      </CardHeader>
      <CardContent>
        <div className="space-y-3">
          {videos.map((video) => (
            <div
              key={video.id}
              className="flex items-center justify-between p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors"
            >
              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-2 mb-1">
                  <Video className="w-4 h-4 text-gray-400 flex-shrink-0" />
                  <p className="font-medium text-gray-900">{video.title}</p>
                </div>
                <p className="text-sm text-gray-500 truncate">{video.youtubeUrl}</p>
                {video.processedAt && (
                  <p className="text-xs text-gray-400 mt-1">
                    Processed at {video.processedAt.toLocaleString()}
                  </p>
                )}
              </div>
              <Badge variant={getStatusVariant(video.status)} className="flex items-center gap-1 ml-4">
                {getStatusIcon(video.status)}
                {video.status}
              </Badge>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
}
