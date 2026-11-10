interface NavbarProps {
  titulo: string
}

export function Navbar({ titulo }: NavbarProps) {
  return (
    <header className="bg-slate-900 text-white shadow">
      <div className="mx-auto flex max-w-6xl items-center justify-between px-4 py-4">
        <h1 className="text-xl font-bold tracking-tight">{titulo}</h1>
        <span className="rounded-full bg-slate-700 px-3 py-1 text-xs font-medium">
          Administración
        </span>
      </div>
    </header>
  )
}