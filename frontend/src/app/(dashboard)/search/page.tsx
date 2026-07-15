"use client";

import { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";
import dynamic from 'next/dynamic';
import { Skeleton } from '@/components/ui/skeleton';
import { MapPin, List } from 'lucide-react';

const HeatmapComponent = dynamic(
  () => import('../heatmap/HeatmapComponent'),
  { 
    ssr: false,
    loading: () => <Skeleton className="w-full h-[600px] rounded-md" />
  }
);

export default function SearchPage() {
  const [country, setCountry] = useState("");
  const [city, setCity] = useState("");
  const [niche, setNiche] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [results, setResults] = useState<any[]>([]);
  const [downloadUrl, setDownloadUrl] = useState("");
  const [showMap, setShowMap] = useState(false);

  useEffect(() => {
    if (typeof window !== 'undefined') {
      const params = new URLSearchParams(window.location.search);
      if (params.get('country')) setCountry(params.get('country') as string);
      if (params.get('city')) setCity(params.get('city') as string);
      if (params.get('niche')) setNiche(params.get('niche') as string);
    }
  }, []);

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    setResults([]);
    setDownloadUrl("");
    
    try {
      const formData = new FormData();
      formData.append("country", country);
      formData.append("city", city);
      formData.append("niche", niche);

      const token = localStorage.getItem("access_token");
      const response = await fetch("http://127.0.0.1:5000/api/search", {
        method: "POST",
        headers: {
          Authorization: `Bearer ${token}`,
        },
        body: formData,
      });
      
      const data = await response.json();
      
      if (response.ok) {
        setResults(data.leads || []);
        if (data.download_url) {
          setDownloadUrl(`http://127.0.0.1:5000${data.download_url}`);
        }
      } else {
        const errorDetail = Array.isArray(data.detail) ? data.detail[0]?.msg : (data.detail || data.message || 'Unknown error');
        setError(errorDetail);
      }
    } catch (error) {
      console.error(error);
      setError("Could not connect to the API. Make sure the backend is running.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-3xl font-bold tracking-tight">New Search</h2>
        <p className="text-muted-foreground">Search for businesses and discover leads.</p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Search Parameters</CardTitle>
          <CardDescription>Enter the niche, city, and country to find leads.</CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSearch} className="space-y-4">
            <div className="grid grid-cols-1 gap-4 md:grid-cols-3">
              <div className="space-y-2">
                <Label htmlFor="niche">Niche</Label>
                <Input 
                  id="niche" 
                  required 
                  placeholder="e.g. Plumbers" 
                  value={niche}
                  onChange={(e) => setNiche(e.target.value)}
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="city">City</Label>
                <Input 
                  id="city" 
                  required 
                  placeholder="e.g. New York" 
                  value={city}
                  onChange={(e) => setCity(e.target.value)}
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="country">Country</Label>
                <Input 
                  id="country" 
                  required 
                  placeholder="e.g. USA" 
                  value={country}
                  onChange={(e) => setCountry(e.target.value)}
                />
              </div>
            </div>
            <Button type="submit" disabled={loading}>
              {loading ? "Searching..." : "Search"}
            </Button>
            {error && <p className="text-sm text-red-500 font-medium mt-2">{error}</p>}
          </form>
        </CardContent>
      </Card>

      {results.length > 0 && (
        <Card>
          <CardHeader className="flex flex-row items-center justify-between">
            <CardTitle>Results ({results.length})</CardTitle>
            <div className="flex gap-2">
              <Button variant="outline" onClick={() => setShowMap(!showMap)}>
                {showMap ? <><List className="mr-2 h-4 w-4" /> View List</> : <><MapPin className="mr-2 h-4 w-4" /> View Map</>}
              </Button>
              {downloadUrl && (
                <Button variant="outline" onClick={() => {
                  const a = document.createElement('a');
                  a.href = downloadUrl;
                  a.download = 'search_results.xlsx';
                  document.body.appendChild(a);
                  a.click();
                  document.body.removeChild(a);
                }}>
                  Download Excel
                </Button>
              )}
            </div>
          </CardHeader>
          <CardContent>
            {showMap ? (
              <div className="h-[600px] w-full rounded-md overflow-hidden border">
                <HeatmapComponent leads={results.filter(r => r.lat && r.lng).map((r, i) => ({
                  id: r.id || i,
                  name: r.name,
                  lat: parseFloat(r.lat),
                  lng: parseFloat(r.lng),
                  category: niche
                }))} />
              </div>
            ) : (
              <Table>
                <TableHeader>
                <TableRow>
                  <TableHead>Name</TableHead>
                  <TableHead>Email</TableHead>
                  <TableHead>Phone</TableHead>
                  <TableHead>Score</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {results.map((lead, i) => (
                  <TableRow key={i}>
                    <TableCell className="font-medium">{lead.name}</TableCell>
                    <TableCell>{lead.email || "-"}</TableCell>
                    <TableCell>{lead.phone || "-"}</TableCell>
                    <TableCell>
                      <Badge variant={lead.score_color === "High" ? "default" : lead.score_color === "Medium" ? "secondary" : "outline"}>
                        {lead.lead_score || 0}
                      </Badge>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
            )}
          </CardContent>
        </Card>
      )}
    </div>
  );
}
