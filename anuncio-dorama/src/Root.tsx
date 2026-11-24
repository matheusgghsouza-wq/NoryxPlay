import { Composition } from "remotion";
import { AnuncioDorama } from "./AnuncioDorama";

export const RemotionRoot: React.FC = () => {
  return (
    <Composition
      id="AnuncioDorama"
      component={AnuncioDorama}
      durationInFrames={360}
      fps={30}
      width={1080}
      height={1920}
      defaultProps={{
        capa: "capa.jpg",
        apresentadoraVideo: "",
        voz: "voz.wav",
        textoCta: "Clique no botão abaixo",
        seloIa: "Apresentadora gerada por IA",
        inicioCtaSegundos: 9.9,
      }}
    />
  );
};
