'use client';

import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarGroup,
  SidebarGroupContent,
  SidebarGroupLabel,
  SidebarHeader,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
} from "@/components/ui/sidebar"
import { LayoutDashboard, Search, History, Bookmark, Users, Activity, Map, Download, Bell, User, Settings, ShieldAlert, LifeBuoy } from "lucide-react"
import Link from "next/link"
import { usePathname } from "next/navigation"

const items = [
  {
    title: "Dashboard",
    url: "/dashboard",
    icon: LayoutDashboard,
  },
  {
    title: "New Search",
    url: "/search",
    icon: Search,
  },
  {
    title: "Search History",
    url: "/history",
    icon: History,
  },
  {
    title: "Saved Searches",
    url: "/saved",
    icon: Bookmark,
  },
  {
    title: "Businesses",
    url: "/businesses",
    icon: Users,
  },
  {
    title: "Lead Management",
    url: "/leads",
    icon: Activity,
  },
  {
    title: "Analytics",
    url: "/analytics",
    icon: Activity, // Use appropriate chart icon
  },
  {
    title: "Heatmap",
    url: "/heatmap",
    icon: Map,
  },
  {
    title: "Exports",
    url: "/exports",
    icon: Download,
  },
  {
    title: "Reminders",
    url: "/reminders",
    icon: Bell,
  },
]

const footerItems = [
  {
    title: "Profile",
    url: "/profile",
    icon: User,
  },
  {
    title: "Settings",
    url: "/settings",
    icon: Settings,
  },
  {
    title: "Admin Panel",
    url: "/admin",
    icon: ShieldAlert,
  },
  {
    title: "Help Center",
    url: "/help",
    icon: LifeBuoy,
  },
]

export function AppSidebar() {
  const pathname = usePathname()

  return (
    <Sidebar>
      <SidebarHeader className="h-16 flex items-center px-4">
        <h1 className="text-xl font-bold tracking-tight">LeadGen SaaS</h1>
      </SidebarHeader>
      <SidebarContent>
        <SidebarGroup>
          <SidebarGroupLabel>Application</SidebarGroupLabel>
          <SidebarGroupContent>
            <SidebarMenu>
              {items.map((item) => (
                <SidebarMenuItem key={item.title}>
                  <SidebarMenuButton 
                    isActive={pathname === item.url}
                    render={
                      <Link href={item.url} className="flex items-center gap-2">
                        <item.icon className="h-4 w-4" />
                        <span>{item.title}</span>
                      </Link>
                    }
                  />
                </SidebarMenuItem>
              ))}
            </SidebarMenu>
          </SidebarGroupContent>
        </SidebarGroup>
      </SidebarContent>
      <SidebarFooter>
        <SidebarMenu>
          {footerItems.map((item) => (
            <SidebarMenuItem key={item.title}>
              <SidebarMenuButton 
                isActive={pathname === item.url}
                render={
                  <Link href={item.url} className="flex items-center gap-2">
                    <item.icon className="h-4 w-4" />
                    <span>{item.title}</span>
                  </Link>
                }
              />
            </SidebarMenuItem>
          ))}
        </SidebarMenu>
      </SidebarFooter>
    </Sidebar>
  )
}
