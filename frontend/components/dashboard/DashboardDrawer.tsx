import { DRAWER_ITEMS, DrawerId } from "./drawerItems";

type Props = {
  active: DrawerId;
  onSelect: (id: DrawerId) => void;
  open: boolean;
  onClose: () => void;
};

export default function DashboardDrawer({ active, onSelect, open, onClose }: Props) {
  return (
    <>
      <div
        className={`dash-drawer-backdrop${open ? " is-open" : ""}`}
        onClick={onClose}
        aria-hidden={!open}
      />
      <aside className={`dash-drawer${open ? " is-open" : ""}`} aria-label="Dashboard navigation">
        <p className="dash-drawer__label">Workspace</p>
        <nav>
          <ul className="dash-drawer__list">
            {DRAWER_ITEMS.map((item) => (
              <li key={item.id}>
                <button
                  type="button"
                  className={`dash-drawer__item${active === item.id ? " is-active" : ""}`}
                  onClick={() => {
                    onSelect(item.id);
                    onClose();
                  }}
                >
                  <span className="dash-drawer__item-label">{item.label}</span>
                  <span className="dash-drawer__item-hint">{item.hint}</span>
                </button>
              </li>
            ))}
          </ul>
        </nav>
      </aside>
    </>
  );
}
