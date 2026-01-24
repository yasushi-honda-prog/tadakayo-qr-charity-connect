import React from "react";
import { Composition } from "remotion";
import { ShortVideo } from "./ShortVideo";
import { HorizontalVideo } from "./HorizontalVideo";

export const RemotionRoot: React.FC = () => {
  return (
    <>
      {/* Main short video - 9:16 vertical format for social media */}
      <Composition
        id="TadakayoShort"
        component={ShortVideo}
        durationInFrames={360} // 12 seconds @ 30fps
        fps={30}
        width={1080}
        height={1920}
      />

      {/* Horizontal video - 16:9 for website hero section */}
      <Composition
        id="TadakayoHorizontal"
        component={HorizontalVideo}
        durationInFrames={360}
        fps={30}
        width={1920}
        height={1080}
      />
    </>
  );
};
