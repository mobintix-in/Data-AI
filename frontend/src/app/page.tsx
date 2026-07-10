"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { api } from "@/services/api";

export default function Home() {
  const [country, setCountry] = useState("");
  const [city, setCity] = useState("");
  const [niche, setNiche] = useState("");
  const [status, setStatus] = useState("");
  const [loading, setLoading] = useState(false);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [user, setUser] = useState<any>(null);
  const [isLoading, setIsLoading] = useState(true);
  const router = useRouter();

  useEffect(() => {
    const checkAuth = async () => {
      try {
        const res = await api.get("/auth/me");
        setUser(res.data);
        setIsAuthenticated(true);
      } catch (err) {
        router.push("/login");
      } finally {
        setIsLoading(false);
      }
    };
    checkAuth();
  }, [router]);

  const logout = () => {
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    router.push("/login");
  };

  const token = typeof window !== "undefined" ? localStorage.getItem("access_token") : null;

  if (isLoading || !isAuthenticated) {
    return <div className="min-h-screen flex items-center justify-center dark:bg-zinc-900"><p className="text-white">Loading...</p></div>;
  }

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setStatus("Searching... This may take a while depending on the niche size.");
    
    try {
      const formData = new FormData();
      formData.append("country", country);
      formData.append("city", city);
      formData.append("niche", niche);

      const response = await fetch("http://127.0.0.1:5000/search", {
        method: "POST",
        headers: {
          Authorization: `Bearer ${token}`,
        },
        body: formData,
      });
      
      let data;
      try {
        data = await response.json();
      } catch (parseError) {
        data = { message: "An unexpected server error occurred (or the request timed out). Check backend logs for more details." };
      }
      
      if (response.ok) {
        if (data.download_url) {
          const a = document.createElement("a");
          a.href = "http://127.0.0.1:5000" + data.download_url;
          a.download = "search_results.xlsx";
          document.body.appendChild(a);
          a.click();
          document.body.removeChild(a);
          setStatus(`Success: ${data.message} Excel file is downloading.`);
        } else {
          setStatus(`Success: ${data.message}`);
        }
      } else {
        const errorDetail = Array.isArray(data.detail) ? data.detail[0]?.msg : (data.detail || data.message || 'Unknown error');
        setStatus(`Error: ${errorDetail}`);
      }
    } catch (error) {
      console.error(error);
      setStatus("Error: Could not connect to the API. Make sure the backend is running.");
    } finally {
      setLoading(false);
    }
  };

  const handleDownload = async () => {
    try {
      const res = await fetch("http://127.0.0.1:5000/download", {
        headers: {
          Authorization: `Bearer ${token}`
        }
      });
      if (res.ok) {
        const blob = await res.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = "search_results.xlsx";
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
      } else {
        alert("Failed to download file");
      }
    } catch (err) {
      console.error(err);
      alert("An error occurred while downloading");
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-zinc-900 py-12 px-4 sm:px-6 lg:px-8 font-sans">
      <div className="max-w-md mx-auto bg-white dark:bg-zinc-800 rounded-xl shadow-md overflow-hidden md:max-w-2xl p-8">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Lead Scraper</h1>
          <p className="mt-2 text-gray-600 dark:text-gray-400">Search for businesses and export leads to Excel.</p>
        </div>
        
        <div className="flex justify-between items-center mb-6 text-sm text-gray-600 dark:text-gray-300">
          <span>Welcome, {user?.email}</span>
          <div className="space-x-4">
            <button onClick={() => router.push("/profile")} className="text-indigo-600 hover:text-indigo-500 dark:text-indigo-400">Profile</button>
            <button onClick={logout} className="text-indigo-600 hover:text-indigo-500 dark:text-indigo-400">Logout</button>
          </div>
        </div>
        
        <form onSubmit={handleSearch} className="space-y-6">
          <div>
            <label htmlFor="country" className="block text-sm font-medium text-gray-700 dark:text-gray-300">Country</label>
            <input 
              type="text" 
              id="country" 
              required
              value={country}
              onChange={(e) => setCountry(e.target.value)}
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm p-2 border dark:bg-zinc-700 dark:border-zinc-600 dark:text-white"
              placeholder="e.g. USA"
            />
          </div>
          
          <div>
            <label htmlFor="city" className="block text-sm font-medium text-gray-700 dark:text-gray-300">City</label>
            <input 
              type="text" 
              id="city" 
              required
              value={city}
              onChange={(e) => setCity(e.target.value)}
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm p-2 border dark:bg-zinc-700 dark:border-zinc-600 dark:text-white"
              placeholder="e.g. New York"
            />
          </div>
          
          <div>
            <label htmlFor="niche" className="block text-sm font-medium text-gray-700 dark:text-gray-300">Niche</label>
            <input 
              type="text" 
              id="niche" 
              required
              value={niche}
              onChange={(e) => setNiche(e.target.value)}
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm p-2 border dark:bg-zinc-700 dark:border-zinc-600 dark:text-white"
              placeholder="e.g. Plumbers"
            />
          </div>
          
          <button 
            type="submit" 
            disabled={loading}
            className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            {loading ? 'Scraping...' : 'Start Search'}
          </button>
        </form>

        {status && (
          <div className={`mt-6 p-4 rounded-md ${status.startsWith('Error') ? 'bg-red-50 text-red-800 dark:bg-red-900/30 dark:text-red-300' : 'bg-blue-50 text-blue-800 dark:bg-blue-900/30 dark:text-blue-300'}`}>
            <p className="text-sm font-medium">{status}</p>
          </div>
        )}

        <div className="mt-8 pt-6 border-t border-gray-200 dark:border-zinc-700">
          <h2 className="text-lg font-medium text-gray-900 dark:text-white mb-4">Export Results</h2>
          <button 
            onClick={handleDownload}
            className="w-full flex justify-center py-2 px-4 border border-gray-300 dark:border-zinc-600 rounded-md shadow-sm text-sm font-medium text-gray-700 dark:text-gray-300 bg-white dark:bg-zinc-800 hover:bg-gray-50 dark:hover:bg-zinc-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition-colors"
          >
            Download Excel File
          </button>
        </div>
      </div>
    </div>
  );
}
