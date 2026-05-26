export interface PatternMeta {
  id: number;
  name: string;
}
export const TOP10 = [6, 8, 17, 100, 103, 145, 146, 148, 151, 152];

export const catalog: PatternMeta[] = Array.from({ length: 155 }, (_, i) => ({
  id: i + 1,
  name: `Pattern ${i + 1}`,
}));

const KNOWN: Record<number, string> = {
  6: 'Negative Constraints / Prohibited Actions',
  8: 'Decision Tree vs Prose',
  17: 'Schema Lock (JSON output contract)',
  100: 'Progressive Disclosure',
  103: 'Reconnaissance-Then-Action',
  145: 'Iron-Law Inviolable Rule Framing',
  146: 'Rationalization-Prevention Table',
  148: 'Anti-Performative-Agreement Vocabulary Ban',
  151: 'HARD-GATE Block Tag',
  152: 'DOT-Graph Decision Flow',
};
for (const [id, name] of Object.entries(KNOWN)) {
  catalog[+id - 1].name = name;
}
