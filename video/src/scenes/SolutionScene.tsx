import React from "react";
import {
  AbsoluteFill,
  useCurrentFrame,
  spring,
  useVideoConfig,
  Sequence,
  interpolate,
} from "remotion";
import { loadFont } from "@remotion/google-fonts/NotoSansJP";
import { theme } from "../styles/theme";
import { Typewriter } from "../components/Typewriter";

const { fontFamily } = loadFont();

// Fixed QR-like pattern (7x7 = 49 cells)
// true = filled (dark), false = empty (white)
const QR_PATTERN = [
  // Row 1: Position detection pattern (top-left corner)
  true, true, true, false, true, true, true,
  // Row 2
  true, false, true, false, true, false, true,
  // Row 3
  true, true, true, false, true, true, true,
  // Row 4: Timing pattern
  false, false, false, false, false, false, false,
  // Row 5
  true, true, true, false, true, false, true,
  // Row 6
  true, false, true, false, false, true, false,
  // Row 7
  true, true, true, false, true, true, true,
];

export const SolutionScene: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // QR code bounce animation
  const qrSpring = spring({
    frame,
    fps,
    config: {
      damping: 8,
      stiffness: 100,
    },
  });

  // Glow pulse animation
  const glowOpacity = interpolate(
    frame % 60,
    [0, 30, 60],
    [0.3, 0.7, 0.3],
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
      }}
    >
      {/* QR Code placeholder with glow */}
      <div
        style={{
          transform: `scale(${qrSpring})`,
          marginBottom: 48,
          position: "relative",
        }}
      >
        <div
          style={{
            position: "absolute",
            inset: -20,
            borderRadius: 24,
            background: theme.brand,
            opacity: glowOpacity,
            filter: "blur(20px)",
          }}
        />
        <div
          style={{
            width: 280,
            height: 280,
            backgroundColor: "white",
            borderRadius: 16,
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            position: "relative",
            border: `4px solid ${theme.brand}`,
          }}
        >
          {/* Simple QR pattern - fixed pattern for consistent rendering */}
          <div
            style={{
              width: 200,
              height: 200,
              display: "grid",
              gridTemplateColumns: "repeat(7, 1fr)",
              gridTemplateRows: "repeat(7, 1fr)",
              gap: 4,
            }}
          >
            {QR_PATTERN.map((filled, i) => (
              <div
                key={i}
                style={{
                  backgroundColor: filled ? theme.bgPrimary : "transparent",
                  borderRadius: 2,
                }}
              />
            ))}
          </div>
        </div>
      </div>

      {/* Main message */}
      <Sequence from={15} durationInFrames={105}>
        <div
          style={{
            fontSize: 52,
            fontWeight: 700,
            color: theme.textPrimary,
            textAlign: "center",
            lineHeight: 1.4,
          }}
        >
          <Typewriter text="スキャンするだけ!" charFrames={2} showCursor={false} />
        </div>
      </Sequence>

      {/* Payment icons */}
      <Sequence from={45} durationInFrames={75}>
        <div
          style={{
            display: "flex",
            gap: 32,
            marginTop: 32,
          }}
        >
          <PaymentBadge name="PayPay" color="#FF0033" delay={0} />
          <PaymentBadge name="楽天ペイ" color="#BF0000" delay={10} />
        </div>
      </Sequence>
    </AbsoluteFill>
  );
};

const PaymentBadge: React.FC<{ name: string; color: string; delay: number }> = ({
  name,
  color,
  delay,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const badgeSpring = spring({
    frame: frame - delay,
    fps,
    config: {
      damping: 8,
      stiffness: 100,
    },
  });

  return (
    <div
      style={{
        backgroundColor: color,
        color: "white",
        padding: "12px 24px",
        borderRadius: 8,
        fontSize: 28,
        fontWeight: 700,
        transform: `scale(${Math.max(0, badgeSpring)})`,
      }}
    >
      {name}
    </div>
  );
};
