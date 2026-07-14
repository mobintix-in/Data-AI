'use client';

import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { format } from 'date-fns';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Download, FileSpreadsheet, FileText, Trash, Loader2 } from 'lucide-react';
import { api } from '@/services/api';
import { Skeleton } from '@/components/ui/skeleton';

export default function ExportsPage() {
  const queryClient = useQueryClient();

  const { data, isLoading, refetch } = useQuery({
    queryKey: ['export-history'],
    queryFn: async () => {
      const res = await api.get('/exports/history');
      return res.data;
    }
  });

  const exportMutation = useMutation({
    mutationFn: async (type: 'excel' | 'csv') => {
      const res = await api.get(`/exports/generate?export_type=${type}`);
      return res.data;
    },
    onSuccess: (data) => {
      if (data.file_url) {
        window.location.href = `${process.env.NEXT_PUBLIC_API_URL?.replace('/api', '') || 'http://localhost:5000'}${data.file_url}`;
      }
      refetch();
    }
  });

  const deleteMutation = useMutation({
    mutationFn: async (id: number) => {
      await api.delete(`/exports/${id}`);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['export-history'] });
    }
  });

  const bulkDeleteMutation = useMutation({
    mutationFn: async (type: 'excel' | 'csv') => {
      await api.delete(`/exports/bulk?export_type=${type}`);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['export-history'] });
    }
  });

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-end flex-wrap gap-4">
        <div>
          <h2 className="text-3xl font-bold tracking-tight">Exports</h2>
          <p className="text-muted-foreground">Manage your generated files and generate new exports.</p>
        </div>
        <div className="flex flex-wrap gap-2">
          <Button 
            variant="outline" 
            className="text-red-500 hover:text-red-600 hover:bg-red-50 dark:hover:bg-red-950 border-red-200 dark:border-red-900"
            onClick={() => {
              if (window.confirm('Are you sure you want to delete all CSV exports?')) {
                bulkDeleteMutation.mutate('csv');
              }
            }}
            disabled={bulkDeleteMutation.isPending}
          >
            <Trash className="mr-2 h-4 w-4" />
            Delete CSVs
          </Button>
          <Button 
            variant="outline" 
            className="text-red-500 hover:text-red-600 hover:bg-red-50 dark:hover:bg-red-950 border-red-200 dark:border-red-900"
            onClick={() => {
              if (window.confirm('Are you sure you want to delete all Excel exports?')) {
                bulkDeleteMutation.mutate('excel');
              }
            }}
            disabled={bulkDeleteMutation.isPending}
          >
            <Trash className="mr-2 h-4 w-4" />
            Delete Excels
          </Button>
          <div className="w-px h-10 bg-border mx-1 hidden sm:block"></div>
          <Button 
            variant="outline" 
            onClick={() => exportMutation.mutate('csv')}
            disabled={exportMutation.isPending}
          >
            {exportMutation.isPending ? <Loader2 className="mr-2 h-4 w-4 animate-spin" /> : <FileText className="mr-2 h-4 w-4" />}
            Export CSV
          </Button>
          <Button 
            onClick={() => exportMutation.mutate('excel')}
            disabled={exportMutation.isPending}
          >
            {exportMutation.isPending ? <Loader2 className="mr-2 h-4 w-4 animate-spin" /> : <FileSpreadsheet className="mr-2 h-4 w-4" />}
            Export Excel
          </Button>
        </div>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Export History</CardTitle>
          <CardDescription>A log of all the files you have previously exported.</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {isLoading ? (
              [1, 2, 3].map(i => (
                <div key={i} className="flex justify-between p-4 border rounded-md">
                  <Skeleton className="h-4 w-[200px]" />
                  <Skeleton className="h-8 w-8" />
                </div>
              ))
            ) : data?.length === 0 ? (
              <p className="text-center text-muted-foreground py-8">No exports found.</p>
            ) : (
              data?.map((item: any) => (
                <div key={item.id} className="flex items-center justify-between p-4 border rounded-md hover:bg-muted/50 transition-colors">
                  <div className="flex items-center gap-4">
                    {item.file_type === 'EXCEL' ? (
                      <FileSpreadsheet className="h-8 w-8 text-green-600" />
                    ) : (
                      <FileText className="h-8 w-8 text-blue-600" />
                    )}
                    <div>
                      <p className="font-medium">
                        Export {item.id} - {item.row_count} Rows
                      </p>
                      <p className="text-sm text-muted-foreground">
                        {format(new Date(item.created_at), 'PPP p')}
                      </p>
                    </div>
                  </div>
                  <div className="flex items-center gap-2">
                    <Badge variant="secondary">{item.file_type}</Badge>
                    <a href={`${process.env.NEXT_PUBLIC_API_URL?.replace('/api', '') || 'http://localhost:5000'}/${item.file_path}`} download>
                      <Button variant="ghost" size="icon" title="Download Again">
                        <Download className="h-4 w-4" />
                      </Button>
                    </a>
                    <Button 
                      variant="ghost" 
                      size="icon" 
                      title="Delete" 
                      className="text-red-500 hover:text-red-600 hover:bg-red-50 dark:hover:bg-red-950"
                      onClick={() => {
                        if (window.confirm('Are you sure you want to delete this export?')) {
                          deleteMutation.mutate(item.id);
                        }
                      }}
                      disabled={deleteMutation.isPending}
                    >
                      <Trash className="h-4 w-4" />
                    </Button>
                  </div>
                </div>
              ))
            )}
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
