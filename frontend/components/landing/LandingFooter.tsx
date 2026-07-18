export default function LandingFooter() {
  return (
    <footer className="lp-footer">
      <div>
        <strong>MemGuard</strong>
        <p className="muted">Trust-aware memory agent · MIT License</p>
      </div>
      <div className="lp-footer__links">
        <a href="https://github.com/aagneye/MemGuard/blob/master/docs/SETUP.md" target="_blank" rel="noopener noreferrer">
          Docs
        </a>
        <a href="https://github.com/aagneye/MemGuard" target="_blank" rel="noopener noreferrer">
          GitHub
        </a>
        <a href="/demo">Demo</a>
      </div>
    </footer>
  );
}
