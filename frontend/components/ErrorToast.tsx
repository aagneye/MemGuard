"use client";
import React, { useEffect, useState } from "react";

interface ErrorToastProps {
  message: string | null;
  onDismiss: () => void;
  durationMs?: number;
}

export default function ErrorToast({ message, onDismiss, durationMs = 4000 }: ErrorToastProps) {
  const [visible, setVisible] = useState(false);

  useEffect(() => {
    if (message) {
      setVisible(true);
      const t = setTimeout(() => {
        setVisible(false);
        setTimeout(onDismiss, 300);
      }, durationMs);
      return () => clearTimeout(t);
    }
  }, [message, durationMs, onDismiss]);

  if (!message) return null;

  return (
    <div
      className={`error-toast ${visible ? "error-toast--visible" : "error-toast--hidden"}`}
      role="alert"
      aria-live="assertive"
    >
      <span className="error-toast__icon">⚠</span>
      <span className="error-toast__message">{message}</span>
      <button className="error-toast__close" onClick={onDismiss} aria-label="Dismiss">
        ×
      </button>
    </div>
  );
}
