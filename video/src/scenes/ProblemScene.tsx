import React from "react";
import {
  AbsoluteFill,
  useCurrentFrame,
  spring,
  useVideoConfig,
  Sequence,
} from "remotion";
import { loadFont } from "@remotion/google-fonts/NotoSansJP";
import { theme } from "../styles/theme";
import { Typewriter } from "../components/Typewriter";

const { fontFamily } = loadFont();

export const ProblemScene: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Icon bounce animation
  const iconSpring = spring({
    frame,
    fps,
    config: {
      damping: 8,
      stiffness: 100,
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
      {/* Thinking/confused emoji */}
      <div
        style={{
          fontSize: 120,
          transform: `scale(${iconSpring})`,
          marginBottom: 48,
        }}
      >
        🤔
      </div>

      {/* First line */}
      <Sequence from={0} durationInFrames={60}>
        <div
          style={{
            fontSize: 42,
            color: theme.textPrimary,
            textAlign: "center",
            lineHeight: 1.4,
          }}
        >
          <Typewriter text="支援したいけど..." charFrames={3} />
        </div>
      </Sequence>

      {/* Second line */}
      <Sequence from={30} durationInFrames={60}>
        <div
          style={{
            fontSize: 48,
            fontWeight: 700,
            color: theme.brand,
            textAlign: "center",
            marginTop: 24,
          }}
        >
          <Typewriter text="手続きが面倒..." charFrames={3} />
        </div>
      </Sequence>
    </AbsoluteFill>
  );
};
