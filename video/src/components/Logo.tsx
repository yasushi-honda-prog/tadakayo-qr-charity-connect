import React from "react";
import { useCurrentFrame, spring, useVideoConfig, staticFile } from "remotion";

type Props = {
  showCharacter?: boolean;
  scale?: number;
};

export const Logo: React.FC<Props> = ({ showCharacter = false, scale = 1 }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Logo entrance animation with spring (no bounce)
  const logoSpring = spring({
    frame,
    fps,
    config: {
      damping: 200,
      stiffness: 100,
    },
  });

  // Character entrance animation (delayed, with bounce)
  const characterSpring = spring({
    frame: frame - 15,
    fps,
    config: {
      damping: 8,
      stiffness: 100,
    },
  });

  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        gap: 24,
        transform: `scale(${logoSpring * scale})`,
      }}
    >
      <img
        src={staticFile("tadakayo-logo.jpg")}
        alt="Tadakayo Logo"
        style={{
          width: 300,
          height: "auto",
          borderRadius: 16,
          boxShadow: "0 0 40px rgba(229, 45, 39, 0.4)",
        }}
      />
      {showCharacter && (
        <img
          src={staticFile("tadakayo-character.png")}
          alt="Tadakayo Character"
          style={{
            width: 200,
            height: "auto",
            transform: `scale(${Math.max(0, characterSpring)})`,
          }}
        />
      )}
    </div>
  );
};
