import React from "react";

interface SpinnerProps {
  size?: "sm" | "md" | "lg";
  label?: string;
}

export default function Spinner({ size = "md", label }: SpinnerProps) {
  const sizeMap = { sm: 16, md: 24, lg: 36 };
  const px = sizeMap[size];
  return (
    <span className="spinner-wrapper" role="status" aria-label={label ?? "Loading…"}>
      <svg
        width={px}
        height={px}
        viewBox="0 0 24 24"
        fill="none"
        className="spinner-svg"
      >
        <circle cx="12" cy="12" r="10" stroke="#e2e8f0" strokeWidth="3" />
        <path
          d="M12 2 A10 10 0 0 1 22 12"
          stroke="#6366f1"
          strokeWidth="3"
          strokeLinecap="round"
        />
      </svg>
      {label && <span className="spinner-label">{label}</span>}
    </span>
  );
}
