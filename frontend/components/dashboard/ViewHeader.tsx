export function ViewHeader({ title, lede }: { title: string; lede: string }) {
  return (
    <header className="view-header">
      <h1 className="dash-view-title">{title}</h1>
      <p className="dash-view-lede">{lede}</p>
    </header>
  );
}
