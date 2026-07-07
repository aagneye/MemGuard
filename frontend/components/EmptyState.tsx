interface Props {
  icon?: string;
  title: string;
  description?: string;
  hint?: string;
}

export default function EmptyState({ icon = "💬", title, description, hint }: Props) {
  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        textAlign: "center",
        padding: "32px 16px",
        gap: "8px",
        color: "#64748b",
      }}
    >
      <span style={{ fontSize: "36px" }}>{icon}</span>
      <strong style={{ color: "#94a3b8", fontSize: "15px" }}>{title}</strong>
      {description && <p style={{ margin: 0, fontSize: "13px", maxWidth: "300px" }}>{description}</p>}
      {hint && (
        <code
          style={{
            fontSize: "12px",
            background: "#0f172a",
            border: "1px solid #1e293b",
            borderRadius: "6px",
            padding: "6px 12px",
            color: "#7dd3fc",
            marginTop: "8px",
            display: "block",
            maxWidth: "400px",
          }}
        >
          {hint}
        </code>
      )}
    </div>
  );
}
