// Video template library - hook and animation presets

export { useVideoPlayer, useSceneTimer } from './hooks';
export type { SceneDurations, UseVideoPlayerOptions, UseVideoPlayerReturn } from './hooks';

export { useRecorder } from './recorder';
export type { RecorderState, UseRecorderReturn } from './recorder';


export {
  springs,
  easings,
  sceneTransitions,
  elementAnimations,
  charVariants,
  charContainerVariants,
  staggerConfigs,
  containerVariants,
  itemVariants,
  staggerDelay,
  customSpring,
  withDelay,
} from './animations';
