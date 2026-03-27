import { useState, useCallback, useRef, useEffect } from 'react';
import html2canvas from 'html2canvas';

export type RecorderState = 'idle' | 'recording' | 'processing' | 'ready';

export interface UseRecorderReturn {
  state: RecorderState;
  progress: number;
  downloadUrl: string | null;
  record: () => void;
  downloadVideo: () => void;
  reset: () => void;
}

export function useRecorder(
  containerRef: React.RefObject<HTMLDivElement | null>,
  totalDurationMs: number
): UseRecorderReturn {
  const [state, setState] = useState<RecorderState>('idle');
  const [progress, setProgress] = useState(0);
  const [downloadUrl, setDownloadUrl] = useState<string | null>(null);
  const recorderRef = useRef<MediaRecorder | null>(null);
  const chunksRef = useRef<Blob[]>([]);
  const canvasRef = useRef<HTMLCanvasElement | null>(null);
  const animFrameRef = useRef<number>(0);
  const activeRef = useRef(false);
  const startTimeRef = useRef(0);

  useEffect(() => {
    return () => {
      if (animFrameRef.current) cancelAnimationFrame(animFrameRef.current);
      activeRef.current = false;
    };
  }, []);

  const record = useCallback(() => {
    const container = containerRef.current;
    if (!container || state === 'recording') return;

    const canvas = document.createElement('canvas');
    canvas.width = 1920;
    canvas.height = 1080;
    canvasRef.current = canvas;

    const stream = canvas.captureStream(30);
    const mimeType = MediaRecorder.isTypeSupported('video/webm;codecs=vp9')
      ? 'video/webm;codecs=vp9'
      : 'video/webm';

    const recorder = new MediaRecorder(stream, {
      mimeType,
      videoBitsPerSecond: 6_000_000,
    });

    chunksRef.current = [];

    recorder.ondataavailable = (e) => {
      if (e.data.size > 0) chunksRef.current.push(e.data);
    };

    recorder.onstop = () => {
      setState('processing');
      setTimeout(() => {
        const blob = new Blob(chunksRef.current, { type: mimeType });
        const url = URL.createObjectURL(blob);
        setDownloadUrl(url);
        setState('ready');
      }, 500);
    };

    recorder.start(200);
    recorderRef.current = recorder;
    activeRef.current = true;
    startTimeRef.current = performance.now();
    setState('recording');
    setProgress(0);
    setDownloadUrl(null);

    const captureFrame = () => {
      if (!activeRef.current || !container) return;

      const elapsed = performance.now() - startTimeRef.current;
      const pct = Math.min(elapsed / totalDurationMs, 1);
      setProgress(Math.round(pct * 100));

      if (elapsed >= totalDurationMs + 1500) {
        activeRef.current = false;
        if (recorderRef.current?.state === 'recording') {
          recorderRef.current.stop();
        }
        return;
      }

      html2canvas(container, {
        canvas: canvasRef.current!,
        width: container.offsetWidth,
        height: container.offsetHeight,
        scale: 1920 / container.offsetWidth,
        useCORS: true,
        allowTaint: true,
        backgroundColor: '#020617',
        logging: false,
        imageTimeout: 0,
      }).then(() => {
        if (activeRef.current) {
          animFrameRef.current = requestAnimationFrame(captureFrame);
        }
      }).catch(() => {
        if (activeRef.current) {
          animFrameRef.current = requestAnimationFrame(captureFrame);
        }
      });
    };

    animFrameRef.current = requestAnimationFrame(captureFrame);
  }, [containerRef, state, totalDurationMs]);

  const downloadVideo = useCallback(() => {
    if (!downloadUrl) return;
    const a = document.createElement('a');
    a.href = downloadUrl;
    a.download = 'AgentScrumMaster-Intro.webm';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
  }, [downloadUrl]);

  const reset = useCallback(() => {
    activeRef.current = false;
    if (animFrameRef.current) cancelAnimationFrame(animFrameRef.current);
    if (recorderRef.current?.state === 'recording') {
      recorderRef.current.stop();
    }
    if (downloadUrl) URL.revokeObjectURL(downloadUrl);
    setDownloadUrl(null);
    setState('idle');
    setProgress(0);
  }, [downloadUrl]);

  return { state, progress, downloadUrl, record, downloadVideo, reset };
}
