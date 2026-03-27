import { useState, useCallback, useRef } from 'react';

export type RecorderState = 'idle' | 'recording' | 'ready';

export interface UseRecorderReturn {
  state: RecorderState;
  downloadUrl: string | null;
  record: () => Promise<void>;
  downloadVideo: () => void;
  reset: () => void;
  error: string | null;
}

export function useRecorder(totalDurationMs: number): UseRecorderReturn {
  const [state, setState] = useState<RecorderState>('idle');
  const [downloadUrl, setDownloadUrl] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const chunksRef = useRef<Blob[]>([]);
  const streamRef = useRef<MediaStream | null>(null);

  const record = useCallback(async () => {
    try {
      setError(null);
      const stream = await navigator.mediaDevices.getDisplayMedia({
        video: {
          displaySurface: 'browser',
          frameRate: 30,
          width: 1920,
          height: 1080,
        } as MediaTrackConstraints,
        audio: false,
      });

      streamRef.current = stream;

      const mimeType = MediaRecorder.isTypeSupported('video/webm;codecs=vp9')
        ? 'video/webm;codecs=vp9'
        : 'video/webm';

      const recorder = new MediaRecorder(stream, {
        mimeType,
        videoBitsPerSecond: 8_000_000,
      });

      chunksRef.current = [];

      recorder.ondataavailable = (e) => {
        if (e.data.size > 0) {
          chunksRef.current.push(e.data);
        }
      };

      recorder.onstop = () => {
        stream.getTracks().forEach(t => t.stop());
        streamRef.current = null;

        if (chunksRef.current.length > 0) {
          const blob = new Blob(chunksRef.current, { type: mimeType });
          const url = URL.createObjectURL(blob);
          setDownloadUrl(url);
          setState('ready');
        } else {
          setState('idle');
        }
      };

      stream.getVideoTracks()[0].onended = () => {
        if (recorder.state === 'recording') {
          recorder.stop();
        }
      };

      recorder.start(100);
      mediaRecorderRef.current = recorder;
      setState('recording');

      setTimeout(() => {
        if (mediaRecorderRef.current?.state === 'recording') {
          mediaRecorderRef.current.stop();
        }
      }, totalDurationMs + 2000);

    } catch (err: any) {
      if (err.name === 'NotAllowedError') {
        setError('Screen sharing was cancelled. Click Record and select this tab to capture the video.');
      } else {
        setError('Recording failed. Please try again.');
      }
      setState('idle');
    }
  }, [totalDurationMs]);

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
    if (downloadUrl) {
      URL.revokeObjectURL(downloadUrl);
    }
    if (streamRef.current) {
      streamRef.current.getTracks().forEach(t => t.stop());
      streamRef.current = null;
    }
    setDownloadUrl(null);
    setState('idle');
    setError(null);
  }, [downloadUrl]);

  return {
    state,
    downloadUrl,
    record,
    downloadVideo,
    reset,
    error,
  };
}
