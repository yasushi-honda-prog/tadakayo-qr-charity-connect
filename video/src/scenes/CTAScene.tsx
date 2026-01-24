import React from "react";
import {
  AbsoluteFill,
  useCurrentFrame,
  spring,
  useVideoConfig,
  interpolate,
  staticFile,
} from "remotion";
import { loadFont } from "@remotion/google-fonts/NotoSansJP";
import { theme } from "../styles/theme";

const { fontFamily } = loadFont();

export const CTAScene: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();

  // Main text entrance
  const textSpring = spring({
    frame,
    fps,
    config: {
      damping: 200,
      stiffness: 80,
    },
  });

  // Badge bounce
  const badgeSpring = spring({
    frame: frame - 15,
    fps,
    config: {
      damping: 8,
      stiffness: 100,
    },
  });

  // Logo entrance
  const logoSpring = spring({
    frame: frame - 30,
    fps,
    config: {
      damping: 200,
      stiffness: 80,
    },
  });

  // Fade out at the end
  const fadeOut = interpolate(
    frame,
    [durationInFrames - 20, durationInFrames],
    [1, 0],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
  );

  return (
    <AbsoluteFill
      style={{
        backgroundColor: theme.bgPrimary,
        fontFamily,
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        padding: 60,
        opacity: fadeOut,
      }}
    >
      {/* Main CTA text */}
      <div
        style={{
          opacity: textSpring,
          transform: `translateY(${(1 - textSpring) * 30}px)`,
          textAlign: "center",
        }}
      >
        <h1
          style={{
            fontSize: 56,
            fontWeight: 700,
            color: theme.textPrimary,
            margin: 0,
            lineHeight: 1.3,
          }}
        >
          最短
          <span style={{ color: theme.brand, fontSize: 72 }}>2</span>
          タップで
        </h1>
        <h2
          style={{
            fontSize: 64,
            fontWeight: 700,
            color: theme.brand,
            margin: 0,
            marginTop: 16,
          }}
        >
          支援完了
        </h2>
      </div>

      {/* Feature badge */}
      <div
        style={{
          marginTop: 48,
          transform: `scale(${Math.max(0, badgeSpring)})`,
        }}
      >
        <div
          style={{
            backgroundColor: theme.bgSecondary,
            border: `2px solid ${theme.brand}`,
            borderRadius: 12,
            padding: "16px 32px",
            display: "flex",
            alignItems: "center",
            gap: 16,
          }}
        >
          <span style={{ fontSize: 36 }}>✨</span>
          <span
            style={{
              fontSize: 28,
              fontWeight: 700,
              color: theme.textPrimary,
            }}
          >
            登録・ログイン不要
          </span>
        </div>
      </div>

      {/* Logo */}
      <div
        style={{
          marginTop: 64,
          opacity: logoSpring,
          transform: `scale(${logoSpring})`,
        }}
      >
        <img
          src={staticFile("tadakayo-logo.jpg")}
          alt="Tadakayo Logo"
          style={{
            width: 180,
            height: "auto",
            borderRadius: 12,
            boxShadow: theme.shadowGlow,
          }}
        />
      </div>
    </AbsoluteFill>
  );
};
