import './globals.css'
import type { Metadata } from 'next'
import { Noto_Sans } from 'next/font/google'

const noto = Noto_Sans({ weight: "400", subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'isolated-python',
  description: 'Run some untrusted Python code.',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <head>
        <link rel="icon" href="/favicon.ico" sizes="any" />
      </head>
      <body className={noto.className}>{children}</body>
    </html>
  )
}
