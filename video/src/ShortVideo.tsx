import React from "react";
import { TransitionSeries, linearTiming } from "@remotion/transitions";
import { fade } from "@remotion/transitions/fade";
import { slide } from "@remotion/transitions/slide";
import { OpeningScene } from "./scenes/OpeningScene";
import { ProblemScene } from "./scenes/ProblemScene";
import { SolutionScene } from "./scenes/SolutionScene";
import { CTAScene } from "./scenes/CTAScene";

export const ShortVideo: React.FC = () => {
  return (
    <TransitionSeries>
      {/* Scene 1: Opening (0-2 sec = 60 frames) */}
      <TransitionSeries.Sequence durationInFrames={60}>
        <OpeningScene />
      </TransitionSeries.Sequence>

      {/* Transition: Fade */}
      <TransitionSeries.Transition
        presentation={fade()}
        timing={linearTiming({ durationInFrames: 15 })}
      />

      {/* Scene 2: Problem (2-5 sec = 90 frames) */}
      <TransitionSeries.Sequence durationInFrames={90}>
        <ProblemScene />
      </TransitionSeries.Sequence>

      {/* Transition: Slide from right */}
      <TransitionSeries.Transition
        presentation={slide({ direction: "from-right" })}
        timing={linearTiming({ durationInFrames: 15 })}
      />

      {/* Scene 3: Solution (5-9 sec = 120 frames) */}
      <TransitionSeries.Sequence durationInFrames={120}>
        <SolutionScene />
      </TransitionSeries.Sequence>

      {/* Transition: Fade */}
      <TransitionSeries.Transition
        presentation={fade()}
        timing={linearTiming({ durationInFrames: 15 })}
      />

      {/* Scene 4: CTA (9-12 sec = 90 frames) */}
      <TransitionSeries.Sequence durationInFrames={90}>
        <CTAScene />
      </TransitionSeries.Sequence>
    </TransitionSeries>
  );
};
