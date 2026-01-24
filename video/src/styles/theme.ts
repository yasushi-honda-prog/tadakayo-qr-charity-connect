export const theme = {
  // Brand colors (from GitHub Pages design)
  brand: "#E52D27",
  brandDark: "#c41e1a",
  brandGlow: "rgba(229, 45, 39, 0.3)",

  // Background
  bgPrimary: "#0d1117",
  bgSecondary: "#161b22",

  // Text
  textPrimary: "#e6edf3",
  textSecondary: "#8b949e",

  // Accent
  accentGreen: "#3fb950",
  accentBlue: "#58a6ff",

  // Shadows
  shadowGlow: "0 0 30px rgba(229, 45, 39, 0.3)",
} as const;

export type Theme = typeof theme;
