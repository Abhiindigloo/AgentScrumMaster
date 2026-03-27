import { motion } from 'framer-motion';
import { useEffect, useState } from 'react';

// Common easing
const smoothEase = [0.16, 1, 0.3, 1];

export function Scene0_Intro() {
  return (
    <motion.div
      className="absolute inset-0 flex flex-col items-center justify-center z-10"
      initial={{ opacity: 0, scale: 1.05 }}
      animate={{ opacity: 1, scale: 1 }}
      exit={{ opacity: 0, scale: 0.95, filter: 'blur(10px)' }}
      transition={{ duration: 1.2, ease: smoothEase }}
    >
      <div className="absolute inset-0 bg-gradient-to-b from-transparent via-[var(--color-bg-dark)]/50 to-[var(--color-bg-dark)] pointer-events-none" />

      <motion.div
        initial={{ y: '3vw', opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ delay: 0.4, duration: 1, ease: smoothEase }}
        className="text-center relative z-10 w-full"
      >
        <motion.div
          initial={{ scale: 0.8, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          transition={{ duration: 1.5, ease: smoothEase }}
          className="mb-[2vw]"
        >
          <h1 className="text-[6vw] font-bold text-white tracking-tighter font-display drop-shadow-2xl leading-none">
            Agent<span className="text-[var(--color-accent)]">ScrumMaster</span>
          </h1>
        </motion.div>
        
        <motion.p 
          className="text-[2vw] text-[var(--color-text-secondary)] w-[60vw] mx-auto leading-relaxed font-light"
          initial={{ y: '2vw', opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ delay: 0.8, duration: 1, ease: smoothEase }}
        >
          Bridging the gap between human intuition and automated project management.
        </motion.p>
      </motion.div>
    </motion.div>
  );
}

export function Scene1_Core() {
  const features = [
    { title: "Autonomous Refinement", desc: "Granular user stories with acceptance criteria." },
    { title: "Proactive Blockers", desc: "Detect bottlenecks before they derail." },
    { title: "Intelligent Planning", desc: "RAG-driven realistic workloads." },
    { title: "Automated Stand-ups", desc: "Synthesize progress from GitHub, Jira, Slack." },
  ];

  return (
    <motion.div
      className="absolute inset-0 flex items-center justify-center z-10 p-[5vw]"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0, x: '-5vw', filter: 'blur(5px)' }}
      transition={{ duration: 0.8, ease: smoothEase }}
    >
      <div className="flex w-[90vw] items-center gap-[4vw]">
        <div className="flex-1">
          <motion.h2
            className="text-[3.5vw] font-bold text-white mb-[3vw] font-display leading-tight"
            initial={{ x: '-3vw', opacity: 0 }}
            animate={{ x: 0, opacity: 1 }}
            transition={{ delay: 0.2, duration: 0.8, ease: smoothEase }}
          >
            Core Functionalities
          </motion.h2>

          <div className="flex flex-col gap-[1.5vw]">
            {features.map((feature, i) => (
              <motion.div
                key={i}
                className="bg-[var(--color-secondary)]/30 backdrop-blur-md p-[1.5vw] border-l-[0.2vw] border-[var(--color-accent)] rounded-r-xl"
                initial={{ opacity: 0, x: '-2vw' }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.4 + i * 0.15, duration: 0.6, ease: smoothEase }}
              >
                <h3 className="text-[1.5vw] font-bold text-[var(--color-accent-light)] mb-[0.5vw] font-display leading-tight">{feature.title}</h3>
                <p className="text-[var(--color-text-secondary)] text-[1.2vw] leading-snug">{feature.desc}</p>
              </motion.div>
            ))}
          </div>
        </div>
        
        <motion.div 
          className="flex-1 h-[40vw] max-h-[70vh] relative rounded-2xl overflow-hidden border border-[var(--color-secondary)] shadow-2xl shadow-[var(--color-accent)]/10"
          initial={{ opacity: 0, scale: 0.9, rotateY: 15 }}
          animate={{ opacity: 1, scale: 1, rotateY: 0 }}
          transition={{ delay: 0.6, duration: 1.2, ease: smoothEase }}
          style={{ perspective: 1000 }}
        >
          <img 
            src={`${import.meta.env.BASE_URL}scrum-board.png`} 
            alt="Scrum Board" 
            className="w-full h-full object-cover"
          />
          <div className="absolute inset-0 bg-gradient-to-t from-[var(--color-bg-dark)]/80 to-transparent" />
        </motion.div>
      </div>
    </motion.div>
  );
}

export function Scene2_Arch() {
  const tech = [
    { title: "Reasoning Engine", desc: "Break down complex requirements into actionable tasks." },
    { title: "Tool Use", desc: "Interact directly with VCS and project boards." },
    { title: "Contextual Memory", desc: "Remember team preferences and past decisions." }
  ];

  return (
    <motion.div
      className="absolute inset-0 flex items-center justify-center z-10 p-[5vw]"
      initial={{ opacity: 0, x: '5vw' }}
      animate={{ opacity: 1, x: 0 }}
      exit={{ opacity: 0, scale: 1.1, filter: 'blur(10px)' }}
      transition={{ duration: 0.8, ease: smoothEase }}
    >
      <div className="flex flex-row-reverse w-[90vw] items-center gap-[4vw]">
        <div className="flex-1">
          <motion.h2
            className="text-[3.5vw] font-bold text-white mb-[3vw] font-display leading-tight"
            initial={{ y: '-3vw', opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ delay: 0.2, duration: 0.8, ease: smoothEase }}
          >
            Technical Architecture
          </motion.h2>

          <div className="flex flex-col gap-[2vw]">
            {tech.map((item, i) => (
              <motion.div
                key={i}
                className="flex items-start gap-[1.5vw]"
                initial={{ opacity: 0, y: '2vw' }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.5 + i * 0.2, duration: 0.6, ease: smoothEase }}
              >
                <div className="w-[4vw] h-[4vw] shrink-0 rounded-xl bg-[var(--color-accent)]/10 border border-[var(--color-accent)]/30 flex items-center justify-center text-[var(--color-accent-light)] font-mono font-bold text-[1.5vw] shadow-[0_0_15px_rgba(6,182,212,0.3)]">
                  0{i + 1}
                </div>
                <div>
                  <h3 className="text-[1.8vw] text-white font-display font-semibold mb-[0.5vw] leading-tight">{item.title}</h3>
                  <p className="text-[var(--color-text-secondary)] text-[1.2vw] leading-snug">{item.desc}</p>
                </div>
              </motion.div>
            ))}
          </div>
        </div>

        <motion.div 
          className="flex-1 h-[40vw] max-h-[70vh] relative rounded-2xl overflow-hidden border border-[var(--color-secondary)] shadow-2xl shadow-[var(--color-accent-blue)]/10"
          initial={{ opacity: 0, x: '-5vw', rotateY: -15 }}
          animate={{ opacity: 1, x: 0, rotateY: 0 }}
          transition={{ delay: 0.4, duration: 1.2, ease: smoothEase }}
          style={{ perspective: 1000 }}
        >
          <img 
            src={`${import.meta.env.BASE_URL}reasoning-engine.png`} 
            alt="Reasoning Engine" 
            className="w-full h-full object-cover"
          />
          <div className="absolute inset-0 bg-gradient-to-r from-[var(--color-bg-dark)]/50 to-transparent" />
        </motion.div>
      </div>
    </motion.div>
  );
}

export function Scene3_Outro() {
  return (
    <motion.div
      className="absolute inset-0 flex flex-col items-center justify-center z-10"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      transition={{ duration: 1.5, ease: smoothEase }}
    >
      <div className="absolute inset-0 bg-[var(--color-bg-dark)]/60 backdrop-blur-sm pointer-events-none" />
      
      <motion.div
        className="text-center w-[80vw] relative z-10"
        initial={{ y: '3vw', opacity: 0, scale: 0.95 }}
        animate={{ y: 0, opacity: 1, scale: 1 }}
        transition={{ delay: 0.5, duration: 1.2, ease: smoothEase }}
      >
        <motion.div
           initial={{ opacity: 0, y: '-2vw' }}
           animate={{ opacity: 1, y: 0 }}
           transition={{ delay: 0.8, duration: 1 }}
        >
          <h2 className="text-[4vw] font-bold text-white mb-[2.5vw] leading-tight font-display">
            Empowering developers to stay in <span className="text-[var(--color-accent-light)] italic pr-[0.5vw]">"the flow"</span>
          </h2>
        </motion.div>

        <motion.p 
          className="text-[2vw] text-[var(--color-text-secondary)] font-light leading-relaxed w-[60vw] mx-auto"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 1.5, duration: 1 }}
        >
          Allowing Scrum Masters to focus on coaching and team dynamics rather than manual ticket updates.
        </motion.p>

        <motion.div
          className="mt-[4vw] inline-block"
          initial={{ opacity: 0, scale: 0.8 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 2.2, duration: 0.8, type: "spring" }}
        >
          <div className="px-[2vw] py-[1vw] border border-[var(--color-accent)]/30 rounded-full bg-[var(--color-accent)]/10 text-[var(--color-accent-light)] font-mono text-[1.5vw] uppercase tracking-widest shadow-[0_0_30px_rgba(6,182,212,0.2)]">
            AgentScrumMaster
          </div>
        </motion.div>
      </motion.div>
    </motion.div>
  );
}
