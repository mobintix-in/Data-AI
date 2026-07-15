'use client';

import { useEffect, useState } from 'react';
import { MapContainer, TileLayer, CircleMarker, Popup, useMap } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import { useTheme } from 'next-themes';

interface LeadMarker {
  id: number;
  name: string;
  lat: number;
  lng: number;
  category: string;
}

// Map bounds updater component
function MapBounds({ leads }: { leads: LeadMarker[] }) {
  const map = useMap();
  
  useEffect(() => {
    if (leads.length > 0) {
      // Calculate bounds
      let minLat = 90, maxLat = -90, minLng = 180, maxLng = -180;
      leads.forEach(l => {
        if (l.lat < minLat) minLat = l.lat;
        if (l.lat > maxLat) maxLat = l.lat;
        if (l.lng < minLng) minLng = l.lng;
        if (l.lng > maxLng) maxLng = l.lng;
      });
      
      // Pad bounds slightly
      map.fitBounds([
        [minLat - 0.5, minLng - 0.5],
        [maxLat + 0.5, maxLng + 0.5]
      ]);
    }
  }, [leads, map]);

  return null;
}

export default function HeatmapComponent({ leads }: { leads: LeadMarker[] }) {
  const { theme } = useTheme();
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  if (!mounted) return null;

  // Dark mode tile layer vs Light mode tile layer
  const tileUrl = theme === 'dark' 
    ? 'https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png'
    : 'https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png';

  const defaultCenter: [number, number] = [39.8283, -98.5795]; // US Center

  return (
    <div style={{ height: '100%', width: '100%', zIndex: 0, position: 'relative' }}>
      <MapContainer 
        center={defaultCenter} 
        zoom={4} 
        style={{ height: '100%', width: '100%', zIndex: 10 }}
      >
        <TileLayer
          attribution='&copy; <a href="https://carto.com/">CARTO</a>'
          url={tileUrl}
        />
        
        {leads.map((lead) => (
          <CircleMarker
            key={lead.id}
            center={[lead.lat, lead.lng]}
            radius={8}
            pathOptions={{ 
              color: 'hsl(var(--primary))', 
              fillColor: 'hsl(var(--primary))',
              fillOpacity: 0.5,
              weight: 0
            }}
          >
            <Popup>
              <div className="font-sans">
                <strong className="block text-base mb-1">{lead.name}</strong>
                <span className="text-sm text-gray-500">{lead.category}</span>
                <a 
                  href={`https://www.google.com/search?tbm=isch&q=${encodeURIComponent(lead.name + ' ' + lead.category)}`}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="mt-2 inline-flex items-center justify-center whitespace-nowrap rounded-md text-xs font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 bg-primary text-primary-foreground hover:bg-primary/90 h-8 px-3 py-2 w-full mt-3"
                >
                  View Photos
                </a>
              </div>
            </Popup>
          </CircleMarker>
        ))}

        <MapBounds leads={leads} />
      </MapContainer>
    </div>
  );
}
