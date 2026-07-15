'use client';

import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { format } from 'date-fns';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Play, Star, MoreHorizontal, Trash } from 'lucide-react';
import { api } from '@/services/api';
import { Skeleton } from '@/components/ui/skeleton';
import { useRouter } from 'next/navigation';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"

export default function SearchHistoryPage() {
  const router = useRouter();

  const { data, isLoading } = useQuery({
    queryKey: ['search-history'],
    queryFn: async () => {
      const res = await api.get('/search-history');
      return res.data;
    }
  });

  const queryClient = useQueryClient();

  const deleteMutation = useMutation({
    mutationFn: async (id: number) => {
      await api.delete(`/search-history/${id}`);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['search-history'] });
    }
  });

  const saveSearchMutation = useMutation({
    mutationFn: async (item: any) => {
      const name = `${item.search_params?.niche || "Any"} in ${item.search_params?.city || "Any City"}`;
      const res = await api.post('/saved-searches', {
        name,
        filters: item.search_params || {}
      });
      return res.data;
    },
    onSuccess: () => {
      alert("Search saved successfully!");
    },
    onError: () => {
      alert("Failed to save search.");
    }
  });

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-3xl font-bold tracking-tight">Search History</h2>
        <p className="text-muted-foreground">View your past searches, run them again, or save them.</p>
      </div>

      <div className="grid gap-4">
        {isLoading ? (
          [1, 2, 3].map(i => (
            <Card key={i}>
              <CardContent className="p-6">
                <Skeleton className="h-4 w-[250px] mb-4" />
                <Skeleton className="h-4 w-[200px]" />
              </CardContent>
            </Card>
          ))
        ) : data?.items?.length === 0 ? (
          <Card>
            <CardContent className="p-10 text-center text-muted-foreground">
              No search history found.
            </CardContent>
          </Card>
        ) : (
          data?.items?.map((item: any) => (
            <Card key={item.id} className="hover:border-primary/50 transition-colors">
              <CardContent className="p-6 flex items-center justify-between">
                <div className="space-y-1">
                  <div className="flex items-center gap-2">
                    <h3 className="font-semibold text-lg">
                      {item.search_params?.niche || "Any"} in {item.search_params?.city || "Any City"}, {item.search_params?.country || "Any Country"}
                    </h3>
                    <Badge variant="secondary">{item.results_count} leads found</Badge>
                  </div>
                  <p className="text-sm text-muted-foreground">
                    Searched on {format(new Date(item.created_at), 'PPPp')}
                  </p>
                </div>
                
                <div className="flex items-center gap-2">
                  <Button 
                    variant="outline" 
                    size="sm"
                    onClick={() => {
                      const params = new URLSearchParams();
                      if (item.search_params?.niche) params.append('niche', item.search_params.niche);
                      if (item.search_params?.city) params.append('city', item.search_params.city);
                      if (item.search_params?.country) params.append('country', item.search_params.country);
                      router.push(`/search?${params.toString()}`);
                    }}
                  >
                    <Play className="h-4 w-4 mr-2" />
                    Run Again
                  </Button>
                  
                  <DropdownMenu>
                    <DropdownMenuTrigger>
                      <div className="inline-flex items-center justify-center whitespace-nowrap rounded-md text-sm font-medium ring-offset-background transition-colors hover:bg-accent hover:text-accent-foreground h-9 w-9">
                        <MoreHorizontal className="h-4 w-4" />
                      </div>
                    </DropdownMenuTrigger>
                    <DropdownMenuContent align="end">
                      <DropdownMenuLabel>Actions</DropdownMenuLabel>
                      <DropdownMenuItem onClick={() => saveSearchMutation.mutate(item)}>
                        <Star className="h-4 w-4 mr-2" /> Save Search
                      </DropdownMenuItem>
                      <DropdownMenuSeparator />
                      <DropdownMenuItem 
                        className="text-destructive"
                        onClick={() => deleteMutation.mutate(item.id)}
                      >
                        <Trash className="h-4 w-4 mr-2" /> Delete
                      </DropdownMenuItem>
                    </DropdownMenuContent>
                  </DropdownMenu>
                </div>
              </CardContent>
            </Card>
          ))
        )}
      </div>
    </div>
  );
}
