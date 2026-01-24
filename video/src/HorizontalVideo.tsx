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

const { fontFamily } = loadFont();

// QR pattern
const QR_PATTERN = [
  true, true, true, false, true, true, true,
  true, false, true, false, true, false, true,
  true, true, true, false, true, true, true,
  false, false, false, false, false, false, false,
  true, true, true, false, true, false, true,
  true, false, true, false, false, true, false,
  true, true, true, false, true, true, true,
];

// Scene 1: Problem (0-120 frames = 4 seconds)
const ProblemScene: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const textSpring = spring({
    frame,
    fps,
    config: { damping: 200, stiffness: 80 },
  });

  const text2Spring = spring({
    frame: frame - 30,
    fps,
    config: { damping: 200, stiffness: 80 },
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
      }}
    >
      <div
        style={{
          fontSize: 120,
          marginBottom: 40,
          transform: `scale(${textSpring})`,
        }}
      >
        🤔
      </div>
      <div
        style={{
          opacity: textSpring,
          transform: `translateY(${(1 - textSpring) * 30}px)`,
        }}
      >
        <h1
          style={{
            fontSize: 72,
            fontWeight: 700,
            color: theme.textPrimary,
            textAlign: "center",
            margin: 0,
          }}
        >
          NPOを支援したい...
        </h1>
      </div>
      <div
        style={{
          opacity: Math.max(0, text2Spring),
          transform: `translateY(${(1 - Math.max(0, text2Spring)) * 30}px)`,
          marginTop: 24,
        }}
      >
        <h2
          style={{
            fontSize: 64,
            fontWeight: 700,
            color: theme.brand,
            textAlign: "center",
            margin: 0,
          }}
        >
          でも手続きが面倒...
        </h2>
      </div>
    </AbsoluteFill>
  );
};

// Scene 2: Solution (120-240 frames = 4 seconds)
const SolutionScene: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const qrSpring = spring({
    frame,
    fps,
    config: { damping: 8, stiffness: 100 },
  });

  const textSpring = spring({
    frame: frame - 20,
    fps,
    config: { damping: 200, stiffness: 80 },
  });

  const glowOpacity = interpolate(
    frame % 40,
    [0, 20, 40],
    [0.4, 0.8, 0.4],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
  );

  return (
    <AbsoluteFill
      style={{
        backgroundColor: theme.bgPrimary,
        fontFamily,
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        gap: 100,
        padding: "0 100px",
      }}
    >
      {/* QR Code */}
      <div
        style={{
          transform: `scale(${qrSpring})`,
          position: "relative",
        }}
      >
        <div
          style={{
            position: "absolute",
            inset: -40,
            borderRadius: 40,
            background: theme.brand,
            opacity: glowOpacity,
            filter: "blur(40px)",
          }}
        />
        <div
          style={{
            width: 350,
            height: 350,
            backgroundColor: "white",
            borderRadius: 24,
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            position: "relative",
            border: `6px solid ${theme.brand}`,
          }}
        >
          <div
            style={{
              width: 260,
              height: 260,
              display: "grid",
              gridTemplateColumns: "repeat(7, 1fr)",
              gridTemplateRows: "repeat(7, 1fr)",
              gap: 6,
            }}
          >
            {QR_PATTERN.map((filled, i) => (
              <div
                key={i}
                style={{
                  backgroundColor: filled ? theme.bgPrimary : "transparent",
                  borderRadius: 4,
                }}
              />
            ))}
          </div>
        </div>
      </div>

      {/* Text */}
      <div
        style={{
          opacity: textSpring,
          transform: `translateX(${(1 - textSpring) * 50}px)`,
        }}
      >
        <h1
          style={{
            fontSize: 80,
            fontWeight: 700,
            color: theme.textPrimary,
            margin: 0,
            lineHeight: 1.3,
          }}
        >
          QRコードを
          <br />
          <span style={{ color: theme.brand, fontSize: 96 }}>スキャン</span>
          <br />
          するだけ！
        </h1>
      </div>
    </AbsoluteFill>
  );
};

// Scene 3: CTA (240-360 frames = 4 seconds)
const CTAScene: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();

  const logoSpring = spring({
    frame,
    fps,
    config: { damping: 200, stiffness: 100 },
  });

  const textSpring = spring({
    frame: frame - 15,
    fps,
    config: { damping: 200, stiffness: 80 },
  });

  const badgeSpring = spring({
    frame: frame - 40,
    fps,
    config: { damping: 8, stiffness: 100 },
  });

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
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        gap: 80,
        padding: "0 100px",
        opacity: fadeOut,
      }}
    >
      {/* Logo */}
      <div
        style={{
          transform: `scale(${logoSpring})`,
        }}
      >
        <img
          src={staticFile("tadakayo-logo.jpg")}
          alt="Tadakayo"
          style={{
            width: 280,
            height: "auto",
            borderRadius: 24,
            boxShadow: theme.shadowGlow,
          }}
        />
      </div>

      {/* Text */}
      <div
        style={{
          opacity: textSpring,
          transform: `translateX(${(1 - textSpring) * 50}px)`,
          display: "flex",
          flexDirection: "column",
          alignItems: "flex-start",
        }}
      >
        <h1
          style={{
            fontSize: 72,
            fontWeight: 700,
            color: theme.textPrimary,
            margin: 0,
            lineHeight: 1.2,
          }}
        >
          最短
          <span style={{ color: theme.brand, fontSize: 120 }}>2</span>
          タップで
        </h1>
        <h2
          style={{
            fontSize: 96,
            fontWeight: 700,
            color: theme.brand,
            margin: 0,
            marginTop: 16,
          }}
        >
          支援完了！
        </h2>

        {/* Payment badges */}
        <div
          style={{
            display: "flex",
            gap: 20,
            marginTop: 40,
            transform: `scale(${Math.max(0, badgeSpring)})`,
          }}
        >
          <div
            style={{
              backgroundColor: "#FF0033",
              color: "white",
              padding: "16px 32px",
              borderRadius: 12,
              fontSize: 32,
              fontWeight: 700,
            }}
          >
            PayPay
          </div>
          <div
            style={{
              backgroundColor: "#BF0000",
              color: "white",
              padding: "16px 32px",
              borderRadius: 12,
              fontSize: 32,
              fontWeight: 700,
            }}
          >
            楽天ペイ
          </div>
        </div>
      </div>
    </AbsoluteFill>
  );
};

export const HorizontalVideo: React.FC = () => {
  return (
    <AbsoluteFill style={{ backgroundColor: theme.bgPrimary }}>
      {/* Scene 1: Problem (0-4 sec) */}
      <Sequence from={0} durationInFrames={120}>
        <ProblemScene />
      </Sequence>

      {/* Scene 2: Solution (4-8 sec) */}
      <Sequence from={120} durationInFrames={120}>
        <SolutionScene />
      </Sequence>

      {/* Scene 3: CTA (8-12 sec) */}
      <Sequence from={240} durationInFrames={120}>
        <CTAScene />
      </Sequence>
    </AbsoluteFill>
  );
};
