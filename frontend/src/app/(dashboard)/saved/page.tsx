'use client';

import { useRouter } from 'next/navigation';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { format } from 'date-fns';
import { Card, CardContent } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Play, MoreHorizontal, Trash, Share } from 'lucide-react';
import { api } from '@/services/api';
import { Skeleton } from '@/components/ui/skeleton';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"

export default function SavedSearchesPage() {
  const router = useRouter();
  const { data, isLoading } = useQuery({
    queryKey: ['saved-searches'],
    queryFn: async () => {
      const res = await api.get('/saved-searches');
      return res.data;
    }
  });

  const queryClient = useQueryClient();
  const deleteMutation = useMutation({
    mutationFn: async (id: number) => {
      await api.delete(`/saved-searches/${id}`);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['saved-searches'] });
    }
  });

  const handleShare = async (item: any) => {
    const params = new URLSearchParams();
    if (item.filters?.niche) params.append('niche', item.filters.niche);
    if (item.filters?.city) params.append('city', item.filters.city);
    if (item.filters?.country) params.append('country', item.filters.country);
    
    const searchUrl = `${window.location.origin}/search?${params.toString()}`;
    
    const filterText = Object.entries(item.filters || {})
      .map(([k, v]) => `${k}: ${v}`)
      .join(', ');
    const text = `Check out this search: ${item.name} - ${filterText}`;
    
    if (navigator.share) {
      try {
        await navigator.share({
          title: item.name,
          text: text,
          url: searchUrl
        });
      } catch (err) {
        console.error('Error sharing:', err);
      }
    } else {
      navigator.clipboard.writeText(`${text}\nLink: ${searchUrl}`);
      alert('Search details and link copied to clipboard!');
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-3xl font-bold tracking-tight">Saved Searches</h2>
        <p className="text-muted-foreground">Manage your favorite search filters to run them again quickly.</p>
      </div>

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        {isLoading ? (
          [1, 2, 3].map(i => (
            <Card key={i}>
              <CardContent className="p-6">
                <Skeleton className="h-4 w-3/4 mb-4" />
                <Skeleton className="h-4 w-1/2" />
              </CardContent>
            </Card>
          ))
        ) : data?.length === 0 ? (
          <Card className="col-span-full">
            <CardContent className="p-10 text-center text-muted-foreground">
              No saved searches found. Save a search from your history to see it here.
            </CardContent>
          </Card>
        ) : (
          data?.map((item: any) => (
            <Card key={item.id} className="hover:border-primary/50 transition-colors">
              <CardContent className="p-6">
                <div className="flex items-start justify-between mb-4">
                  <div>
                    <h3 className="font-semibold text-lg">{item.name}</h3>
                    <p className="text-sm text-muted-foreground">
                      Created on {format(new Date(item.created_at), 'MMM d, yyyy')}
                    </p>
                  </div>
                  <DropdownMenu>
                    <DropdownMenuTrigger>
                      <div className="inline-flex items-center justify-center whitespace-nowrap rounded-md text-sm font-medium ring-offset-background transition-colors hover:bg-accent hover:text-accent-foreground h-9 w-9 -mr-2 -mt-2">
                        <MoreHorizontal className="h-4 w-4" />
                      </div>
                    </DropdownMenuTrigger>
                    <DropdownMenuContent align="end">
                      <DropdownMenuLabel>Actions</DropdownMenuLabel>
                      <DropdownMenuItem onClick={() => handleShare(item)}>
                        <Share className="h-4 w-4 mr-2" /> Share
                      </DropdownMenuItem>
                      <DropdownMenuSeparator />
                      <DropdownMenuItem className="text-destructive" onClick={() => deleteMutation.mutate(item.id)}>
                        <Trash className="h-4 w-4 mr-2" /> Delete
                      </DropdownMenuItem>
                    </DropdownMenuContent>
                  </DropdownMenu>
                </div>

                <div className="flex flex-wrap gap-2 mb-6">
                  {Object.entries(item.filters || {}).map(([key, value]) => (
                    <Badge key={key} variant="secondary">
                      {key}: {String(value)}
                    </Badge>
                  ))}
                </div>

                <Button className="w-full" onClick={() => {
                  const params = new URLSearchParams();
                  if (item.filters?.niche) params.append('niche', item.filters.niche);
                  if (item.filters?.city) params.append('city', item.filters.city);
                  if (item.filters?.country) params.append('country', item.filters.country);
                  router.push(`/search?${params.toString()}`);
                }}>
                  <Play className="h-4 w-4 mr-2" />
                  Run Search Again
                </Button>
              </CardContent>
            </Card>
          ))
        )}
      </div>
    </div>
  );
}
