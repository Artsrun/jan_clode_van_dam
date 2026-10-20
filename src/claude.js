import Anthropic from '@anthropic-ai/sdk';
import { config } from './config.js';

const client = new Anthropic({
  apiKey: config.anthropicKey,
});

/**
 * Send a user message to Claude and return the text reply.
 * Keeps the surface deliberately thin so we can later add tools, memory, streaming, etc.
 */
export async function askClaude(userMessage, { system = config.systemPrompt } = {}) {
  const response = await client.messages.create({
    model: config.model,
    max_tokens: 1024,
    system,
    messages: [
      {
        role: 'user',
        content: userMessage,
      },
    ],
  });

  // Anthropic returns an array of content blocks; we only care about text for now
  const textBlock = response.content.find((block) => block.type === 'text');
  return textBlock?.text ?? '(empty response from Claude)';
}
