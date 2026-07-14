import { AppSidebar } from "@/components/layout/AppSidebar"
import { TopNavbar } from "@/components/layout/TopNavbar"
import { SidebarProvider } from "@/components/ui/sidebar"

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <SidebarProvider>
      <div className="flex min-h-screen w-full">
        <AppSidebar />
        <div className="flex w-full flex-col">
          <TopNavbar />
          <main className="flex-1 p-6 overflow-y-auto bg-muted/20">
            {children}
          </main>
        </div>
      </div>
    </SidebarProvider>
  )
}
