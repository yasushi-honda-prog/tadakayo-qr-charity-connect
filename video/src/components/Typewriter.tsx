import React from "react";
import { useCurrentFrame, interpolate } from "remotion";

type Props = {
  text: string;
  charFrames?: number;
  showCursor?: boolean;
  style?: React.CSSProperties;
};

export const Typewriter: React.FC<Props> = ({
  text,
  charFrames = 2,
  showCursor = true,
  style,
}) => {
  const frame = useCurrentFrame();
  const typedChars = Math.floor(frame / charFrames);
  const displayText = text.slice(0, Math.min(typedChars, text.length));

  // Cursor blinking animation using interpolate
  const cursorOpacity = interpolate(
    frame % 16,
    [0, 8, 16],
    [1, 0, 1],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
  );

  const isComplete = typedChars >= text.length;

  return (
    <span style={style}>
      {displayText}
      {showCursor && (
        <span
          style={{
            opacity: isComplete ? cursorOpacity : 1,
            marginLeft: 2,
          }}
        >
          |
        </span>
      )}
    </span>
  );
};
