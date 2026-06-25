import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: '应用名称',
  description: '应用描述',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="zh-CN">
      <body className="antialiased">{children}</body>
    </html>
  )
}
