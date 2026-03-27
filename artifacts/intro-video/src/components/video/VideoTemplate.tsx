// Video Template - Replace ReplitLoadingScene with your scenes

import { AnimatePresence } from 'framer-motion';
import { useVideoPlayer } from '@/lib/video';
import { Scene0_Intro, Scene1_Core, Scene2_Arch, Scene3_Outro } from './AgentScrumMasterScenes';

const SCENE_DURATIONS = {
  intro: 4000,
  core: 6000,
  arch: 5000,
  outro: 5000,
};

export default function VideoTemplate() {
  const { currentScene } = useVideoPlayer({
    durations: SCENE_DURATIONS,
  });

  return (
    <div
      className="w-full h-screen overflow-hidden relative font-body"
      style={{ backgroundColor: 'var(--color-bg-dark)' }}
    >
      {/* Background Video Layer */}
      <video
        className="absolute inset-0 w-full h-full object-cover opacity-40 mix-blend-screen"
        src={`${import.meta.env.BASE_URL}bg-network.mp4`}
        autoPlay
        muted
        loop
        playsInline
      />
      
      {/* Gradient Overlay */}
      <div className="absolute inset-0 bg-gradient-to-t from-[var(--color-bg-dark)] via-transparent to-[var(--color-bg-dark)] opacity-80" />

      {/* mode="wait" = sequential, "sync" = simultaneous, "popLayout" = new snaps in while old animates out */}
      <AnimatePresence mode="wait">
        {currentScene === 0 && <Scene0_Intro key="intro" />}
        {currentScene === 1 && <Scene1_Core key="core" />}
        {currentScene === 2 && <Scene2_Arch key="arch" />}
        {currentScene === 3 && <Scene3_Outro key="outro" />}
      </AnimatePresence>
    </div>
  );
}
