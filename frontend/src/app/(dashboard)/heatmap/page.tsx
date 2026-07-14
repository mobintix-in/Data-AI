'use client';

import { useQuery } from '@tanstack/react-query';
import dynamic from 'next/dynamic';
import { api } from '@/services/api';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Skeleton } from '@/components/ui/skeleton';

// Dynamically import the map component so it doesn't render on the server
// (React-Leaflet accesses window object which causes errors in Next.js SSR)
const HeatmapComponent = dynamic(
  () => import('./HeatmapComponent'),
  { 
    ssr: false,
    loading: () => <Skeleton className="w-full h-[600px] rounded-md" />
  }
);

export default function HeatmapPage() {
  const { data, isLoading } = useQuery({
    queryKey: ['heatmap-data'],
    queryFn: async () => {
      const res = await api.get('/heatmap');
      return res.data;
    }
  });

  return (
    <div className="space-y-6 h-[calc(100vh-120px)] flex flex-col">
      <div>
        <h2 className="text-3xl font-bold tracking-tight">Geographic Heatmap</h2>
        <p className="text-muted-foreground">Visualize your generated leads on a world map.</p>
      </div>

      <Card className="flex-1 flex flex-col overflow-hidden">
        <CardHeader className="py-4">
          <CardTitle>Lead Density Map</CardTitle>
          <CardDescription>All your scraped leads plotted by their latitude and longitude.</CardDescription>
        </CardHeader>
        <CardContent className="flex-1 p-0 overflow-hidden relative">
          {isLoading ? (
            <Skeleton className="w-full h-full absolute inset-0 rounded-none m-4" />
          ) : (
            <HeatmapComponent leads={data?.data || []} />
          )}
        </CardContent>
      </Card>
    </div>
  );
}
