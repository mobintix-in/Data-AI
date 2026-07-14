'use client';

import { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle, CardFooter } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { useAuth } from '@/contexts/AuthContext';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import { User, Key, Shield, Loader2 } from 'lucide-react';
import { Separator } from '@/components/ui/separator';
import { api } from '@/services/api';

export default function SettingsPage() {
  const { user, updateUser } = useAuth();
  
  const [firstName, setFirstName] = useState('');
  const [lastName, setLastName] = useState('');
  const [email, setEmail] = useState('');
  const [geminiKey, setGeminiKey] = useState('');
  
  const [isSavingProfile, setIsSavingProfile] = useState(false);
  const [isSavingKey, setIsSavingKey] = useState(false);

  useEffect(() => {
    if (user) {
      setFirstName(user.first_name || '');
      setLastName(user.last_name || '');
      setEmail(user.email || '');
      setGeminiKey(user.gemini_api_key || '');
    }
  }, [user]);

  const handleSaveProfile = async () => {
    setIsSavingProfile(true);
    try {
      const response = await api.put('/auth/me', {
        first_name: firstName,
        last_name: lastName
      });
      updateUser(response.data);
      alert('Profile updated successfully');
    } catch (error) {
      console.error('Failed to save profile:', error);
      alert('Failed to update profile');
    } finally {
      setIsSavingProfile(false);
    }
  };

  const handleSaveKeys = async () => {
    setIsSavingKey(true);
    try {
      const response = await api.put('/auth/me', {
        gemini_api_key: geminiKey
      });
      updateUser(response.data);
      alert('API keys updated successfully');
    } catch (error) {
      console.error('Failed to save API keys:', error);
      alert('Failed to update API keys');
    } finally {
      setIsSavingKey(false);
    }
  };

  return (
    <div className="space-y-6 max-w-4xl mx-auto">
      <div>
        <h2 className="text-3xl font-bold tracking-tight">Settings</h2>
        <p className="text-muted-foreground">Manage your account settings and preferences.</p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2"><User className="w-5 h-5" /> Profile Information</CardTitle>
          <CardDescription>Update your account's profile information and email address.</CardDescription>
        </CardHeader>
        <CardContent className="space-y-6">
          <div className="flex items-center gap-6">
            <Avatar className="h-24 w-24">
              <AvatarImage src={user?.profile_image} />
              <AvatarFallback className="text-2xl">{user?.first_name?.charAt(0)}</AvatarFallback>
            </Avatar>
            <Button variant="outline">Change Avatar</Button>
          </div>
          <Separator />
          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label htmlFor="firstName">First Name</Label>
              <Input 
                id="firstName" 
                value={firstName} 
                onChange={(e) => setFirstName(e.target.value)} 
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="lastName">Last Name</Label>
              <Input 
                id="lastName" 
                value={lastName} 
                onChange={(e) => setLastName(e.target.value)} 
              />
            </div>
            <div className="space-y-2 col-span-2">
              <Label htmlFor="email">Email</Label>
              <Input 
                id="email" 
                type="email" 
                value={email} 
                disabled 
              />
              <p className="text-xs text-muted-foreground">Contact support to change your email address.</p>
            </div>
          </div>
        </CardContent>
        <CardFooter className="flex justify-end">
          <Button onClick={handleSaveProfile} disabled={isSavingProfile}>
            {isSavingProfile ? <Loader2 className="w-4 h-4 mr-2 animate-spin" /> : null}
            Save Changes
          </Button>
        </CardFooter>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2"><Key className="w-5 h-5" /> API Keys</CardTitle>
          <CardDescription>Manage your API keys for external integrations.</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="geminiKey">Google Gemini API Key</Label>
            <Input 
              id="geminiKey" 
              type="password" 
              placeholder="AIzaSy..." 
              value={geminiKey}
              onChange={(e) => setGeminiKey(e.target.value)}
            />
            <p className="text-xs text-muted-foreground">Used for generating AI summaries and scoring leads.</p>
          </div>
        </CardContent>
        <CardFooter className="flex justify-end">
          <Button onClick={handleSaveKeys} disabled={isSavingKey}>
            {isSavingKey ? <Loader2 className="w-4 h-4 mr-2 animate-spin" /> : null}
            Save Keys
          </Button>
        </CardFooter>
      </Card>
      
      {user?.role === 'ADMIN' && (
        <Card className="border-red-200 dark:border-red-900 bg-red-50/50 dark:bg-red-900/10">
          <CardHeader>
            <CardTitle className="flex items-center gap-2 text-red-600 dark:text-red-400"><Shield className="w-5 h-5" /> Admin Zone</CardTitle>
            <CardDescription>You have administrator privileges.</CardDescription>
          </CardHeader>
          <CardContent>
            <a href="/admin">
              <Button variant="destructive">
                Go to Admin Panel
              </Button>
            </a>
          </CardContent>
        </Card>
      )}
    </div>
  );
}
