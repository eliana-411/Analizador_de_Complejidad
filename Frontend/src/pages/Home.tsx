import { createSignal } from 'solid-js';
import { H1, H2, Body } from '../components/ui/Typography';
import Button from '../components/ui/Button';
import Card from '../components/ui/Card';
import Input from '../components/ui/Input';
import Badge from '../components/ui/Badge';
import Divider from '../components/ui/Divider';
import ComponentSection from '../components/showcase/ComponentSection';
import CodeBlock from '../components/showcase/CodeBlock';
import ContentContainer from '../components/layout/ContentContainer';

/**
 * Home page - Component showcase and living style guide
 * Displays all UI components with interactive demos
 */
export default function Home() {
  const [inputValue, setInputValue] = createSignal('');
  const [emailValue, setEmailValue] = createSignal('');

  return (
    <ContentContainer>
      {/* Hero section */}
      <div class="mb-12 animate-fade-in-up">
        <H1 gradient>Component Showcase</H1>
        <Body class="text-lg mt-4 max-w-3xl">
          Welcome to the Algorithm Complexity Analyzer design system.
          This living style guide showcases all UI components built with SolidJS,
          Tailwind CSS, and glassomorphic design.
        </Body>
      </div>

      <Divider />

      {/* Typography Section */}
      <ComponentSection
        title="Typography"
        description="Headings and body text with optional gradient effects"
      >
        <div class="space-y-4">
          <H1>Heading 1 - Regular</H1>
          <H1 gradient>Heading 1 - Gradient</H1>
          <H2>Heading 2 - Regular</H2>
          <H2 gradient>Heading 2 - Gradient</H2>
          <Body>Body text - Lorem ipsum dolor sit amet, consectetur adipiscing elit.</Body>
        </div>

        <CodeBlock
          language="tsx"
          code={`<H1>Regular Heading</H1>
<H1 gradient>Gradient Heading</H1>
<Body>Body text content</Body>`}
        />
      </ComponentSection>

      {/* Button Section */}
      <ComponentSection
        title="Buttons"
        description="Four button variants with hover effects and animations"
      >
        <div class="flex flex-wrap gap-4">
          <Button variant="primary">Primary Button</Button>
          <Button variant="secondary">Secondary Button</Button>
          <Button variant="ghost">Ghost Button</Button>
          <Button variant="danger">Danger Button</Button>
          <Button variant="primary" disabled>Disabled</Button>
        </div>

        <CodeBlock
          language="tsx"
          code={`<Button variant="primary">Primary</Button>
<Button variant="secondary">Secondary</Button>
<Button variant="ghost">Ghost</Button>
<Button variant="danger">Danger</Button>`}
        />
      </ComponentSection>

      {/* Card Section */}
      <ComponentSection
        title="Cards"
        description="Glass morphic cards with optional header, footer, and hover effects"
      >
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <Card title="Basic Card">
            <Body>This is a basic card with a title and content.</Body>
          </Card>

          <Card title="Card with Footer" footer={
            <div class="flex justify-end">
              <Button variant="ghost">Cancel</Button>
              <Button variant="primary" class="ml-2">Confirm</Button>
            </div>
          }>
            <Body>This card includes a footer with actions.</Body>
          </Card>

          <Card hover title="Hoverable Card">
            <Body>This card has a hover lift effect. Try hovering over it!</Body>
          </Card>

          <Card>
            <Body>Card without a title - just content.</Body>
          </Card>
        </div>

        <CodeBlock
          language="tsx"
          code={`<Card title="Card Title">
  <Body>Card content here</Body>
</Card>

<Card hover title="Hover Card">
  <Body>Hover for lift effect</Body>
</Card>`}
        />
      </ComponentSection>

      {/* Input Section */}
      <ComponentSection
        title="Input Fields"
        description="Glass input fields with floating labels and focus states"
      >
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6 max-w-4xl">
          <Input
            label="Username"
            value={inputValue()}
            onChange={setInputValue}
            placeholder="Enter your username"
          />

          <Input
            label="Email"
            type="email"
            value={emailValue()}
            onChange={setEmailValue}
            placeholder="Enter your email"
          />

          <Input
            label="With Error"
            value=""
            onChange={() => {}}
            error="This field is required"
          />

          <Input
            value=""
            onChange={() => {}}
            placeholder="Input without label"
          />
        </div>

        <CodeBlock
          language="tsx"
          code={`const [value, setValue] = createSignal('');

<Input
  label="Username"
  value={value()}
  onChange={setValue}
  placeholder="Enter username"
/>`}
        />
      </ComponentSection>

      {/* Badge Section */}
      <ComponentSection
        title="Badges"
        description="Status indicators for complexity results and labels"
      >
        <div class="flex flex-wrap gap-3">
          <Badge variant="success">O(1) - Constant</Badge>
          <Badge variant="success">O(log n) - Logarithmic</Badge>
          <Badge variant="warning">O(n) - Linear</Badge>
          <Badge variant="warning">O(n log n)</Badge>
          <Badge variant="danger">O(n²) - Quadratic</Badge>
          <Badge variant="danger">O(2ⁿ) - Exponential</Badge>
          <Badge variant="info">Info Badge</Badge>
        </div>

        <CodeBlock
          language="tsx"
          code={`<Badge variant="success">O(1)</Badge>
<Badge variant="warning">O(n)</Badge>
<Badge variant="danger">O(n²)</Badge>
<Badge variant="info">Info</Badge>`}
        />
      </ComponentSection>

      {/* Divider Section */}
      <ComponentSection
        title="Dividers"
        description="Gradient dividers for visual separation"
      >
        <div class="space-y-8">
          <div>
            <Body>Content above divider</Body>
            <Divider />
            <Body>Content below divider</Body>
          </div>

          <div class="flex items-center space-x-4">
            <Body>Left content</Body>
            <Divider vertical class="h-12" />
            <Body>Right content</Body>
          </div>
        </div>

        <CodeBlock
          language="tsx"
          code={`<Divider />
<Divider vertical class="h-12" />`}
        />
      </ComponentSection>

      {/* Footer */}
      <div class="mt-16 pt-8 border-t border-white/10">
        <Body class="text-center text-gray-500">
          Algorithm Complexity Analyzer v1.0.0 - Built with SolidJS & Tailwind CSS
        </Body>
      </div>
    </ContentContainer>
  );
}
