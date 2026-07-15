'use client';

import { useQuery } from '@tanstack/react-query';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Search, Building2, Bookmark, Download, Star, CheckCircle2, PhoneCall, Clock } from 'lucide-react';
import { api } from '@/services/api';
import { Skeleton } from '@/components/ui/skeleton';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

export default function DashboardPage() {
  const { data: stats, isLoading: statsLoading } = useQuery({
    queryKey: ['dashboard-stats'],
    queryFn: async () => {
      const res = await api.get('/dashboard/stats');
      return res.data;
    }
  });

  const { data: activityData, isLoading: activityLoading } = useQuery({
    queryKey: ['dashboard-activity'],
    queryFn: async () => {
      const res = await api.get('/dashboard/activity');
      return res.data;
    }
  });

  const { data: recentSearches, isLoading: recentSearchesLoading } = useQuery({
    queryKey: ['dashboard-recent-searches'],
    queryFn: async () => {
      const res = await api.get('/dashboard/recent-searches');
      return res.data;
    }
  });

  const isLoading = statsLoading || activityLoading || recentSearchesLoading;

  if (isLoading) {
    return (
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        {[1, 2, 3, 4, 5, 6, 7, 8].map((i) => (
          <Card key={i}>
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <Skeleton className="h-4 w-[100px]" />
              <Skeleton className="h-4 w-4" />
            </CardHeader>
            <CardContent>
              <Skeleton className="h-8 w-[60px]" />
            </CardContent>
          </Card>
        ))}
      </div>
    );
  }

  const statCards = [
    { title: "Today's Searches", value: stats?.today_searches || 0, icon: Search, color: "text-blue-500" },
    { title: "Total Searches", value: stats?.total_searches || 0, icon: Search, color: "text-blue-600" },
    { title: "Total Businesses", value: stats?.total_businesses || 0, icon: Building2, color: "text-purple-500" },
    { title: "Saved Leads", value: stats?.saved_leads || 0, icon: Bookmark, color: "text-emerald-500" },
    { title: "Avg AI Lead Score", value: `${stats?.avg_lead_score || 0}/100`, icon: Star, color: "text-yellow-500" },
    { title: "Verified Emails", value: stats?.verified_emails || 0, icon: CheckCircle2, color: "text-green-500" },
    { title: "Verified Phones", value: stats?.verified_phones || 0, icon: PhoneCall, color: "text-indigo-500" },
    { title: "Total Exports", value: stats?.exports || 0, icon: Download, color: "text-orange-500" },
  ];

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-3xl font-bold tracking-tight">Dashboard</h2>
        <p className="text-muted-foreground">Welcome back! Here's an overview of your lead generation activity.</p>
      </div>

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        {statCards.map((stat, i) => (
          <Card key={i} className="hover:shadow-md transition-shadow">
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <CardTitle className="text-sm font-medium text-muted-foreground">{stat.title}</CardTitle>
              <stat.icon className={`h-4 w-4 ${stat.color}`} />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{stat.value}</div>
            </CardContent>
          </Card>
        ))}
      </div>

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-7">
        <Card className="col-span-4 flex flex-col">
          <CardHeader>
            <CardTitle>Recent Activity Overview</CardTitle>
            <CardDescription>Your search activity over the last 7 days.</CardDescription>
          </CardHeader>
          <CardContent className="flex-1 min-h-[300px] h-[300px]">
            {activityData && activityData.length > 0 ? (
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={activityData} margin={{ top: 5, right: 20, bottom: 5, left: 0 }}>
                  <Line type="monotone" dataKey="searches" stroke="#3b82f6" strokeWidth={2} activeDot={{ r: 8 }} />
                  <CartesianGrid stroke="#ccc" strokeDasharray="5 5" opacity={0.3} />
                  <XAxis dataKey="name" axisLine={false} tickLine={false} tickMargin={10} fontSize={12} />
                  <YAxis axisLine={false} tickLine={false} tickMargin={10} fontSize={12} allowDecimals={false} />
                  <Tooltip contentStyle={{ borderRadius: '8px', border: '1px solid #e2e8f0' }} />
                </LineChart>
              </ResponsiveContainer>
            ) : (
              <div className="flex h-full items-center justify-center border-dashed border-2 rounded-md m-4">
                <p className="text-muted-foreground">No activity data available.</p>
              </div>
            )}
          </CardContent>
        </Card>
        <Card className="col-span-3">
          <CardHeader>
            <CardTitle>Recent Searches</CardTitle>
            <CardDescription>Your most recent lead generation searches.</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {recentSearches && recentSearches.length > 0 ? (
                recentSearches.map((search: any) => (
                    <div 
                      key={search.id} 
                      className="flex items-center justify-between border-b pb-4 last:border-0 last:pb-0 cursor-pointer hover:bg-muted/50 p-2 rounded-md transition-colors"
                      onClick={() => {
                        const params = new URLSearchParams();
                        if (search.search_params?.niche) params.append('niche', search.search_params.niche);
                        if (search.search_params?.city) params.append('city', search.search_params.city);
                        if (search.search_params?.country) params.append('country', search.search_params.country);
                        window.location.href = `/search?${params.toString()}`;
                      }}
                    >
                      <div className="flex items-center gap-3">
                        <div className="rounded-full bg-blue-100 p-2 dark:bg-blue-900/30">
                          <Clock className="h-4 w-4 text-blue-600 dark:text-blue-400" />
                        </div>
                        <div>
                          <p className="text-sm font-medium">
                            {search.search_params?.niche || 'Any'} in {search.search_params?.city || 'Any City'}
                          </p>
                          <p className="text-xs text-muted-foreground">
                            {new Date(search.created_at).toLocaleDateString()}
                          </p>
                        </div>
                      </div>
                    <div className="text-sm font-medium bg-secondary text-secondary-foreground px-2 py-1 rounded-md">
                      {search.results_count} results
                    </div>
                  </div>
                ))
              ) : (
                <div className="py-8 text-center text-sm text-muted-foreground">
                  No recent searches found.
                </div>
              )}
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
