import { AnimatePresence, motion } from 'framer-motion';
import { useVideoPlayer, useRecorder } from '@/lib/video';
import { Scene0_Intro, Scene1_Core, Scene2_Arch, Scene3_Outro } from './AgentScrumMasterScenes';

const SCENE_DURATIONS = {
  intro: 4000,
  core: 6000,
  arch: 5000,
  outro: 5000,
};

const TOTAL_DURATION = Object.values(SCENE_DURATIONS).reduce((a, b) => a + b, 0);

export default function VideoTemplate() {
  const { currentScene } = useVideoPlayer({
    durations: SCENE_DURATIONS,
  });

  const { state, record, downloadVideo, reset, error } = useRecorder(TOTAL_DURATION);

  return (
    <div
      className="w-full h-screen overflow-hidden relative font-body"
      style={{ backgroundColor: 'var(--color-bg-dark)' }}
    >
      <video
        className="absolute inset-0 w-full h-full object-cover opacity-40 mix-blend-screen"
        src={`${import.meta.env.BASE_URL}bg-network.mp4`}
        autoPlay
        muted
        loop
        playsInline
      />
      
      <div className="absolute inset-0 bg-gradient-to-t from-[var(--color-bg-dark)] via-transparent to-[var(--color-bg-dark)] opacity-80" />

      <AnimatePresence mode="wait">
        {currentScene === 0 && <Scene0_Intro key="intro" />}
        {currentScene === 1 && <Scene1_Core key="core" />}
        {currentScene === 2 && <Scene2_Arch key="arch" />}
        {currentScene === 3 && <Scene3_Outro key="outro" />}
      </AnimatePresence>

      <div className="absolute top-4 right-4 z-50 flex items-center gap-3">
        {state === 'idle' && (
          <motion.button
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            onClick={record}
            className="flex items-center gap-2 px-5 py-2.5 rounded-full bg-white/10 backdrop-blur-md border border-white/20 text-white text-sm font-medium hover:bg-white/20 transition-colors cursor-pointer"
          >
            <span className="w-3 h-3 rounded-full bg-red-500" />
            Record & Download
          </motion.button>
        )}

        {state === 'recording' && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="flex items-center gap-2 px-5 py-2.5 rounded-full bg-red-500/20 backdrop-blur-md border border-red-500/40 text-red-300 text-sm font-medium"
          >
            <motion.span
              className="w-3 h-3 rounded-full bg-red-500"
              animate={{ opacity: [1, 0.3, 1] }}
              transition={{ repeat: Infinity, duration: 1 }}
            />
            Recording... ({Math.round(TOTAL_DURATION / 1000)}s)
          </motion.div>
        )}

        {state === 'ready' && (
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            className="flex items-center gap-2"
          >
            <button
              onClick={downloadVideo}
              className="flex items-center gap-2 px-5 py-2.5 rounded-full bg-[var(--color-accent)]/90 text-white text-sm font-bold hover:bg-[var(--color-accent)] transition-colors cursor-pointer"
            >
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
                <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
                <polyline points="7 10 12 15 17 10" />
                <line x1="12" y1="15" x2="12" y2="3" />
              </svg>
              Download Video
            </button>
            <button
              onClick={reset}
              className="px-4 py-2.5 rounded-full bg-white/10 backdrop-blur-md border border-white/20 text-white text-sm hover:bg-white/20 transition-colors cursor-pointer"
            >
              Re-record
            </button>
          </motion.div>
        )}
      </div>

      {error && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0 }}
          className="absolute bottom-6 left-1/2 -translate-x-1/2 z-50 px-6 py-3 rounded-xl bg-red-500/20 backdrop-blur-md border border-red-500/30 text-red-300 text-sm max-w-lg text-center"
        >
          {error}
        </motion.div>
      )}
    </div>
  );
}
