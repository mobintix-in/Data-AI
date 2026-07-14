import { useState } from "react";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import {
  Sheet,
  SheetContent,
  SheetDescription,
  SheetHeader,
  SheetTitle,
} from "@/components/ui/sheet";
import { Badge } from "@/components/ui/badge";
import { Separator } from "@/components/ui/separator";
import { Button } from "@/components/ui/button";
import { Loader2, Sparkles } from "lucide-react";
import api from "@/lib/axios";
import { BusinessLead } from "./columns";

interface BusinessDrawerProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  lead: BusinessLead | null;
}

export function BusinessDrawer({ open, onOpenChange, lead }: BusinessDrawerProps) {
  const queryClient = useQueryClient();
  const [localSummary, setLocalSummary] = useState<string | null>(null);

  const generateSummary = useMutation({
    mutationFn: async () => {
      const res = await api.post(`/ai/generate-summary/${lead?.id}`);
      return res.data;
    },
    onSuccess: (data) => {
      setLocalSummary(data.summary);
      queryClient.invalidateQueries({ queryKey: ['businesses'] });
    }
  });

  if (!lead) return null;

  // Wait for the local state update or use the actual lead property
  const displaySummary = localSummary || (lead as any).ai_summary;

  return (
    <Sheet open={open} onOpenChange={(isOpen) => {
      onOpenChange(isOpen);
      if (!isOpen) setLocalSummary(null);
    }}>
      <SheetContent className="sm:max-w-xl w-full overflow-y-auto">
        <SheetHeader>
          <SheetTitle className="text-2xl">{lead.name}</SheetTitle>
          <SheetDescription>
            {lead.category} • Scraped on {new Date(lead.created_at).toLocaleDateString()}
          </SheetDescription>
        </SheetHeader>
        
        <div className="py-6 space-y-6">
          <div className="flex items-center gap-4">
            <Badge variant={lead.lead_score > 75 ? "default" : lead.lead_score >= 50 ? "secondary" : "destructive"} className="text-lg px-3 py-1">
              Score: {lead.lead_score}/100
            </Badge>
            <Badge variant="outline" className="text-lg px-3 py-1">
              {lead.lead_status}
            </Badge>
          </div>

          <Separator />

          <div>
            <h3 className="font-semibold text-lg mb-2">Contact Information</h3>
            <div className="grid grid-cols-2 gap-4 text-sm">
              <div>
                <p className="text-muted-foreground">Email</p>
                <p className="font-medium">{lead.email || "N/A"}</p>
              </div>
              <div>
                <p className="text-muted-foreground">Phone</p>
                <p className="font-medium">{lead.phone || "N/A"}</p>
              </div>
            </div>
          </div>

          <Separator />
          
          <div>
            <h3 className="font-semibold text-lg mb-2 flex items-center gap-2">
              <Sparkles className="h-4 w-4 text-primary" />
              AI Summary
            </h3>
            <div className="bg-muted p-4 rounded-md text-sm min-h-[100px] flex flex-col justify-center">
              {displaySummary ? (
                <p className="leading-relaxed">{displaySummary}</p>
              ) : (
                <div className="text-center space-y-3">
                  <p className="text-muted-foreground">AI Summary not generated yet.</p>
                  <Button 
                    variant="outline" 
                    size="sm" 
                    onClick={() => generateSummary.mutate()}
                    disabled={generateSummary.isPending}
                  >
                    {generateSummary.isPending ? (
                      <><Loader2 className="mr-2 h-4 w-4 animate-spin" /> Generating...</>
                    ) : (
                      <><Sparkles className="mr-2 h-4 w-4" /> Generate using Gemini</>
                    )}
                  </Button>
                </div>
              )}
            </div>
          </div>

          <Separator />
          
          <div>
            <h3 className="font-semibold text-lg mb-2">Timeline</h3>
            <p className="text-sm text-muted-foreground italic">No interactions recorded.</p>
          </div>
        </div>
      </SheetContent>
    </Sheet>
  );
}
