import { CheckCircle } from 'lucide-solid';
import { H1, Body } from '../components/ui/Typography';
import Card from '../components/ui/Card';
import Button from '../components/ui/Button';
import ContentContainer from '../components/layout/ContentContainer';

export default function Validador() {
  return (
    <ContentContainer>
      <div class="flex flex-col items-center justify-center min-h-[60vh] text-center">
        <div class="glass rounded-full p-8 mb-8 animate-float">
          <CheckCircle class="w-16 h-16 text-green-400" />
        </div>

        <H1 gradient class="mb-4">Validador de Pseudocódigo</H1>
        <Body class="text-lg mb-8 max-w-2xl">
          Valida la sintaxis y semántica de tu pseudocódigo antes del análisis de complejidad.
        </Body>

        <Card class="max-w-xl">
          <div class="space-y-4">
            <H1 class="text-2xl">Próximamente</H1>
            <Body>Características en desarrollo:</Body>
            <ul class="text-left space-y-2 text-gray-600">
              <li>• Validación sintáctica</li>
              <li>• Validación semántica</li>
              <li>• Corrección automática de errores</li>
              <li>• Sugerencias de mejora</li>
            </ul>
            <Button variant="primary" onClick={() => window.location.href = '/'}>
              Volver al Inicio
            </Button>
          </div>
        </Card>
      </div>
    </ContentContainer>
  );
}
