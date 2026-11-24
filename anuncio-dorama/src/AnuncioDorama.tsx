import { Audio, Video } from "@remotion/media";
import React from "react";
import {
  AbsoluteFill,
  Easing,
  Img,
  interpolate,
  Sequence,
  spring,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import { aberturaBoca, LegendaPalavra, Legendas } from "./Legendas";

type Props = {
  capa: string;
  /** Vídeo da apresentadora (ideal: .webm com fundo transparente). Vazio = apresentadora provisória. */
  apresentadoraVideo: string;
  /** Áudio da fala. Vazio = sem áudio (só se o vídeo da apresentadora já tiver som). */
  voz: string;
  textoCta: string;
  seloIa: string;
  inicioCtaSegundos: number;
};

// Tempos estimados da fala (~11,5 s). Quando chegar o áudio real, ajuste aqui
// (ou transcreva com Whisper e cole o resultado).
const LEGENDAS: LegendaPalavra[] = [
  { text: "Ai,", startMs: 300, endMs: 550, timestampMs: 400, confidence: null },
  { text: " gente,", startMs: 550, endMs: 950, timestampMs: 700, confidence: null },
  { text: " olha", startMs: 1050, endMs: 1300, timestampMs: 1150, confidence: null },
  { text: " só", startMs: 1300, endMs: 1500, timestampMs: 1400, confidence: null },
  { text: " essa", startMs: 1500, endMs: 1750, timestampMs: 1600, confidence: null },
  { text: " novelinha!", startMs: 1750, endMs: 2500, timestampMs: 2000, confidence: null, pageBreakAfter: true },
  { text: "Sabe", startMs: 2700, endMs: 2950, timestampMs: 2800, confidence: null },
  { text: " aquele", startMs: 2950, endMs: 3250, timestampMs: 3100, confidence: null },
  { text: " dorama", startMs: 3250, endMs: 3650, timestampMs: 3400, confidence: null },
  { text: " que", startMs: 3650, endMs: 3800, timestampMs: 3700, confidence: null, pageBreakAfter: true },
  { text: "você", startMs: 3800, endMs: 4050, timestampMs: 3900, confidence: null },
  { text: " começa", startMs: 4050, endMs: 4400, timestampMs: 4200, confidence: null },
  { text: " dizendo", startMs: 4400, endMs: 4800, timestampMs: 4600, confidence: null },
  { text: " ‘só", startMs: 4800, endMs: 5100, timestampMs: 4900, confidence: null },
  { text: " um", startMs: 5100, endMs: 5250, timestampMs: 5150, confidence: null },
  { text: " episódio’?", startMs: 5250, endMs: 5800, timestampMs: 5400, confidence: null, pageBreakAfter: true },
  { text: "Pois", startMs: 6000, endMs: 6250, timestampMs: 6100, confidence: null },
  { text: " é…", startMs: 6250, endMs: 6900, timestampMs: 6400, confidence: null, pageBreakAfter: true },
  { text: "Já", startMs: 7000, endMs: 7200, timestampMs: 7100, confidence: null },
  { text: " coloca", startMs: 7200, endMs: 7550, timestampMs: 7350, confidence: null },
  { text: " na", startMs: 7550, endMs: 7680, timestampMs: 7600, confidence: null },
  { text: " sua", startMs: 7680, endMs: 7900, timestampMs: 7750, confidence: null },
  { text: " lista.", startMs: 7900, endMs: 8500, timestampMs: 8100, confidence: null, pageBreakAfter: true },
  { text: "Quer", startMs: 8700, endMs: 8900, timestampMs: 8800, confidence: null },
  { text: " ver", startMs: 8900, endMs: 9100, timestampMs: 9000, confidence: null },
  { text: " qual", startMs: 9100, endMs: 9350, timestampMs: 9200, confidence: null },
  { text: " é?", startMs: 9350, endMs: 9800, timestampMs: 9500, confidence: null, pageBreakAfter: true },
  { text: "Clique", startMs: 9950, endMs: 10300, timestampMs: 10100, confidence: null },
  { text: " no", startMs: 10300, endMs: 10450, timestampMs: 10350, confidence: null },
  { text: " botão", startMs: 10450, endMs: 10800, timestampMs: 10600, confidence: null },
  { text: " abaixo!", startMs: 10800, endMs: 11500, timestampMs: 11000, confidence: null },
];

// Dimensões da capa original (1086 × 1448) e a faixa onde está o título.
const CAPA_W = 1086;
const CAPA_H = 1448;
const TITULO_Y = 1000;
const TITULO_H = 430;

const Fundo: React.FC<{ capa: string }> = ({ capa }) => {
  const frame = useCurrentFrame();
  const { durationInFrames } = useVideoConfig();
  const zoom = interpolate(frame, [0, durationInFrames], [1.05, 1.16]);
  return (
    <AbsoluteFill style={{ backgroundColor: "#05060f" }}>
      <Img
        src={staticFile(capa)}
        style={{
          position: "absolute",
          height: 2300,
          left: "50%",
          top: 0,
          transform: `translateX(-50%) scale(${zoom})`,
          transformOrigin: "50% 30%",
        }}
      />
      <AbsoluteFill
        style={{
          background:
            "linear-gradient(180deg, rgba(5,6,15,0.85) 0%, rgba(5,6,15,0.25) 26%, rgba(5,6,15,0) 40%, rgba(5,6,15,0.55) 62%, rgba(5,6,15,0.92) 100%)",
        }}
      />
    </AbsoluteFill>
  );
};

const Titulo: React.FC<{ capa: string }> = ({ capa }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const entrada = spring({ frame, fps, config: { damping: 14 } });
  const largura = 1000;
  const escala = largura / CAPA_W;
  const brilho = interpolate(frame % 90, [0, 45, 90], [1, 1.12, 1]);
  return (
    <div
      style={{
        position: "absolute",
        top: 60,
        left: (1080 - largura) / 2,
        width: largura,
        height: TITULO_H * escala,
        overflow: "hidden",
        opacity: entrada,
        transform: `translateY(${(1 - entrada) * -40}px) scale(${0.9 + entrada * 0.1})`,
        filter: `brightness(${brilho}) drop-shadow(0 8px 24px rgba(0,0,0,0.8))`,
        WebkitMaskImage:
          "linear-gradient(180deg, transparent 0%, black 12%, black 88%, transparent 100%)",
        maskImage: "linear-gradient(180deg, transparent 0%, black 12%, black 88%, transparent 100%)",
      }}
    >
      <Img
        src={staticFile(capa)}
        style={{
          position: "absolute",
          width: CAPA_W * escala,
          height: CAPA_H * escala,
          top: -TITULO_Y * escala,
          left: 0,
        }}
      />
    </div>
  );
};

/** Apresentadora provisória: ilustração simples com boca sincronizada às legendas. */
const ApresentadoraProvisoria: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const ms = (frame / fps) * 1000;
  const boca = aberturaBoca(LEGENDAS, ms);
  const piscando = frame % 96 < 4;
  const balanco = Math.sin(frame / 18) * 4;
  const inclinacao = Math.sin(frame / 27) * 1.5;

  return (
    <div style={{ position: "absolute", inset: 0 }}>
      <svg
        viewBox="0 0 900 1160"
        style={{
          position: "absolute",
          width: 900,
          height: 1160,
          left: 90,
          top: 760,
          transform: `translateY(${balanco}px) rotate(${inclinacao}deg)`,
          transformOrigin: "50% 100%",
        }}
      >
        {/* cabelo atrás */}
        <path d="M250 330 Q250 120 450 110 Q650 120 650 330 L690 700 L210 700 Z" fill="#2b1a14" />
        {/* tronco */}
        <path d="M80 1160 L120 1000 Q140 760 330 720 L570 720 Q760 760 780 1000 L820 1160 Z" fill="#c2185b" />
        <path d="M380 720 L450 820 L520 720 Z" fill="#e8b89a" />
        {/* pescoço */}
        <rect x="400" y="560" width="100" height="180" rx="40" fill="#e0ab8b" />
        {/* rosto */}
        <ellipse cx="450" cy="400" rx="165" ry="205" fill="#efc1a2" />
        {/* franja */}
        <path d="M285 330 Q300 170 450 165 Q600 170 615 330 Q560 240 450 245 Q340 240 285 330 Z" fill="#2b1a14" />
        {/* olhos */}
        {piscando ? (
          <>
            <path d="M370 400 q25 8 50 0" stroke="#2b1a14" strokeWidth="6" fill="none" />
            <path d="M480 400 q25 8 50 0" stroke="#2b1a14" strokeWidth="6" fill="none" />
          </>
        ) : (
          <>
            <ellipse cx="395" cy="398" rx="22" ry="25" fill="#fff" />
            <ellipse cx="505" cy="398" rx="22" ry="25" fill="#fff" />
            <circle cx="395" cy="400" r="14" fill="#3b2418" />
            <circle cx="505" cy="400" r="14" fill="#3b2418" />
            <circle cx="400" cy="395" r="4" fill="#fff" />
            <circle cx="510" cy="395" r="4" fill="#fff" />
          </>
        )}
        <path d="M365 360 q30 -16 60 -4" stroke="#2b1a14" strokeWidth="8" fill="none" strokeLinecap="round" />
        <path d="M475 356 q30 -12 60 4" stroke="#2b1a14" strokeWidth="8" fill="none" strokeLinecap="round" />
        {/* bochechas */}
        <ellipse cx="350" cy="470" rx="30" ry="16" fill="#f29c9c" opacity="0.45" />
        <ellipse cx="550" cy="470" rx="30" ry="16" fill="#f29c9c" opacity="0.45" />
        {/* boca: sorriso leve + abertura sincronizada */}
        <path
          d={`M400 505 Q450 ${525 + boca * 10} 500 505 Q450 ${530 + boca * 42} 400 505 Z`}
          fill="#7a2230"
        />
        <path d="M398 504 Q450 518 502 504" stroke="#b5475a" strokeWidth="6" fill="none" strokeLinecap="round" />
      </svg>
      <div
        style={{
          position: "absolute",
          right: 70,
          top: 700,
          padding: "10px 22px",
          borderRadius: 999,
          background: "rgba(255,255,255,0.12)",
          border: "2px dashed rgba(255,255,255,0.6)",
          color: "white",
          fontFamily: "Inter, Arial, sans-serif",
          fontWeight: 700,
          fontSize: 26,
        }}
      >
        PROVISÓRIA · trocar pela apresentadora IA
      </div>
    </div>
  );
};

const Apresentadora: React.FC<{ video: string }> = ({ video }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const entrada = spring({ frame: frame - 4, fps, config: { damping: 16 } });
  return (
    <AbsoluteFill
      style={{
        transform: `translateY(${(1 - entrada) * 300}px)`,
        opacity: entrada,
      }}
    >
      {video ? (
        <Video
          src={staticFile(video)}
          style={{
            position: "absolute",
            bottom: 0,
            left: 0,
            width: 1080,
            height: 1150,
            objectFit: "cover",
            objectPosition: "50% 0%",
          }}
        />
      ) : (
        <ApresentadoraProvisoria />
      )}
    </AbsoluteFill>
  );
};

const Cta: React.FC<{ texto: string }> = ({ texto }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const entrada = spring({ frame, fps, config: { damping: 9, stiffness: 160 } });
  const pulso = 1 + 0.05 * Math.sin((frame / fps) * Math.PI * 3);
  const seta = interpolate(frame % 20, [0, 10, 20], [0, 16, 0], {
    easing: Easing.inOut(Easing.quad),
  });
  return (
    <AbsoluteFill style={{ alignItems: "center", justifyContent: "flex-end", paddingBottom: 110 }}>
      <div
        style={{
          transform: `scale(${entrada * pulso})`,
          padding: "34px 64px",
          borderRadius: 999,
          background: "linear-gradient(180deg, #FFE27A 0%, #F5B400 100%)",
          boxShadow: "0 0 0 6px rgba(255,255,255,0.9), 0 18px 50px rgba(245,180,0,0.65)",
          color: "#1a1200",
          fontFamily: "Inter, Arial, sans-serif",
          fontWeight: 900,
          fontSize: 64,
          letterSpacing: -1,
          whiteSpace: "nowrap",
        }}
      >
        {texto}
      </div>
      <svg
        width="90"
        height="70"
        viewBox="0 0 90 70"
        style={{ marginTop: 18, transform: `translateY(${seta}px)`, opacity: entrada }}
      >
        <path d="M10 10 L45 50 L80 10" stroke="#FFD54A" strokeWidth="14" fill="none" strokeLinecap="round" strokeLinejoin="round" />
      </svg>
    </AbsoluteFill>
  );
};

export const AnuncioDorama: React.FC<Props> = ({
  capa,
  apresentadoraVideo,
  voz,
  textoCta,
  seloIa,
  inicioCtaSegundos,
}) => {
  const { fps } = useVideoConfig();
  const inicioCta = Math.round(inicioCtaSegundos * fps);
  return (
    <AbsoluteFill>
      <Fundo capa={capa} />
      <Titulo capa={capa} />
      <div
        style={{
          position: "absolute",
          top: 490,
          left: 80,
          padding: "8px 18px",
          borderRadius: 12,
          background: "rgba(0,0,0,0.55)",
          color: "rgba(255,255,255,0.9)",
          fontFamily: "Inter, Arial, sans-serif",
          fontWeight: 600,
          fontSize: 26,
        }}
      >
        {seloIa}
      </div>
      <Apresentadora video={apresentadoraVideo} />
      {voz ? <Audio src={staticFile(voz)} /> : null}
      <Sequence durationInFrames={inicioCta} name="Legendas">
        <Legendas
          legendas={LEGENDAS}
          style={{ position: "absolute", left: 80, width: 920, top: 1480, height: 240 }}
        />
      </Sequence>
      <Sequence from={inicioCta} name="CTA">
        <Cta texto={textoCta} />
      </Sequence>
    </AbsoluteFill>
  );
};
