import React from "react";
import {
  AbsoluteFill,
  useCurrentFrame,
  spring,
  useVideoConfig,
  interpolate,
  Sequence,
  staticFile,
} from "remotion";
import { loadFont } from "@remotion/google-fonts/NotoSansJP";
import { theme } from "./styles/theme";
import { Typewriter } from "./components/Typewriter";

const { fontFamily } = loadFont();

// Fixed QR-like pattern (7x7 = 49 cells)
const QR_PATTERN = [
  true, true, true, false, true, true, true,
  true, false, true, false, true, false, true,
  true, true, true, false, true, true, true,
  false, false, false, false, false, false, false,
  true, true, true, false, true, false, true,
  true, false, true, false, false, true, false,
  true, true, true, false, true, true, true,
];

export const HorizontalVideo: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();

  // Animation phases
  const logoSpring = spring({
    frame,
    fps,
    config: { damping: 200, stiffness: 100 },
  });

  const textSpring = spring({
    frame: frame - 20,
    fps,
    config: { damping: 200, stiffness: 80 },
  });

  const qrSpring = spring({
    frame: frame - 40,
    fps,
    config: { damping: 8, stiffness: 100 },
  });

  const badgeSpring = spring({
    frame: frame - 60,
    fps,
    config: { damping: 8, stiffness: 100 },
  });

  // Glow pulse
  const glowOpacity = interpolate(
    frame % 60,
    [0, 30, 60],
    [0.3, 0.6, 0.3],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
  );

  // Fade out at end
  const fadeOut = interpolate(
    frame,
    [durationInFrames - 30, durationInFrames],
    [1, 0],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
  );

  return (
    <AbsoluteFill
      style={{
        backgroundColor: theme.bgPrimary,
        fontFamily,
        opacity: fadeOut,
      }}
    >
      {/* Main horizontal layout */}
      <div
        style={{
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          height: "100%",
          padding: "60px 80px",
          gap: 80,
        }}
      >
        {/* Left: Logo and text */}
        <div
          style={{
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            flex: 1,
          }}
        >
          {/* Logo */}
          <div
            style={{
              transform: `scale(${logoSpring})`,
              marginBottom: 32,
            }}
          >
            <img
              src={staticFile("tadakayo-logo.jpg")}
              alt="Tadakayo Logo"
              style={{
                width: 200,
                height: "auto",
                borderRadius: 16,
                boxShadow: theme.shadowGlow,
              }}
            />
          </div>

          {/* Title */}
          <div
            style={{
              opacity: textSpring,
              transform: `translateY(${(1 - textSpring) * 20}px)`,
              textAlign: "center",
            }}
          >
            <h1
              style={{
                fontSize: 64,
                fontWeight: 700,
                color: theme.textPrimary,
                margin: 0,
                lineHeight: 1.2,
              }}
            >
              QRチャリティ
            </h1>
            <h2
              style={{
                fontSize: 56,
                fontWeight: 700,
                color: theme.brand,
                margin: 0,
                marginTop: 8,
              }}
            >
              コネクト
            </h2>
          </div>

          {/* Tagline */}
          <Sequence from={80} durationInFrames={280}>
            <div
              style={{
                marginTop: 32,
                fontSize: 32,
                color: theme.textSecondary,
                textAlign: "center",
              }}
            >
              <Typewriter text="最短2タップで支援完了" charFrames={3} showCursor={false} />
            </div>
          </Sequence>
        </div>

        {/* Right: QR Code */}
        <div
          style={{
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            flex: 1,
          }}
        >
          {/* QR Code with glow */}
          <div
            style={{
              transform: `scale(${Math.max(0, qrSpring)})`,
              position: "relative",
            }}
          >
            <div
              style={{
                position: "absolute",
                inset: -30,
                borderRadius: 32,
                background: theme.brand,
                opacity: glowOpacity,
                filter: "blur(30px)",
              }}
            />
            <div
              style={{
                width: 320,
                height: 320,
                backgroundColor: "white",
                borderRadius: 20,
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                position: "relative",
                border: `4px solid ${theme.brand}`,
              }}
            >
              <div
                style={{
                  width: 240,
                  height: 240,
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
                      borderRadius: 3,
                    }}
                  />
                ))}
              </div>
            </div>
          </div>

          {/* Payment badges */}
          <div
            style={{
              display: "flex",
              gap: 24,
              marginTop: 40,
              transform: `scale(${Math.max(0, badgeSpring)})`,
            }}
          >
            <div
              style={{
                backgroundColor: "#FF0033",
                color: "white",
                padding: "14px 28px",
                borderRadius: 10,
                fontSize: 24,
                fontWeight: 700,
              }}
            >
              PayPay
            </div>
            <div
              style={{
                backgroundColor: "#BF0000",
                color: "white",
                padding: "14px 28px",
                borderRadius: 10,
                fontSize: 24,
                fontWeight: 700,
              }}
            >
              楽天ペイ
            </div>
          </div>
        </div>
      </div>
    </AbsoluteFill>
  );
};
