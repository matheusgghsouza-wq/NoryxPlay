import type { Caption } from "@remotion/captions";
import React from "react";
import { interpolate, useCurrentFrame, useVideoConfig } from "remotion";

export type LegendaPalavra = Caption & { pageBreakAfter?: boolean };

type Pagina = { inicioMs: number; fimMs: number; palavras: LegendaPalavra[] };

const agruparPaginas = (legendas: LegendaPalavra[]): Pagina[] => {
  const paginas: Pagina[] = [];
  let atual: LegendaPalavra[] = [];
  legendas.forEach((l, i) => {
    atual.push(l);
    if (l.pageBreakAfter || i === legendas.length - 1) {
      paginas.push({
        inicioMs: atual[0].startMs,
        fimMs: atual[atual.length - 1].endMs,
        palavras: atual,
      });
      atual = [];
    }
  });
  return paginas;
};

// Retorna 0..1 indicando "quanto" a boca deve abrir agora, a partir das legendas.
export const aberturaBoca = (legendas: LegendaPalavra[], ms: number) => {
  const palavra = legendas.find((l) => ms >= l.startMs && ms < l.endMs);
  if (!palavra) return 0;
  const t = (ms - palavra.startMs) / 1000;
  const silabas = Math.max(1, palavra.text.replace(/[^aeiouáéíóúâêôãõà]/gi, "").length);
  const freq = silabas / ((palavra.endMs - palavra.startMs) / 1000);
  return 0.25 + 0.75 * Math.abs(Math.sin(t * Math.PI * freq));
};

export const Legendas: React.FC<{
  legendas: LegendaPalavra[];
  style?: React.CSSProperties;
}> = ({ legendas, style }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const ms = (frame / fps) * 1000;
  const paginas = agruparPaginas(legendas);
  const pagina = paginas.find((p, i) => {
    const proxima = paginas[i + 1];
    return ms >= p.inicioMs && ms < (proxima ? Math.min(proxima.inicioMs, p.fimMs + 400) : p.fimMs + 400);
  });
  if (!pagina) return null;

  const entrada = interpolate(ms, [pagina.inicioMs, pagina.inicioMs + 150], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  return (
    <div
      style={{
        display: "flex",
        flexWrap: "wrap",
        justifyContent: "center",
        alignContent: "center",
        columnGap: 18,
        textAlign: "center",
        fontFamily: "Inter, 'Helvetica Neue', Arial, sans-serif",
        fontWeight: 900,
        fontSize: 72,
        lineHeight: 1.15,
        color: "white",
        WebkitTextStroke: "10px black",
        paintOrder: "stroke fill",
        textShadow: "0 6px 18px rgba(0,0,0,0.6)",
        opacity: entrada,
        transform: `translateY(${(1 - entrada) * 20}px)`,
        ...style,
      }}
    >
      {pagina.palavras.map((p, i) => {
        const ativa = ms >= p.startMs && ms < p.endMs;
        const pop = ativa
          ? interpolate(ms, [p.startMs, p.startMs + 120], [1.18, 1.08], {
              extrapolateRight: "clamp",
            })
          : 1;
        return (
          <span
            key={i}
            style={{
              display: "inline-block",
              color: ativa ? "#FFD54A" : "white",
              transform: `scale(${pop})`,
            }}
          >
            {p.text.trim()}
          </span>
        );
      })}
    </div>
  );
};
