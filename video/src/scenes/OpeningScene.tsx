import React from "react";
import { AbsoluteFill, useCurrentFrame, spring, useVideoConfig } from "remotion";
import { loadFont } from "@remotion/google-fonts/NotoSansJP";
import { theme } from "../styles/theme";
import { Logo } from "../components/Logo";

const { fontFamily } = loadFont();

export const OpeningScene: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Title entrance with spring (no bounce)
  const titleSpring = spring({
    frame: frame - 30,
    fps,
    config: {
      damping: 200,
      stiffness: 80,
    },
  });

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
      }}
    >
      <Logo showCharacter={true} scale={1} />

      <div
        style={{
          marginTop: 48,
          opacity: titleSpring,
          transform: `translateY(${(1 - titleSpring) * 20}px)`,
        }}
      >
        <h1
          style={{
            fontSize: 56,
            fontWeight: 700,
            color: theme.textPrimary,
            textAlign: "center",
            margin: 0,
          }}
        >
          QRチャリティ
        </h1>
        <h2
          style={{
            fontSize: 48,
            fontWeight: 700,
            color: theme.brand,
            textAlign: "center",
            margin: 0,
            marginTop: 8,
          }}
        >
          コネクト
        </h2>
      </div>
    </AbsoluteFill>
  );
};
